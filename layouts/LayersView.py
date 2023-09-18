from tkinter import Frame, Button
from data import AppGlobals as App
from objects.ImageLayer import LayerType
from utils.LayerUtils import add_image_file_layer, add_panel_layer, delete_layer, move_layer_to_new_index
import lib.GuiHandler as Gui


def initialize_layers_view(master):
    layers_frame = Gui.create_frame(master, bg_color='red', pad_x=10, pad_y=10)
    Gui.pack_widget(layers_frame, fill='both', side='right')
    display_initial_widgets(layers_frame)


def add_image_layer_btn_pressed(frame: Frame):
    filepath = Gui.open_image_file()

    if filepath:
        add_image_file_layer(filename=filepath, layer_name='Image')
        refresh_layers_tab(frame)


def add_image_layer_to_panel(frame: Frame):
    current_page = App.project.pages[App.current_page]

    if len(current_page.layers) == 0 or current_page.layers[App.current_layer].layer_type != LayerType.PANEL:
        return

    current_layer = current_page.layers[App.current_layer]

    filepath = Gui.open_image_file()

    if filepath:
        add_image_file_layer(filename=filepath, layer_name='Image', parent_panel=current_layer)
        refresh_layers_tab(frame)


def add_panel_layer_btn_pressed(frame: Frame):
    default_points = [(180, 270), (250, 270), (250, 500), (180, 500)]
    add_panel_layer(points=default_points)
    refresh_layers_tab(frame)


def move_layer_up(frame: Frame):
    cur = App.current_layer
    move_layer_to_new_index(cur, cur - 1)
    refresh_layers_tab(frame)


def move_layer_down(frame: Frame):
    cur = App.current_layer
    move_layer_to_new_index(cur, cur + 1)
    refresh_layers_tab(frame)


def delete_layer_btn_pressed(frame: Frame):
    page = App.project.pages[App.current_page]

    if len(page.layers) > 0:
        delete_layer(App.current_layer)
        refresh_layers_tab(frame)


def select_layer(i: int, frame: Frame):
    App.current_layer = i
    refresh_layers_tab(frame)


def refresh_layers_tab(frame: Frame):
    for widget in frame.winfo_children():
        widget.destroy()

    display_initial_widgets(frame)

    for i, obj in enumerate(App.project.pages[App.current_page].layers):
        color = 'white'
        if i == App.current_layer:
            color = 'blue'
        elif obj.layer_type == LayerType.PANEL:
            color = 'green'
        elif obj.layer_type == LayerType.TEXT_BUBBLE:
            color = 'red'

        Button(frame, text=obj.name, bg=color, command=lambda index=i: select_layer(index, frame)).pack()


def display_initial_widgets(frame: Frame):
    Gui.create_label(frame, 'Layers').pack()
    Button(frame, text='Add Image Layer', command=lambda: add_image_layer_btn_pressed(frame)).pack()
    Button(frame, text='Add Image To Panel', command=lambda: add_image_layer_to_panel(frame)).pack()
    Button(frame, text='Add Panel Layer', command=lambda: add_panel_layer_btn_pressed(frame)).pack()
    Button(frame, text='Delete Layer', command=lambda: delete_layer_btn_pressed(frame)).pack()
    Button(frame, text='Move Layer Up', command=lambda: move_layer_up(frame)).pack()
    Button(frame, text='Move Layer Down', command=lambda: move_layer_down(frame)).pack()
