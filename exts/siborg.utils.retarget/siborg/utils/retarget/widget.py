import omni.ui as ui
from typing import Union
from omni.kit.widget.viewport import ViewportWidget
from omni.kit.viewport.actions import actions
from omni.kit.manipulator.camera import ViewportCameraManipulator
import omni.usd
from pxr import Sdf
import os
from .shared import get_ext_path

class AnimationPreviewWidget:
    def __init__(self, context_name:str, resolution: Union[tuple, str] = None, *ui_args ,**ui_kw_args):
        """ A widget that displays a preview of a USD animation, with a camera manipulator to control the camera.
        Args:
            context_name: The name of the USD context to use for the viewport
            resolution (x, y): The resolution of the backing texture, or 'fill_frame' to match the widget's ui-size
            *ui_args, **ui_kw_args: Additional arguments to pass to the ViewportWidget's parent frame
        """

        self.skel_path = Sdf.Path("/World/Karin")
        self.camera_path = Sdf.Path("/World/Camera")



        # Put the Viewport in a ZStack so that a background rectangle can be added underneath
        self.__ui_container = ui.ZStack()
        with self.__ui_container:
            # Add a background Rectangle that is black by default, but can change with a set_style 
            ui.Rectangle(style_type_name_override='ViewportBackgroundColor', style={'ViewportBackgroundColor': {'background_color': 0xff000000}})

            # Create the ViewportWidget, forwarding all of the arguments to this constructor
            self.__vp_widget = ViewportWidget(usd_context_name=context_name, camera_path=self.camera_path, resolution=resolution, *ui_args, **ui_kw_args)
            # Make skeleton visible by default
            actions.toggle_skeleton_visibility(self.__vp_widget.viewport_api, True)

            # Add the omni.ui.scene.SceneView that is going to host the camera-manipulator
            self.__scene_view = ui.scene.SceneView(aspect_ratio_policy=ui.scene.AspectRatioPolicy.STRETCH)

            # And finally add the camera-manipulator into that view
            with self.__scene_view.scene:
                self.__camera_manip = ViewportCameraManipulator(self.viewport_api)
                model = self.__camera_manip.model

                # Let's disable any undo for these movements as we're a preview-window
                model.set_ints('disable_undo', [1])

                # We'll also let the Viewport automatically push view and projection changes into our scene-view
                self.viewport_api.add_scene_view(self.__scene_view)

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.__view_change_sub = None
        if self.__camera_manip:
            self.__camera_manip.destroy()
            self.__camera_manip = None
        if self.__scene_view:
            self.__scene_view.destroy()
            self.__scene_view = None
        if self.__vp_widget:
            self.__vp_widget.destroy()
            self.__vp_widget = None
        if self.__ui_container:
            self.__ui_container.destroy()
            self.__ui_container = None

    @property
    def viewport_api(self):
        # Access to the underying ViewportAPI object to control renderer, resolution
        return self.__vp_widget.viewport_api

    @property
    def scene_view(self):
        # Access to the omni.ui.scene.SceneView
        return self.__scene_view

    def set_style(self, *args, **kwargs):
        # Give some styling access
        self.__ui_container.set_style(*args, **kwargs)
