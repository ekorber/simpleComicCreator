import os

from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from data import SessionGlobals
from data.ProjectData import ImageLayer
from ops.Operations import OperationHistory
from plyer import filechooser


class FileHandler(Widget):
    popup_window: Popup = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.file_handler = self

    def import_image(self):
        filepath = filechooser.open_file(filters=['*.png', '*.jpg', '*.jpeg', '*.webp'])

        if not filepath:
            return

        SessionGlobals.editor.clear_screen()
        SessionGlobals.layers_tab.clear_layers_tab()

        SessionGlobals.project.add_layer(ImageLayer(filepath[0], (300, 600)))

        SessionGlobals.editor.populate_screen()
        SessionGlobals.layers_tab.populate_layers_tab()

        OperationHistory.confirm_operation(SessionGlobals.project.get_active_layer())
        SessionGlobals.layers_tab.select_layer(SessionGlobals.project.get_active_layer_index())

    def open_project(self):
        filepath = filechooser.open_file(filters=[f'*.{SessionGlobals.PROJECT_FILE_EXTENSION}'])
        SessionGlobals.input_listener.keyboard_open()

        if not filepath:
            return

        SessionGlobals.editor.clear_screen()
        SessionGlobals.layers_tab.clear_layers_tab()

        SessionGlobals.project.load_from_file(filepath[0])

        SessionGlobals.layers_tab.populate_layers_tab()
        SessionGlobals.layers_tab.select_layer(SessionGlobals.project.get_active_layer_index())
        SessionGlobals.page_navigation_widget.refresh_view_no_external_refresh()

        SessionGlobals.editor.populate_screen()

    def pick_save_file_location(self):
        path = filechooser.save_file(filters=[f'*.{SessionGlobals.PROJECT_FILE_EXTENSION}'])
        SessionGlobals.input_listener.keyboard_open()
        if path:
            return path[0]
        else:
            return None
