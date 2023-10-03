from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from ops.Operations import OperationHistory


class EditDropdownMenu(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auto_width = False
        self.width = 300

        undo = Button(text='Undo (Ctrl + Z)')
        undo.size_hint = (None, None)
        undo.size = (250, 50)
        undo.bind(on_release=lambda instance: self.on_undo_click())
        self.add_widget(undo)

        redo = Button(text='Redo (Ctrl + Shift + Z)')
        redo.size_hint = (None, None)
        redo.size = (250, 50)
        redo.bind(on_release=lambda instance: self.on_redo_click())
        self.add_widget(redo)

    def on_undo_click(self):
        OperationHistory.undo()

    def on_redo_click(self):
        OperationHistory.redo()
