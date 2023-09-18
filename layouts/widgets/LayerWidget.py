from kivy.properties import ObjectProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout

from data import SessionGlobals


class LayerWidget(BoxLayout):
    disable_touch_events = False
    layer_name_input = ObjectProperty(None)
    delete_button = ObjectProperty(None)
    bg_color = ColorProperty([0, 0, 0.6])
    text_input_bg_color = ColorProperty([0.4, 0.4, 0.4])
    text_input_fg_color = ColorProperty([0.75, 0.75, 0.75])

    def __init__(self, index: int, layers_tab, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.layers_tab = layers_tab
        self.layer_name_input.text = SessionGlobals.layer_collection.get_layer_at_index(self.index).layer_name

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        if self.collide_point(x=touch.pos[0], y=touch.pos[1])\
                and not self.delete_button.collide_point(x=touch.pos[0], y=touch.pos[1]):
            self.layers_tab.select_layer(self.index)

    def set_selected(self, value: bool):
        if value:
            self.bg_color = [0, 0, 0.9]
        else:
            self.bg_color = [0, 0, 0.6]

    def on_delete_click(self):
        self.disable_touch_events = True
        self.layers_tab.delete_layer(self.index)

    def on_focus_changed(self, value: bool):
        if value:
            self.text_input_bg_color = [1, 1, 1]
            self.text_input_fg_color = [0.2, 0.2, 0.2]
        else:
            self.text_input_bg_color = [0.4, 0.4, 0.4]
            self.text_input_fg_color = [0.75, 0.75, 0.75]

            # Prevent empty layer name
            stripped_input = self.layer_name_input.text.strip()
            if stripped_input:
                SessionGlobals.layer_collection.get_layer_at_index(self.index).layer_name = stripped_input
            else:
                SessionGlobals.layer_collection.get_layer_at_index(self.index).layer_name = 'Layer'

            self.layer_name_input.text = self.layer_name_input.text\
                = SessionGlobals.layer_collection.get_layer_at_index(self.index).layer_name
