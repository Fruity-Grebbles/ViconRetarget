# Utility to add retargeting to animated skeletons in USD.
# Must be run inside omniverse kit eg `kit.exe --exec auto_retarget.py <args>`

from pxr import Usd, UsdSkel, Sdf, AnimationSkelBindingAPI
import omni
from omni.anim.retarget.core import load_auto_map, auto_setup_by_prim



def retarget_stage(stage: Usd.Stage, rigname='Biped', use_mapping=True, auto_facing=True, auto_tagging=False, auto_posing=True):
    """Sets up the first skeleton in the given USD file for animation retargeting"""

    ensure_default_prim(stage)

    if skeleton := get_skeleton_in_stage(stage):
        print(f'Setting up retargeting for {skeleton.GetPath()}')
        auto_setup_by_prim(rigname, skeleton, use_mapping, auto_facing, auto_tagging, auto_posing)
        stage.Save()
    else:
        raise RuntimeError(f'No skeleton found in stage for {stage} Unable to set up retargeting')


def retarget_file(filename):
    """Sets up retargeting for the first skeleton in the given USD file"""
    if filename.endswith('.usd') or filename.endswith('.usda'):
        stage = open_usd_file(filename)
        retarget_stage(stage)
    raise ValueError(f'{filename} is not a USD file - skipping')


def retarget_all(path):
    """Sets up retargeting for all skeletons in USD files in the given path"""
    import os
    for filename in os.listdir(path):
        if filename.endswith('.usd') or filename.endswith('.usda'):
            stage = open_usd_file(os.path.join(path, filename))
            retarget_stage(stage)


def bind_animations(skeleton: UsdSkel.Skeleton):
    """Apply AnimationSkelBindingAPI to each animation under a skeleton in the prim hierarchy. This is a custom schema
    from NVIDIA, and not a part of Pixar's USD spec.
    https://docs.omniverse.nvidia.com/extensions/latest/ext_animation-retargeting.html#retargeting-with-skelanimation"""
    for child in skeleton.GetPrim().GetChildren():
        if child.IsA(UsdSkel.Animation):
            binding = AnimationSkelBindingAPI.Apply(child)
            binding.CreateSourceSkeletonRel().SetTargets([skeleton.GetPrim().GetPath()])


def open_usd_file(filename) -> Usd.Stage:
    """opens a USD file and returns the stage"""
    if filename.endswith('.usd') or filename.endswith('.usda'):
        return Usd.Stage.Open(filename)
    raise ValueError(f'{filename} is not a USD file - skipping')


def get_skeleton_in_stage(stage):
    """Returns the first skeleton in the stage, if any"""
    return next(
        (prim for prim in stage.Traverse() if prim.IsA(UsdSkel.Skeleton)), None
    )


def ensure_default_prim(stage: Usd.Stage) -> Sdf.Path:
    """Ensures the stage has a default prim. If not, sets the first skeleton as the default prim"""
    if not stage.HasDefaultPrim:
        if skeleton := get_skeleton_in_stage(stage):
            stage.SetDefaultPrim(skeleton)
            stage.Save()
        else:
            raise RuntimeError('No skeleton found for default prim!')
    return stage.GetDefaultPrim()


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input USD file')
    parser.add_argument('--retarget-all', '-r', action='store_true',
                        help='Auto-retarget skeletons for all files in the given path')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise RuntimeError('Input file does not exist')
    
    automap_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'rigs', 'Karin')
    load_auto_map(automap_path)

    if args.retarget_all:
        if os.path.isdir(args.input):
            retarget_all(args.input)
        else:
            raise RuntimeError('Input path is not a directory')
    else:
        retarget_file(args.input)
