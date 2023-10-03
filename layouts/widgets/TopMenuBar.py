from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from layouts.menus.EditDropdownMenu import EditDropdownMenu
from layouts.menus.FileDropdownMenu import FileDropdownMenu


class TopMenuBar(BoxLayout):

    file_button = ObjectProperty(Button)
    edit_button = ObjectProperty(Button)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_dropdown = FileDropdownMenu()
        self.edit_dropdown = EditDropdownMenu()

    def open_file_dropdown(self):
        print('file')
        self.file_dropdown.open(self.file_button)

    def open_edit_dropdown(self):
        print('edit')
        self.edit_dropdown.open(self.edit_button)
