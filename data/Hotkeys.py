class Hotkey:
    def __init__(self, keycode, modifiers=None):
        if modifiers is None:
            modifiers = []

        self.keycode = keycode
        self.modifiers = modifiers
        if modifiers:
            self.are_modifiers_relevant = True
        else:
            self.are_modifiers_relevant = False

    def is_pressed(self, keycode, modifiers):
        if self.are_modifiers_relevant:
            num_required_modifiers_found = 0
            for mod in modifiers:
                for self_mod in self.modifiers:
                    if mod == self_mod:
                        num_required_modifiers_found += 1

            return self.keycode == keycode and num_required_modifiers_found == len(self.modifiers)
        else:
            return self.keycode == keycode


TRANSLATE_KEY = Hotkey(keycode=(103, 'g'))
ROTATE_KEY = Hotkey(keycode=(114, 'r'))
SCALE_KEY = Hotkey(keycode=(115, 's'))

X_AXIS_LOCK_KEY = Hotkey(keycode=(120, 'x'))
Y_AXIS_LOCK_KEY = Hotkey(keycode=(121, 'y'))
Z_AXIS_LOCK_KEY = Hotkey(keycode=(122, 'z'))

NEW_PROJECT_KEY = Hotkey(keycode=(110, 'n'), modifiers=['shift', 'ctrl'])
OPEN_PROJECT_KEY = Hotkey(keycode=(111, 'o'), modifiers=['shift', 'ctrl'])
SAVE_PROJECT_KEY = Hotkey(keycode=(115, 's'), modifiers=['ctrl'])
SAVE_PROJECT_AS_KEY = Hotkey(keycode=(115, 's'), modifiers=['shift', 'ctrl'])
EXPORT_PROJECT_KEY = Hotkey(keycode=(101, 'e'), modifiers=['ctrl'])

NEW_LAYER_KEY = Hotkey(keycode=(110, 'n'))
NEW_PAGE_KEY = Hotkey(keycode=(110, 'n'), modifiers=['shift'])

NEXT_PAGE_KEY = Hotkey(keycode=(275, 'right'))
PREVIOUS_PAGE_KEY = Hotkey(keycode=(276, 'left'))

UNDO_KEY = Hotkey(keycode=(122, 'z'), modifiers=['ctrl'])
REDO_KEY = Hotkey(keycode=(122, 'z'), modifiers=['ctrl', 'shift'])

CONFIRM_KEY = Hotkey(keycode=(13, 'enter'))
CANCEL_KEY = Hotkey(keycode=(27, 'escape'))
