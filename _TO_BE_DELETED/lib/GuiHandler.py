from tkinter import Tk, Canvas, filedialog, Frame, Label
from typing import Literal

canvas: Canvas


def create_window(width: int, height: int, title: str):
    window = Tk()
    window.geometry(f"{width}x{height}")
    window.title(title)
    return window


def create_canvas(master, bg_color: str):
    global canvas
    canvas = Canvas(master, bg=bg_color)


def create_image(x: int, y: int, image):
    return canvas.create_image(x, y, image=image)


def create_rect(x0: int, y0: int, x1: int, y1: int, fill_color: str, stroke_width: int, stroke_color: str = 'black'):
    canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline=stroke_color, width=stroke_width)


def create_frame(master, bg_color: str, pad_x=10, pad_y=10):
    return Frame(master, bg=bg_color, padx=pad_x, pady=pad_y)


def create_label(master, text):
    return Label(master, text=text)


def pack_widget(widget, expand: int = 1, fill: Literal["none", "x", "y", "both"] = 'both',
                side: Literal["left", "right", "top", "bottom"] = 'left'):
    widget.pack(expand=expand, fill=fill, side=side)


def open_image_file():
    return filedialog.askopenfilename(title='Select An Image',
                                      filetypes=(('Image Files (.png, .jpg)', ['*.png', '*.jpg']),))


def move(layer_id: int, x: int, y: int):
    canvas.move(layer_id, x, y)


def raise_tag(first: int, second: int):
    canvas.tag_raise(first, second)


def lower_tag(first: int, second: int):
    canvas.tag_lower(first, second)


def delete_layer(layer_id: int):
    canvas.delete(layer_id)
