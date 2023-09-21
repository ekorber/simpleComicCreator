import os

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import ops.Operations
from data import SessionGlobals
from layouts.widgets.FileChooserWidget import FileChooserWidget
from layouts.widgets.LayerWidget import LayerWidget
from objects.LayerCollection import ImageLayer


class LayersTab(BoxLayout):
    layers_area = ObjectProperty(None)
    popup_window: Popup = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.layers_tab = self

    def dismiss_popup(self):
        self.popup_window.dismiss()

    def move_layer_up(self):
        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()
        SessionGlobals.layer_collection.move_current_layer_up()
        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def move_layer_down(self):
        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()
        SessionGlobals.layer_collection.move_current_layer_down()
        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def on_new_image_layer(self):
        content = FileChooserWidget(open_file=self.display_selected_image, cancel=self.dismiss_popup)
        self.popup_window = Popup(title="Select image", content=content,
                                  size_hint=(0.9, 0.9))
        self.popup_window.open()

    def display_selected_image(self, path, filename):
        self.popup_window.dismiss()

        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()

        SessionGlobals.layer_collection.add_layer(
            ImageLayer(os.path.join(path, filename[0]), (300, 600)))

        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()

        ops.Operations.OperationHistory.confirm_operation(SessionGlobals.layer_collection.get_active_layer())
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def select_layer(self, index: int):
        SessionGlobals.layer_collection.active_layer = index
        for layer in self.ids.layers_area.children:
            layer.set_selected(layer.index is index)

    def delete_layer(self, index: int):
        new_history = []
        for node in ops.Operations.OperationHistory.history:
            if node.layer != SessionGlobals.layer_collection.get_layer_at_index(index):
                new_history.append(node)
        ops.Operations.OperationHistory.history = new_history

        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()

        SessionGlobals.layer_collection.delete_layer_at_index(index)

        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()

        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def refresh_view(self):
        self.clear_layers_tab()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.layer_collection.active_layer)

    def clear_layers_tab(self):
        for index in range(len(SessionGlobals.layer_collection.layers)):
            for child in self.ids.layers_area.children:
                if child.index == index:
                    self.ids.layers_area.remove_widget(child)

    def populate_layers_tab(self):
        for index in reversed(range(len(SessionGlobals.layer_collection.layers))):
            widget = LayerWidget(index=index, layers_tab=self)
            name = SessionGlobals.layer_collection.get_layer_at_index(index).layer_name
            widget.layer_name_input.text = name
            self.ids.layers_area.add_widget(widget)