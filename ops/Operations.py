from enum import Enum


# def overlapping(pos: (int, int), rect_pos: (int, int), rect_size: (int, int)):
#     return rect_pos[0] <= pos[0] <= rect_pos[0] + rect_size[0] and rect_pos[1] <= pos[1] <= rect_pos[1] + rect_size[1]


class OperationType(Enum):
    NO_OP = -1
    TRANSLATE = 0
    ROTATE = 1
    SCALE = 2


class Translate:
    last_mouse_pos = [0, 0]
    original_pos = [0, 0]

    @staticmethod
    def on_touch_down(pos, active_layer_image):
        Translate.last_mouse_pos[:] = pos
        Translate.original_pos = [active_layer_image.pos[0], active_layer_image.pos[1]]

    @staticmethod
    def on_touch_move(pos, active_layer_image):
        delta_mouse_pos = (pos[0] - Translate.last_mouse_pos[0], pos[1] - Translate.last_mouse_pos[1])
        active_layer_image.pos = (active_layer_image.pos[0] + delta_mouse_pos[0], active_layer_image.pos[1]
                                  + delta_mouse_pos[1])
        Translate.last_mouse_pos[:] = pos

    @staticmethod
    def on_touch_up():
        pass

    @staticmethod
    def cancel(active_layer_image):
        active_layer_image.pos = Translate.original_pos


class Rotate:
    last_mouse_pos_x = 0
    original_angle = 0

    @staticmethod
    def on_touch_down(pos, active_layer_image):
        Rotate.last_mouse_pos_x = pos[0]
        Rotate.original_angle = active_layer_image.angle

    @staticmethod
    def on_touch_move(pos, active_layer_image):
        delta_mouse_pos_x = (pos[0] - Rotate.last_mouse_pos_x)
        active_layer_image.angle -= (delta_mouse_pos_x * 0.1)
        Rotate.last_mouse_pos_x = pos[0]

    @staticmethod
    def on_touch_up():
        pass

    @staticmethod
    def cancel(active_layer_image):
        active_layer_image.angle = Rotate.original_angle


class Scale:
    last_mouse_pos_x = 0
    altered_pos = [0, 0]
    original_pos = [0, 0]
    original_size = [0, 0]

    @staticmethod
    def on_touch_down(pos, active_layer_image):
        Scale.last_mouse_pos_x = pos[0]
        Scale.original_pos = [active_layer_image.pos[0], active_layer_image.pos[1]]
        Scale.altered_pos = [active_layer_image.pos[0], active_layer_image.pos[1]]
        Scale.original_size = [active_layer_image.size[0], active_layer_image.size[1]]

    @staticmethod
    def on_touch_move(pos, active_layer_image):
        aspect_ratio = active_layer_image.image.texture_size[0] / active_layer_image.image.texture_size[1]
        delta_mouse_pos_x = (pos[0] - Scale.last_mouse_pos_x)
        active_layer_image.size = (active_layer_image.size[0] + (delta_mouse_pos_x * aspect_ratio),
                                   (active_layer_image.size[1] + delta_mouse_pos_x))
        active_layer_image.pos = (Scale.altered_pos[0] - (delta_mouse_pos_x / 2), Scale.altered_pos[1]
                                  - (delta_mouse_pos_x / 2))
        Scale.altered_pos = active_layer_image.pos
        Scale.last_mouse_pos_x = pos[0]

    @staticmethod
    def on_touch_up():
        pass

    @staticmethod
    def cancel(active_layer_image):
        active_layer_image.size = Scale.original_size
        active_layer_image.pos = Scale.original_pos
