from enum import Enum
from copy import copy

from data import SessionGlobals
from data.ProjectData import ImageLayer


# def overlapping(pos: (int, int), rect_pos: (int, int), rect_size: (int, int)):
#     return rect_pos[0] <= pos[0] <= rect_pos[0] + rect_size[0] and rect_pos[1] <= pos[1] <= rect_pos[1] + rect_size[1]


class OperationType(Enum):
    NO_OP = -1
    TRANSLATE = 0
    ROTATE = 1
    SCALE = 2


class OperationHistoryNode:
    def __init__(self, layer: ImageLayer, pos, angle, size, layer_name):
        self.layer = layer
        self.pos = pos
        self.angle = angle
        self.size = size
        self.layer_name = layer_name


class OperationHistory:
    MAX_UNDO_LENGTH = 128
    history = []
    current_index = -1

    @staticmethod
    def confirm_operation(new_layer_state: ImageLayer):

        if OperationHistory.current_index == len(OperationHistory.history) - 1 or len(OperationHistory.history) == 0:

            if len(OperationHistory.history) == 0:
                OperationHistory.current_index = -1

            if len(OperationHistory.history) > 0:
                current_name = OperationHistory.history[OperationHistory.current_index].layer_name
                current_pos = OperationHistory.history[OperationHistory.current_index].pos
                current_angle = OperationHistory.history[OperationHistory.current_index].angle
                current_size = OperationHistory.history[OperationHistory.current_index].size

                # Return early if no changes have been made
                if new_layer_state.are_attributes_equal(current_name, current_pos, current_angle, current_size):
                    return

            if len(OperationHistory.history) < OperationHistory.MAX_UNDO_LENGTH:
                OperationHistory.current_index += 1
            else:
                # Remove initial element for FIFO list
                OperationHistory.history.pop(0)
        else:
            iterations = (len(OperationHistory.history) - 1) - OperationHistory.current_index
            # Remove all nodes after the current one
            for i in range(iterations):
                OperationHistory.history.pop(OperationHistory.current_index + 1)

        pos = copy(new_layer_state.pos)
        angle = copy(new_layer_state.angle)
        size = copy(new_layer_state.size)
        layer_name = copy(new_layer_state.layer_name)

        OperationHistory.history.append(OperationHistoryNode(
            new_layer_state,
            pos,
            angle,
            size,
            layer_name,
        ))

        OperationHistory.current_index = len(OperationHistory.history) - 1

        if len(OperationHistory.history) > 0:
            for node in OperationHistory.history:
                print(f'Node ImageLayer Reference: pos: {node.pos}'
                      f' - angle: {node.angle}'
                      f' - size: {node.size}'
                      f' - layer name: {node.layer_name}')

            print(f'CURRENT ImageLayer: pos: {SessionGlobals.project.get_active_layer().pos}'
                  f' - angle: {SessionGlobals.project.get_active_layer().angle}'
                  f' - size: {SessionGlobals.project.get_active_layer().size}'
                  f' - layer name: {SessionGlobals.project.get_active_layer().layer_name} \n')

    @staticmethod
    def can_undo():
        return OperationHistory.current_index > 0

    @staticmethod
    def undo():
        if OperationHistory.can_undo():
            OperationHistory.execute_historical_node(OperationHistory.current_index - 1)
            SessionGlobals.layers_tab.refresh_view()

    @staticmethod
    def can_redo():
        return OperationHistory.current_index < len(OperationHistory.history) - 1

    @staticmethod
    def redo():
        if OperationHistory.can_redo():
            OperationHistory.execute_historical_node(OperationHistory.current_index + 1)
            SessionGlobals.layers_tab.refresh_view()

    @staticmethod
    def execute_historical_node(index):
        OperationHistory.current_index = index
        node = OperationHistory.history[index]
        node.layer.pos = node.pos
        node.layer.angle = node.angle
        node.layer.size = node.size
        node.layer.layer_name = node.layer_name
        node.layer.render()
        print(f'CURRENT ImageLayer: pos: {SessionGlobals.project.get_active_layer().pos}'
              f' - angle: {SessionGlobals.project.get_active_layer().angle}'
              f' - size: {SessionGlobals.project.get_active_layer().size}'
              f' - layer name: {SessionGlobals.project.get_active_layer().layer_name}')


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
    def on_touch_up(active_layer_image):
        Translate.confirm(active_layer_image)

    @staticmethod
    def confirm(active_layer_image):
        OperationHistory.confirm_operation(active_layer_image)

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
    def on_touch_up(active_layer_image):
        Rotate.confirm(active_layer_image)

    @staticmethod
    def confirm(active_layer_image):
        OperationHistory.confirm_operation(active_layer_image)

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
    def on_touch_up(active_layer_image):
        Scale.confirm(active_layer_image)

    @staticmethod
    def confirm(active_layer_image):
        OperationHistory.confirm_operation(active_layer_image)

    @staticmethod
    def cancel(active_layer_image):
        active_layer_image.size = Scale.original_size
        active_layer_image.pos = Scale.original_pos
