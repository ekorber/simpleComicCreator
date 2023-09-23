from kivy.uix.widget import Widget

from data import SessionGlobals
from ops.Operations import OperationType, Translate, Rotate, Scale


class EditorTab(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.editor = self
        self.mouse_operation_active = False

    def clear_screen(self):
        for img in SessionGlobals.project.get_current_page().layers:
            self.remove_widget(img)

    def populate_screen(self):
        for img in SessionGlobals.project.get_current_page().layers:
            self.add_widget(img)

    def refresh_view(self):
        self.clear_screen()
        self.populate_screen()

    def on_touch_down(self, touch):
        if len(SessionGlobals.project.get_current_page().layers) == 0:
            return

        if SessionGlobals.input_listener.hotkey_operation_active:
            return

        self.mouse_operation_active = True

        if SessionGlobals.active_operation == OperationType.TRANSLATE:
            Translate.on_touch_down(touch.pos, SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.ROTATE:
            Rotate.on_touch_down(touch.pos, SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.SCALE:
            Scale.on_touch_down(touch.pos, SessionGlobals.project.get_active_layer())

    def on_touch_move(self, touch):
        if len(SessionGlobals.project.get_current_page().layers) == 0:
            return

        if SessionGlobals.input_listener.hotkey_operation_active:
            return

        if not self.mouse_operation_active:
            return

        if SessionGlobals.active_operation is OperationType.TRANSLATE:
            Translate.on_touch_move(touch.pos, SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.ROTATE:
            Rotate.on_touch_move(touch.pos, SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.SCALE:
            Scale.on_touch_move(touch.pos, SessionGlobals.project.get_active_layer())

        SessionGlobals.project.get_active_layer().render()

    def on_touch_up(self, touch):
        if len(SessionGlobals.project.get_current_page().layers) == 0:
            return

        if SessionGlobals.input_listener.hotkey_operation_active:
            return

        if not self.mouse_operation_active:
            return

        if SessionGlobals.active_operation == OperationType.TRANSLATE:
            Translate.on_touch_up(SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.ROTATE:
            Rotate.on_touch_up(SessionGlobals.project.get_active_layer())
        elif SessionGlobals.active_operation is OperationType.SCALE:
            Scale.on_touch_up(SessionGlobals.project.get_active_layer())

        self.mouse_operation_active = False
