import os

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

import ops.Operations
from data import SessionGlobals
from layouts.widgets.LayerWidget import LayerWidget


class LayersTab(BoxLayout):
    layers_area = ObjectProperty(None)
    popup_window: Popup = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.layers_tab = self

    def move_layer_up(self):
        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()
        SessionGlobals.project.move_current_layer_up()
        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.project.get_active_layer_index())

    def move_layer_down(self):
        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()
        SessionGlobals.project.move_current_layer_down()
        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.project.get_active_layer_index())

    def on_new_image_layer(self):
        SessionGlobals.file_handler.import_image()

    def select_layer(self, index: int):
        SessionGlobals.project.get_current_page().active_layer_index = index
        for layer in self.ids.layers_area.children:
            layer.set_selected(layer.index is index)

    def delete_layer(self, index: int):
        new_history = []
        for node in ops.Operations.OperationHistory.history:
            if node.layer != SessionGlobals.project.get_layer_at_index(index):
                new_history.append(node)

        ops.Operations.OperationHistory.history = new_history

        SessionGlobals.editor.clear_screen()
        self.clear_layers_tab()

        SessionGlobals.project.delete_layer_at_index(index)

        SessionGlobals.editor.populate_screen()
        self.populate_layers_tab()

        self.select_layer(SessionGlobals.project.get_active_layer_index())

    def refresh_view(self):
        self.clear_layers_tab()
        self.populate_layers_tab()
        self.select_layer(SessionGlobals.project.get_active_layer_index())

    def clear_layers_tab(self):
        for index in range(len(SessionGlobals.project.get_current_page().layers)):
            for child in self.ids.layers_area.children:
                if child.index == index:
                    self.ids.layers_area.remove_widget(child)

    def populate_layers_tab(self):
        for index in reversed(range(len(SessionGlobals.project.get_current_page().layers))):
            widget = LayerWidget(index=index, layers_tab=self)
            name = SessionGlobals.project.get_layer_at_index(index).layer_name
            widget.layer_name_input.text = name
            self.ids.layers_area.add_widget(widget)
