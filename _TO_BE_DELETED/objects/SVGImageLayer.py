from toBeDeleted.objects.ImageLayer import ImageLayer, LayerType
from matplotlib.colors import to_rgb
from time import time
import cairo


class SVGImageLayer(ImageLayer):

    def __init__(self, name: str, points: [(int, int)], position: tuple[int, int], size: tuple[int, int],
                 stroke_width: int = 2, stroke_color: str = 'black', fill_color: str = 'white'):

        super().__init__(name=name, layer_type=LayerType.PANEL, position=position, size=size)
        self.points = points
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.generate_polyline_image(size)

    def generate_polyline_image(self, size: tuple[int, int]):

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size[0], size[1])
        ctx = cairo.Context(surface)

        ctx.set_line_width(self.stroke_width)

        # Go to start position
        ctx.move_to(self.points[0][0], self.points[0][1])

        # Loop through all points, and render as lines
        for i, p in enumerate(self.points):
            if i > 0:
                ctx.line_to(p[0], p[1])

        # Close the shape
        ctx.close_path()

        # Apply fill colour
        fill = to_rgb(self.fill_color)
        ctx.set_source_rgb(fill[0], fill[1], fill[2])
        ctx.fill_preserve()

        # Apply stroke colour
        stroke = to_rgb(self.stroke_color)
        ctx.set_source_rgb(stroke[0], stroke[1], stroke[2])
        ctx.stroke()

        # Create png file from svg
        filename = str(f'img\\Panel_{time()}.png')
        surface.write_to_png(filename)
        super().create_image(filename)
