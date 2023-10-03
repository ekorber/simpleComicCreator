from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data import SessionGlobals


class FileDropdownMenu(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_width = False
        self.width = 300

        new = Button(text='New Project (Ctrl + Shift + N)')
        new.size_hint = (None, None)
        new.size = (250, 50)
        new.bind(on_release=lambda instance: self.on_new_project_click())
        self.add_widget(new)

        open_btn = Button(text='Open Project (Ctrl + Shift + O)')
        open_btn.size_hint = (None, None)
        open_btn.size = (250, 50)
        open_btn.bind(on_release=lambda instance: self.on_open_project_click())
        self.add_widget(open_btn)

        save = Button(text='Save Project (Ctrl + S)')
        save.size_hint = (None, None)
        save.size = (250, 50)
        save.bind(on_release=lambda instance: self.on_save_project_click())
        self.add_widget(save)

        save_as = Button(text='Save Project As (Ctrl + Shift + S)')
        save_as.size_hint = (None, None)
        save_as.size = (250, 50)
        save_as.bind(on_release=lambda instance: self.on_save_project_as_click())
        self.add_widget(save_as)

        export = Button(text='Export Project')
        export.size_hint = (None, None)
        export.size = (250, 50)
        export.bind(on_release=lambda instance: self.on_export_click())
        self.add_widget(export)

    def on_new_project_click(self):
        self.dismiss()
        SessionGlobals.new_project_handler.open_new_project_window()

    def on_open_project_click(self):
        self.dismiss()
        SessionGlobals.file_handler.open_project()

    def on_save_project_click(self):
        self.dismiss()
        SessionGlobals.project.save_data_to_file()

    def on_save_project_as_click(self):
        self.dismiss()
        SessionGlobals.project.save_data_to_file(save_as=True)

    def on_export_click(self):
        print('export')
        self.dismiss()
