import omni.ui as ui
from .widget import AnimationPreviewWidget
import omni.usd

class AnimationPreviewWindow(ui.Window):

    def __init__(self, *args, **kwargs):

        super().__init__("Animation Preview", *args, **kwargs)

        self.usd_context = omni.usd.create_context("anim_preview")

        with self.frame:
            self.__preview_widget = AnimationPreviewWidget(self.usd_context.get_name(), resolution=(600, 600))

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.__preview_widget.destroy()
        self.__preview_widget = None
        super().destroy()
