from kivy.uix.floatlayout import FloatLayout
from ops.InputListener import InputListener
import layouts.tabs.EditorTab
import layouts.tabs.ToolOptionsTab
import layouts.tabs.LayersTab
import layouts.widgets.OperationButtonsListWidget
import layouts.widgets.PageNavigationWidget


class Workspace(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(InputListener())
