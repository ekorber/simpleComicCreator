from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from math import ceil


class ImageLayer(Widget):
    def __init__(self, image_src: str, pos: (int, int), **kwargs):
        super().__init__(**kwargs)
        self.layer_name = 'New Layer'
        self.pos = pos
        self.image = Image(source=str(image_src))
        self.size = self.image.texture_size
        self.color = (1, 1, 1, 1)
        self.angle = 0
        self.render()

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
    def __init__(self, dpi: int = 100, size_in_inches: (float, float) = (6.875, 10.438), file_name: str = '', file_path: str = ''):
        self.dpi = dpi
        self.size_in_inches = size_in_inches
        self.size_in_pixels = (ceil(self.size_in_inches[0] * self.dpi), ceil(self.size_in_inches[1] * self.dpi))
        self.file_name = file_name
        self.file_path = file_path
        self.pages: [PageData] = [PageData(page_size=self.size_in_pixels)]
        self.current_page_index = 0

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

    def save_data_to_file(self):
        if not self.file_path:
            # Save as new project file
            self.save_as_new_file()
        else:
            # Save to existing file
            print('save to existing file')

    def save_as_new_file(self):
        print('save as new file')

    def load_from_file(self):
        pass

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
