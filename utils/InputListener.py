from kivy.core.window import Window
from kivy.uix.widget import Widget

from data import SessionGlobals
from data.Hotkeys import *
from ops.Operations import *


class InputListener(Widget):

    keyboard = None
    mouse_pos = (0, 0)
    hotkey_operation_active = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.input_listener = self
        Window.bind(mouse_pos=lambda w, p: self.handle_mouse_input(p))
        self.keyboard_open()

    def keyboard_open(self):
        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down)

    def keyboard_closed(self):
        print('My keyboard have been closed!')
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        # print(' - modifiers are %r' % modifiers)

        self.handle_keyboard_input(keycode, modifiers)

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def handle_mouse_input(self, pos):
        self.mouse_pos = pos
        if self.hotkey_operation_active:
            if SessionGlobals.active_operation == OperationType.TRANSLATE:
                Translate.on_touch_move(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())
            elif SessionGlobals.active_operation == OperationType.ROTATE:
                Rotate.on_touch_move(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())
            elif SessionGlobals.active_operation == OperationType.SCALE:
                Scale.on_touch_move(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())

            SessionGlobals.layer_collection.get_active_layer().render()

    def on_touch_down(self, touch):
        if self.hotkey_operation_active:
            self.confirm_operation()

    def confirm_operation(self):
        print('Confirming op from InputListener')
        if SessionGlobals.active_operation == OperationType.TRANSLATE:
            Translate.confirm(SessionGlobals.layer_collection.get_active_layer())
        elif SessionGlobals.active_operation == OperationType.ROTATE:
            Rotate.confirm(SessionGlobals.layer_collection.get_active_layer())
        elif SessionGlobals.active_operation == OperationType.SCALE:
            Scale.confirm(SessionGlobals.layer_collection.get_active_layer())

        self.hotkey_operation_active = False

    def cancel_operation(self):
        if SessionGlobals.active_operation == OperationType.TRANSLATE:
            Translate.cancel(SessionGlobals.layer_collection.get_active_layer())
        elif SessionGlobals.active_operation == OperationType.ROTATE:
            Rotate.cancel(SessionGlobals.layer_collection.get_active_layer())
        elif SessionGlobals.active_operation == OperationType.SCALE:
            Scale.cancel(SessionGlobals.layer_collection.get_active_layer())

        SessionGlobals.layer_collection.get_active_layer().render()
        self.hotkey_operation_active = False

    def handle_keyboard_input(self, keycode=None, modifiers=None):

        if self.hotkey_operation_active:
            if CONFIRM_KEY.is_pressed(keycode, modifiers):
                self.confirm_operation()
            elif CANCEL_KEY.is_pressed(keycode, modifiers):
                self.cancel_operation()

            return

        if TRANSLATE_KEY.is_pressed(keycode, modifiers):
            if len(SessionGlobals.layer_collection.layers) == 0:
                return

            if SessionGlobals.editor.mouse_operation_active:
                return

            self.hotkey_operation_active = True
            SessionGlobals.active_operation = OperationType.TRANSLATE
            SessionGlobals.op_button_list.set_button_colors()
            Translate.on_touch_down(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())

        elif ROTATE_KEY.is_pressed(keycode, modifiers):
            if len(SessionGlobals.layer_collection.layers) == 0:
                return

            if SessionGlobals.editor.mouse_operation_active:
                return

            self.hotkey_operation_active = True
            SessionGlobals.active_operation = OperationType.ROTATE
            SessionGlobals.op_button_list.set_button_colors()
            Rotate.on_touch_down(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())

        elif SCALE_KEY.is_pressed(keycode, modifiers):
            if len(SessionGlobals.layer_collection.layers) == 0:
                return

            if SessionGlobals.editor.mouse_operation_active:
                return

            self.hotkey_operation_active = True
            SessionGlobals.active_operation = OperationType.SCALE
            SessionGlobals.op_button_list.set_button_colors()
            Scale.on_touch_down(self.mouse_pos, SessionGlobals.layer_collection.get_active_layer())

        elif NEW_LAYER_KEY.is_pressed(keycode, modifiers):
            SessionGlobals.layers_tab.on_new_image_layer()

        # Make sure the hotkeys requiring more modifiers appear higher up in the list
        elif REDO_KEY.is_pressed(keycode, modifiers):
            if OperationHistory.can_redo():
                OperationHistory.redo()
                SessionGlobals.layers_tab.refresh_view()

        elif UNDO_KEY.is_pressed(keycode, modifiers):
            if OperationHistory.can_undo():
                OperationHistory.undo()
                SessionGlobals.layers_tab.refresh_view()


