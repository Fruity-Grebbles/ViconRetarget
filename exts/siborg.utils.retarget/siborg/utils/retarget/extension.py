import omni.ext
import omni.ui as ui
from omni.anim.retarget.core import load_auto_map
import os


# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class SiborgUtilsRetargetExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[siborg.utils.retarget] siborg utils retarget startup")
        # Add an automap to the retarget manager for VICON data
        global ext_path
        ext_path = omni.kit.app.get_app().get_extension_manager().get_extension_path(ext_id)
        rig_path = os.path.join(ext_path, "data", "rigs", "Biped")
        load_auto_map(rig_path, False)

    def on_shutdown(self):
        print("[siborg.utils.retarget] siborg utils retarget shutdown")
