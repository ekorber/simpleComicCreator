from Operations.Operator import Operator, can_operator_begin, page_and_layer_in_bounds
from data import AppGlobals as App
from utils.LayerUtils import re_render_page


class Translate(Operator):

    def __init__(self):
        self.engaged = False
        self.start_x = 0
        self.start_y = 0

    def begin(self):
        if not can_operator_begin():
            return

        if not self.engaged:
            print('Translation begun!')
            self.engaged = True
            self.start_x = App.project.pages[App.current_page].layers[App.current_layer].x
            self.start_y = App.project.pages[App.current_page].layers[App.current_layer].y
            print(f'Started at X:{self.start_x} and Y:{self.start_y}')

    def update_loop(self):
        pass

    def mouse_movement(self, e):
        if not self.engaged:
            return

        if not page_and_layer_in_bounds():
            return

        print(e)

        current_page = App.project.pages[App.current_page]
        current_layer = current_page.layers[App.current_layer]

        current_layer.translate(e.x - App.canvas_mouse_last_x, e.y - App.canvas_mouse_last_y)
        re_render_page()

        App.canvas_mouse_last_x = e.x
        App.canvas_mouse_last_y = e.y

    def apply(self):
        if self.engaged:
            print('Apply!')
            self.engaged = False

    def cancel(self):
        if self.engaged:
            print('Cancel!')
            self.engaged = False
            App.project.pages[App.current_page].layers[App.current_layer].x = self.start_x
            App.project.pages[App.current_page].layers[App.current_layer].y = self.start_y
            print(f'Start X:{App.project.pages[App.current_page].layers[App.current_layer].x}, '
                  f'Y:{App.project.pages[App.current_page].layers[App.current_layer].y}')
