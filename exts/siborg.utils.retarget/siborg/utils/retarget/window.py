import omni.ui as ui
from .widget import AnimationPreviewWidget
import omni.usd
import os
from .shared import get_ext_path

class AnimationPreviewWindow(ui.Window):

    def __init__(self, *args, **kwargs):

        super().__init__("Animation Preview", *args, **kwargs)

        self.usd_context = omni.usd.create_context("anim_preview")

        self.frame.set_build_fn(self._build_ui)


    def _build_ui(self):
        with self.frame:
            with ui.VStack():
                self.__preview_widget = AnimationPreviewWidget(self.usd_context.get_name(), resolution=(600, 600))
                ui.Button("Open Stage", clicked_fn=self._open_stage)

    def _open_stage(self):
        # Open a USD stage and get the skeleton to apply animations to
        ext_path = get_ext_path()
        # Open the USD stage and get the skeleton to apply animations to
        self.usd_context = omni.usd.get_context(self.usd_context)
        self.usd_context.open_stage(os.path.join(ext_path, "data", "anim_preview.usd"))

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.__preview_widget:
            self.__preview_widget.destroy()
            self.__preview_widget = None
        if self.usd_context:
            self.usd_context.remove_all_hydra_engines()
        super().destroy()
