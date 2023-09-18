from kivy.graphics import Color, Rectangle, Rotate, PushMatrix, PopMatrix
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class ImageLayer(Widget):
    def __init__(self, image_src: str, pos: (int, int), **kwargs):
        super().__init__(**kwargs)
        self.layer_name = 'New Layer'
        self.page = 0
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


class LayerCollection:
    def __init__(self):
        self.layers = []
        self.active_layer = 0

    def get_active_layer(self):
        return self.layers[self.active_layer]

    def get_layer_of_index(self, index: int):
        if 0 <= index < len(self.layers):
            return self.layers[index]
        else:
            return None

    def add_layer(self, image_layer: ImageLayer):
        self.layers.append(image_layer)
        self.active_layer = len(self.layers) - 1
        return self.layers.index(image_layer)

    def add_layer_at_index(self, image_layer: ImageLayer, index: int):
        self.layers.insert(index, image_layer)
        self.active_layer = index

    def delete_layer_at_index(self, index: int):
        if self.active_layer >= index:
            self.active_layer -= 1

        if self.active_layer < 0:
            self.active_layer = 0

        self.layers.pop(index)

    def move_current_layer_up(self, n=1):
        self.move_current_layer_to_new_index(self.active_layer + n)

    def move_current_layer_down(self, n=1):
        self.move_current_layer_to_new_index(self.active_layer - n)

    def move_current_layer_to_new_index(self, new: int):
        # If the 'new' layer index is no different
        if self.active_layer == new:
            return

        # If the 'new' layer index is negative
        if self.active_layer == 0 and new < self.active_layer:
            return

        # If the 'new' layer index is greater than the scope of the array
        if self.active_layer == len(self.layers) - 1 and new > self.active_layer:
            return

        if new >= len(self.layers):
            return

        # Re-arrange the actual layers array for this page, to reflect the new z-order
        layer = self.get_active_layer()
        self.delete_layer_at_index(self.active_layer)
        self.add_layer_at_index(layer, new)

