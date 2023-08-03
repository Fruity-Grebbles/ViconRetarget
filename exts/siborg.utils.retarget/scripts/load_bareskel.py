# Module for loading malformed USD files which only contain a skeleton

import omni.usd
from pxr import Usd, UsdGeom, UsdSkel

def get_skeleton_in_stage(stage):
    """Returns the first skeleton in the stage, if any"""
    return next(
        (prim for prim in stage.Traverse() if prim.IsA(UsdSkel.Root)), None
    )


if __name__ == '__main__':

    usd_context = omni.usd.get_context()
    stage = usd_context.get_stage()

    skeleton = get_skeleton_in_stage(stage)
    if not skeleton:
        raise RuntimeError('No skeleton found in stage')

    skeleton.GetParent().GetPrim().GetStage().Export(args.output)