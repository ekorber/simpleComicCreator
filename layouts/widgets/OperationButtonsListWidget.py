from kivy.properties import ObjectProperty
from kivy.uix.stacklayout import StackLayout

from data import SessionGlobals
from ops.Operations import OperationType


class OperationButtonsListWidget(StackLayout):
    move_button = ObjectProperty(None)
    rotate_button = ObjectProperty(None)
    scale_button = ObjectProperty(None)

    selected_color = (1, 1, 1, 1)
    unselected_color = (1, 1, 1, 0.5)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.op_button_list = self

    def set_op_move(self):
        SessionGlobals.active_operation = OperationType.TRANSLATE
        self.set_button_colors()

    def set_op_rotate(self):
        SessionGlobals.active_operation = OperationType.ROTATE
        self.set_button_colors()

    def set_op_scale(self):
        SessionGlobals.active_operation = OperationType.SCALE
        self.set_button_colors()

    def set_button_colors(self):
        if SessionGlobals.active_operation == OperationType.TRANSLATE:
            self.move_button.background_color = self.selected_color
            self.rotate_button.background_color = self.unselected_color
            self.scale_button.background_color = self.unselected_color
        elif SessionGlobals.active_operation == OperationType.ROTATE:
            self.move_button.background_color = self.unselected_color
            self.rotate_button.background_color = self.selected_color
            self.scale_button.background_color = self.unselected_color
        elif SessionGlobals.active_operation == OperationType.SCALE:
            self.move_button.background_color = self.unselected_color
            self.rotate_button.background_color = self.unselected_color
            self.scale_button.background_color = self.selected_color
