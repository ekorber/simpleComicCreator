from data import AppGlobals as App
from objects.ImageLayer import ImageLayer
from objects.SVGImageLayer import SVGImageLayer
from lib import GuiHandler as Gui


def add_image_file_layer(filename: str, layer_name='New Layer', parent_panel=None, insert_index=0):
    page = App.project.pages[App.current_page]
    if insert_index > len(page.layers):
        print('Error! Insert index was outside the bounds of the page\'s layers array')
        return

    page.layers.insert(insert_index, ImageLayer(filename=filename, name=layer_name, parent_panel=parent_panel))
    App.current_layer = insert_index
    page.layers[insert_index].render()


def add_panel_layer(points: [(int, int)], insert_index: int = 0, stroke_color: str = 'black', fill_color: str = 'white',
                    layer_name: str = 'Panel', stroke_width: int = 2):
    min_x = points[0][0]
    max_x = points[0][0]

    min_y = points[0][1]
    max_y = points[0][1]

    for i, p in enumerate(points):
        if p[0] > max_x:
            max_x = p[0]
        elif p[0] < min_x:
            min_x = p[0]

        if p[1] > max_y:
            max_y = p[1]
        elif p[1] < min_y:
            min_y = p[1]

    size = (max_x - min_x, max_y - min_y)

    point_array = []
    for p in points:
        point_array.append((p[0] - min_x, p[1] - min_y))

    new_points = tuple(point_array)

    page = App.project.pages[App.current_page]
    page.layers.insert(insert_index,
                       SVGImageLayer(name=layer_name, points=new_points, position=(min_x, min_y), size=size,
                                     stroke_color=stroke_color, fill_color=fill_color, stroke_width=stroke_width))
    App.current_layer = insert_index
    page.layers[insert_index].render()


def delete_layer(index: int):
    layers = App.project.pages[App.current_page].layers
    for layer in layers:
        if layer.parent_panel and (layer.parent_panel.id == layers[index].id):
            layer.parent_panel = None

    Gui.delete_layer(App.project.pages[App.current_page].layers[index].id)
    App.project.pages[App.current_page].layers.pop(index)
    re_render_page()

    if App.current_layer > 0 and App.current_layer == len(layers):
        App.current_layer -= 1


def move_layer_to_new_index(current: int, new: int):
    # If the 'new' layer index is no different
    if current == new:
        return

    # If the 'new' layer index is negative
    if current == 0 and new < current:
        return

    page = App.project.pages[App.current_page]

    # If the 'new' layer index is greater than the scope of the array
    if current == len(page.layers) - 1 and new > current:
        return

    if new >= len(page.layers):
        return

    # Re-position the z-order of the layer in question
    if new > current:
        Gui.lower_tag(page.layers[current].id, page.layers[new].id)
    else:
        Gui.raise_tag(page.layers[current].id, page.layers[new].id)

    # Re-arrange the actual layers array for this page, to reflect the new z-order
    layer = page.layers[current]
    page.layers.pop(current)
    page.layers.insert(new, layer)

    # Keep the layer in question selected, even after the re-arrangement
    App.current_layer = new


def re_render_page():
    for layer in reversed(App.project.pages[App.current_page].layers):
        Gui.delete_layer(layer.id)
        layer.render()
