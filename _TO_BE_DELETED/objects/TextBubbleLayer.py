from toBeDeleted.objects.ImageLayer import ImageLayer, LayerType
from matplotlib.colors import to_rgb
from toBeDeleted import AppGlobals as App
import time
import cairo


class TextBubbleImageLayer(ImageLayer):

    def __init__(self, filename: str, name: str, parent_layer: ImageLayer, points, stroke_width: int = 2,
                 stroke_color: str = 'black', fill_color: str = 'white'):

        super().__init__(name=name, layer_type=LayerType.TEXT_BUBBLE, parent_layer=parent_layer)
        self.points = points
        self.stroke_width = stroke_width
        self.stroke_color = stroke_color
        self.fill_color = fill_color

    def generate_speech_bubble(self, bubble_bounds: tuple[int, int, int, int], pointer_start: tuple[int, int],
                               pointer_tip: tuple[int, int], pointer_end: tuple[int, int]):

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, App.project.page_width, App.project.page_height)
        ctx = cairo.Context(surface)

        ctx.set_line_width(self.stroke_width)

        ctx.move_to(self.points[0][0], self.points[0][1])
        for i, p in enumerate(self.points):
            if i > 0:
                ctx.line_to(p[0], p[1])

        ctx.close_path()

        fc = to_rgb(self.fill_color)
        sc = to_rgb(self.stroke_color)

        ctx.set_source_rgb(fc[0], fc[1], fc[2])
        ctx.fill_preserve()
        ctx.set_source_rgb(sc[0], sc[1], sc[2])
        ctx.stroke()

        filename = str(f'img\\Panel_{time.time()}.png')
        surface.write_to_png(filename)
        super().create_image(filename)

        # x0 = 10
        # y0 = 10
        # x1 = 150
        # y1 = 80
        # outline_width = 2
        # fill_color = 'white'
        # outline_color = 'black'
        #
        # bubble_pointer_tip_rel_pos = (100, 110)
        # bubble_pointer_start_rel_pos = (40, 30)
        # bubble_pointer_end_rel_pos = (90, 30)
        #
        # # Add the x,y position values to the bubble pointer values
        #
        # id_0 = App.canvas.create_oval(x0, y0, x1, y1, fill=outline_color)
        # id_1 = App.canvas.create_polygon([bubble_pointer_start_rel_pos, bubble_pointer_tip_rel_pos,
        #                                   bubble_pointer_end_rel_pos], fill=fill_color, outline=outline_color,
        #                                  width=outline_width)
        # id_2 = App.canvas.create_oval(x0 + outline_width, y0 + outline_width, x1 - outline_width, y1 - outline_width,
        #                               fill=fill_color, width=0)
