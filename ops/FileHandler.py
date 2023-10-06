import os
import shutil

from PIL import Image
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

    def export_project(self):
        path = filechooser.save_file(filters=['*.zip', ])
        SessionGlobals.input_listener.keyboard_open()

        # If cancelled
        if not path:
            return

        # Separate the file extension, if one exists
        filepath = os.path.splitext(path[0])[0]
        file_extension = os.path.splitext(path[0])[1]

        # Delete the existing file if choosing to overwrite
        if file_extension:
            os.remove(path[0])

        # Create a temporary file
        os.mkdir(filepath, 0o666)

        page_size = SessionGlobals.project.size_in_pixels

        # Loop through all the pages
        for page_index in range(len(SessionGlobals.project.pages)):
            page_background_color = (int(SessionGlobals.project.pages[page_index].page_background.color[0] * 255),
                                     int(SessionGlobals.project.pages[page_index].page_background.color[1] * 255),
                                     int(SessionGlobals.project.pages[page_index].page_background.color[2] * 255),
                                     255)

            page_image = Image.new('RGBA', page_size, page_background_color)

            # Name the page pngs
            page_name = ''
            if page_index == 0:
                page_name = 'Front Cover.png'
            else:
                page_name = f'Page {page_index}.png'

            # Loop through all the layers in this page
            for layer in SessionGlobals.project.pages[page_index].layers:

                # Create a new Pillow image, from the current layer's image
                frame = layer.image.texture.pixels
                pil_image = Image.frombytes(mode='RGBA', size=layer.image.texture.size, data=frame)
                pil_image = pil_image.resize((int(layer.size[0]), int(layer.size[1])))
                size = pil_image.size

                # Apply rotation
                position_after_rotation = (0, 0)
                if layer.angle:
                    pil_image = pil_image.rotate(angle=layer.angle, expand=True, fillcolor=(0, 0, 0, 0))
                    position_after_rotation = (size[0] - pil_image.size[0], size[1] - pil_image.size[1])

                # Position layer image properly
                pos = (int(layer.pos[0] - 100 + (position_after_rotation[0] / 2)), int(page_size[1] - size[1] - layer.pos[1] + 100 + (position_after_rotation[1] / 2)))

                # Paste onto page image
                page_image.paste(pil_image, pos, pil_image)

            # Save to disk
            page_image.save(os.path.join(filepath, page_name))

        # Create zip file from folder
        shutil.make_archive(os.path.basename(filepath), 'zip', filepath)

        # Clean up by deleting the folder, leaving only the zip file
        shutil.rmtree(filepath)
