# Simple script to fix USD files from Vicon Shogun that have a stage and skeleton with no default prim

from pxr import Usd, UsdSkel
import os


def get_skeleton_in_stage(stage):
    """Returns the first skeleton in the stage, if any"""
    return next(
        (prim for prim in stage.Traverse() if prim.IsA(UsdSkel.Skeleton)), None
    )


def fix_all(path):
    """Fixes all malformed USD files in the given path"""
    import os
    for filename in os.listdir(path):
        fix(os.path.join(path, filename))


def fix(filename):
    """Fixes the given malformed USD file"""

    if filename.endswith('.usd') or filename.endswith('.usda'):
        stage = Usd.Stage.Open(filename)
        if skeleton := get_skeleton_in_stage(stage):
            # Set the skeleton as the default prim
            print(f'Setting {skeleton.GetPath()} as default prim in {filename}')
            stage.SetDefaultPrim(skeleton)
            stage.Save()
        else:
            print(f'No skeleton found in stage for {filename} - nothing to fix')
    else:
        print(f'{filename} is not a USD file - skipping')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input USD file')
    parser.add_argument('--fix-all', action='store_true', help='Fix all USD files in the given path')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise RuntimeError('Input file does not exist')

    if args.fix_all:
        if os.path.isdir(args.input):
            fix_all(args.input)
        else:
            raise RuntimeError('Input path is not a directory')
    else:
        fix(args.input)

