import os
from typing import List

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from data import SessionGlobals
from layouts.widgets.FileChooserWidget import FileChooserWidget
from layouts.widgets.LayerWidget import LayerWidget
from objects.LayerCollection import ImageLayer


class LayersTab(BoxLayout):
    layers_area = ObjectProperty(None)
    layer_widgets: List[LayerWidget] = []
    popup_window: Popup = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.layers_tab = self

    def dismiss_popup(self):
        self.popup_window.dismiss()

    def on_new_image_layer(self):
        content = FileChooserWidget(open_file=self.display_selected_image, cancel=self.dismiss_popup)
        self.popup_window = Popup(title="Select image", content=content,
                                  size_hint=(0.9, 0.9))
        self.popup_window.open()

    def move_layer_up(self):
        SessionGlobals.editor.clear_screen()
        SessionGlobals.layer_collection.move_current_layer_up()
        SessionGlobals.editor.populate_screen()
        self.clear_layers_tab()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def move_layer_down(self):
        SessionGlobals.editor.clear_screen()
        SessionGlobals.layer_collection.move_current_layer_down()
        SessionGlobals.editor.populate_screen()
        self.clear_layers_tab()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def display_selected_image(self, path, filename):
        self.popup_window.dismiss()
        SessionGlobals.editor.clear_screen()
        index = SessionGlobals.layer_collection.add_layer(
            ImageLayer(os.path.join(path, filename[0]), (300, 600)))
        SessionGlobals.editor.populate_screen()
        self.clear_layers_tab()
        self.layer_widgets.append(LayerWidget(index=index, layers_tab=self))
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def select_layer(self, index: int):
        SessionGlobals.layer_collection.active_layer = index
        for layer in self.layer_widgets:
            layer.set_selected(layer.index is index)

    def delete_layer(self, index: int):
        SessionGlobals.editor.clear_screen()
        SessionGlobals.layer_collection.delete_layer_at_index(index)
        SessionGlobals.editor.populate_screen()
        self.clear_layers_tab()
        self.layer_widgets.pop(index)
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def clear_layers_tab(self):
        for layer in self.layer_widgets:
            self.ids.layers_area.remove_widget(layer)

    def populate_layers_tab(self):
        for i in reversed(range(len(self.layer_widgets))):
            self.layer_widgets[i].index = i
            self.layer_widgets[i].layer_name_input.text\
                = SessionGlobals.layer_collection.get_layer_at_index(i).layer_name
            self.ids.layers_area.add_widget(self.layer_widgets[i])
