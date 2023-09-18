from data import AppGlobals as App
from Operations.Translate import Translate
import lib.GuiHandler as Gui


def initialize_editor_view(master):
    Gui.create_canvas(master, '#919192')
    Gui.pack_widget(Gui.canvas, expand=1, fill='both')
    Gui.create_rect(100, 100, App.project.page_width, App.project.page_height,
                    fill_color=App.project.pages[App.current_page].background_color, stroke_width=0)

    Translate().register('<Button-1>')

#     App.canvas.bind('<Button-1>', start_command)
#     App.canvas.bind('<Motion>', command_engaged)
#     App.canvas.bind('<ButtonRelease-1>', stop_command)
#
#
# def start_command():
#     if not page_and_layer_in_bounds():
#         # print(f'Page or Layer out of bounds at start command! '
#         #      f'Page: {App.current_page}, Layer: {App.current_layer}')
#         return
#     App.project.pages[App.current_page].layers[App.current_layer].selected = True
#
#
# def command_engaged(e):
#     if not page_and_layer_in_bounds():
#         # print(f'Page or Layer out of bounds at mouse motion! '
#         #      f'Page: {App.current_page}, Layer: {App.current_layer}')
#         return
#
#     global canvas_mouse_last_x
#     global canvas_mouse_last_y
#
#     # If selected, then translate
#     current_page = App.project.pages[App.current_page]
#     current_layer = current_page.layers[App.current_layer]
#
#     if current_layer.selected:
#         current_layer.translate(e.x - canvas_mouse_last_x, e.y - canvas_mouse_last_y)
#         #re_render_page()
#
#     canvas_mouse_last_x = e.x
#     canvas_mouse_last_y = e.y
#
#
# def stop_command():
#     if not page_and_layer_in_bounds():
#         # print(f'Page or Layer out of bounds at stop command! '
#         #      f'Page: {App.current_page}, Layer: {App.current_layer}')
#         return
#     App.project.pages[App.current_page].layers[App.current_layer].selected = False
