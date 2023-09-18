from PIL import ImageTk, Image
from data import AppGlobals as App
from enum import Enum
import numpy as np
from lib import GuiHandler as Gui


class LayerType(Enum):
    IMAGE = 0
    PANEL = 1
    TEXT_BUBBLE = 2


class ImageLayer:

    def __init__(self, name: str, position: tuple[int, int] = None, size: tuple[int, int] = (0, 0),
                 layer_type: LayerType = LayerType.IMAGE, filename: str = None, parent_panel=None):
        self.id = None
        self.layer_type = layer_type
        self.name = name
        if not position:
            position = (int(App.project.page_width * 0.5), int(App.project.page_height * 0.5))
        self.x = position[0]
        self.y = position[1]
        self.selected = False
        self.parent_panel = parent_panel
        self.filename = None
        self.image = None
        self.masked_image = None
        self.width = size[0]
        self.height = size[1]
        if filename:
            self.create_image(filename)

    def create_image(self, filename: str):
        self.filename = filename
        self.image = ImageTk.PhotoImage(Image.open(self.filename))
        self.width = self.image.width()
        self.height = self.image.height()

    def create_masked_image(self):
        image = Image.open(self.filename)
        numpy_image = np.array(image)

        # parent_image = Image.open(self.parent_panel.filename)
        # parent_numpy_image = np.array(parent_image)

        x_dist = self.x - self.parent_panel.x
        y_dist = self.y - self.parent_panel.y

        overlap_area = self.get_overlap_size(self.parent_panel)

        # Show pixels that have Alpha > 100
        masked_pixels = numpy_image[:, :, 3] > 100

        # Hide pixels that are outside the overlapping zone, between this image and its parent
        if overlap_area:
            if x_dist >= 0:
                masked_pixels[:, overlap_area[0]:] = False
            else:
                masked_pixels[:, :self.width - overlap_area[0]] = False

            if y_dist >= 0:
                masked_pixels[overlap_area[1]:, :] = False
            else:
                masked_pixels[:self.height - overlap_area[1], :] = False
        else:
            masked_pixels[:, :] = False

        # Apply mask
        masked_image = Image.open(self.filename)
        masked_image.putalpha(Image.fromarray(masked_pixels))
        self.masked_image = ImageTk.PhotoImage(masked_image)

        # mask = Image.new(1, (self.image.width(), self.image.height()), 0)
        # draw = Draw(mask)

        # points = []
        # for p in self.parent_panel.points:
        #     points.append((p[0], p[1]))

        # draw.polygon(xy=self.parent_panel.points, width=self.parent_panel.stroke_width, fill=1, outline=0)

    def get_overlap_size(self, other_layer):  # returns None if rectangles don't intersect
        dx = min(self.x + int(self.width * 0.5), other_layer.x + int(other_layer.width * 0.5)) \
             - max(self.x - int(self.width * 0.5), other_layer.x - int(other_layer.width * 0.5))
        dy = min(self.y + int(self.height * 0.5), other_layer.y + int(other_layer.height * 0.5)) \
             - max(self.y - int(self.height * 0.5), other_layer.y - int(other_layer.height * 0.5))

        if (dx > 0) and (dy > 0):
            return dx, dy

    def render(self):
        if self.parent_panel:
            self.create_masked_image()
            self.id = Gui.create_image(self.x, self.y, image=self.masked_image)
        else:
            self.id = Gui.create_image(self.x, self.y, image=self.image)

    def render_at(self, x: int, y: int):
        self.x = x
        self.y = y

        if self.masked_image:
            self.id = Gui.create_image(self.x, self.y, image=self.masked_image)
        else:
            self.id = Gui.create_image(self.x, self.y, image=self.image)

    def re_render(self):
        if self.parent_panel:
            self.create_masked_image()
            self.id = Gui.create_image(self.x, self.y, image=self.masked_image)
        else:
            self.id = Gui.create_image(self.x, self.y, image=self.image)

    def set_position(self, new_x: int, new_y: int):
        Gui.move(self.id, new_x - self.x, new_y - self.y)
        self.x = new_x
        self.y = new_y
        if self.parent_panel:
            self.create_masked_image()

    def translate(self, x_offset: int, y_offset: int):
        Gui.move(self.id, x_offset, y_offset)
        self.x += x_offset
        self.y += y_offset
        if self.parent_panel:
            self.create_masked_image()
