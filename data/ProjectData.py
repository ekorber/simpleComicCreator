from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from math import ceil
import json

from data import SessionGlobals


class ImageLayer(Widget):
    def __init__(self, image_src: str = '', pos: (int, int) = (100, 100), **kwargs):
        super().__init__(**kwargs)
        self.layer_name = 'New Layer'
        self.pos = pos
        self.image = Image(source=str(image_src))
        self.size = self.image.texture_size
        self.color = (1, 1, 1, 1)
        self.angle = 0

    def as_dict(self) -> dict:
        return {
            'layer_name': self.layer_name,
            'pos': self.pos,
            'image_src': self.image.source,
            'size': self.size,
            'color': self.color,
            'angle': self.angle,
        }

    def load_values(self, data: dict):
        self.layer_name = data['layer_name']
        self.pos = data['pos']
        self.image = Image(source=data['image_src'])
        self.size = data['size']
        self.color = data['color']
        self.angle = data['angle']

    def render(self):
        with self.canvas:
            self.canvas.clear()
            PushMatrix()
            Rotate(angle=self.angle, origin=(self.pos[0] + (self.size[0] / 2), self.pos[1] + (self.size[1] / 2)))
            Color(self.color[0], self.color[1], self.color[2], self.color[3], mode='rgba')
            Rectangle(pos=self.pos, size=self.size, texture=self.image.texture)
            PopMatrix()

    def are_attributes_equal(self, name, pos, angle, size):
        return self.layer_name == name and self.pos == pos and self.angle == angle and self.size == size


class PageBackground(Widget):
    def __init__(self, pos: (int, int), size: (int, int), color: (float, float, float) = (1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
        self.color = color
        self.render()

    def as_dict(self) -> dict:
        return {
            'pos': self.pos,
            'size': self.size,
            'color': self.color,
        }

    def load_values(self, data: dict):
        self.pos = data['pos']
        self.size = data['size']
        self.color = data['color']

    def render(self):
        with self.canvas:
            self.canvas.clear()
            PushMatrix()
            Color(self.color[0], self.color[1], self.color[2], 1, mode='rgba')
            Rectangle(pos=self.pos, size=self.size)
            PopMatrix()


class PageData:
    def __init__(self, page_size: (int, int)):
        self.layers: [ImageLayer] = []
        self.page_background = PageBackground(pos=(100, 100), size=page_size)
        self.active_layer_index: int = 0

    def as_dict(self) -> dict:
        layer_dictionaries = []
        for layer in self.layers:
            layer_dictionaries.append(layer.as_dict())

        return {
            'layers': layer_dictionaries,
            'page_background': self.page_background.as_dict(),
            'active_layer_index': self.active_layer_index,
        }

    def load_values(self, data: dict):
        self.layers = []
        index = 0
        for layer in data['layers']:
            self.layers.append(ImageLayer())
            self.layers[index].load_values(layer)
            index += 1

        self.page_background.load_values(data['page_background'])
        self.active_layer_index = data['active_layer_index']

    def get_active_layer(self) -> ImageLayer:
        return self.layers[self.active_layer_index]

    def get_layer_at_index(self, index: int) -> ImageLayer:
        if 0 <= index < len(self.layers):
            return self.layers[index]
        else:
            return None

    def add_layer(self, image_layer: ImageLayer):
        self.layers.append(image_layer)
        self.active_layer_index = len(self.layers) - 1

    def add_layer_at_index(self, image_layer: ImageLayer, index: int):
        self.layers.insert(index, image_layer)
        self.active_layer_index = index

    def delete_layer_at_index(self, index: int):
        if self.active_layer_index >= index:
            self.active_layer_index -= 1

        if self.active_layer_index < 0:
            self.active_layer_index = 0

        self.layers.pop(index)

    def move_current_layer_up(self, n=1):
        self.move_current_layer_to_new_index(self.active_layer_index + n)

    def move_current_layer_down(self, n=1):
        self.move_current_layer_to_new_index(self.active_layer_index - n)

    def move_current_layer_to_new_index(self, new: int):
        # If the 'new' layer index is no different
        if self.active_layer_index == new:
            return

        # If the 'new' layer index is negative
        if self.active_layer_index == 0 and new < self.active_layer_index:
            return

        # If the 'new' layer index is greater than the scope of the array
        if self.active_layer_index == len(self.layers) - 1 \
                and new > self.active_layer_index:
            return

        if new >= len(self.layers):
            return

        # Re-arrange the actual layers array for this page, to reflect the new z-order
        layer = self.get_active_layer()
        self.delete_layer_at_index(self.active_layer_index)
        self.add_layer_at_index(layer, new)


class ProjectData:
    def __init__(self, dpi: int = 100, size_in_inches: (float, float) = (6.875, 10.438)):
        self.dpi = dpi
        self.size_in_inches = size_in_inches
        self.size_in_pixels = (ceil(self.size_in_inches[0] * self.dpi), ceil(self.size_in_inches[1] * self.dpi))
        self.file_path = None
        self.pages: [PageData] = [PageData(page_size=self.size_in_pixels)]
        self.current_page_index = 0

    def as_dict(self) -> dict:
        page_dictionaries = []
        for page in self.pages:
            page_dictionaries.append(page.as_dict())

        return {
            'dpi': self.dpi,
            'size_in_inches': self.size_in_inches,
            'size_in_pixels': self.size_in_pixels,
            'pages': page_dictionaries,
            'current_page_index': self.current_page_index,
        }

    def load_values(self, data: dict):
        self.dpi = data['dpi']
        self.size_in_inches = data['size_in_inches']
        self.size_in_pixels = data['size_in_pixels']

        self.pages = []
        index = 0
        for page in data['pages']:
            self.pages.append(PageData(page_size=self.size_in_pixels))
            self.pages[index].load_values(page)
            index += 1

        self.current_page_index = data['current_page_index']

    def to_json(self):
        return json.dumps(self.as_dict(), indent=4)

    def save_data_to_file(self, save_as: bool = False):
        if not self.file_path or save_as:
            path = SessionGlobals.file_handler.pick_save_file_location()
            if path:
                self.file_path = path + f'.{SessionGlobals.PROJECT_FILE_EXTENSION}'
            else:
                return

        # Save data
        with open(self.file_path, 'w') as save_file:
            save_file.write(self.to_json())

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as save_file:
            save_data = json.load(save_file)
            self.load_values(save_data)
            self.file_path = file_path

    def get_current_page(self) -> PageData:
        return self.pages[self.current_page_index]

    def get_total_pages(self) -> int:
        return len(self.pages)

    def add_new_page(self, index: int):
        self.pages.insert(index, PageData(page_size=self.size_in_pixels))
        self.current_page_index = index

    def delete_page(self, index: int):
        self.pages.remove(self.pages[index])

        if self.current_page_index == self.get_total_pages():
            self.current_page_index -= 1

    def get_active_layer(self) -> ImageLayer:
        return self.get_current_page().get_active_layer()

    def get_active_layer_index(self) -> int:
        return self.get_current_page().active_layer_index

    def get_layer_at_index(self, index: int) -> ImageLayer:
        return self.get_current_page().get_layer_at_index(index)

    def add_layer(self, image_layer: ImageLayer):
        self.get_current_page().add_layer(image_layer)

    def add_layer_at_index(self, image_layer: ImageLayer, index: int):
        self.get_current_page().add_layer_at_index(image_layer, index)

    def delete_layer_at_index(self, index: int):
        self.get_current_page().delete_layer_at_index(index)

    def move_current_layer_up(self, n=1):
        self.get_current_page().move_current_layer_up(n)

    def move_current_layer_down(self, n=1):
        self.get_current_page().move_current_layer_down(n)

    def move_current_layer_to_new_index(self, new: int):
        self.get_current_page().move_current_layer_to_new_index(new)
