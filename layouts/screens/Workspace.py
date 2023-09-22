from kivy.uix.floatlayout import FloatLayout
import layouts.tabs.EditorTab
import layouts.tabs.ToolOptionsTab
import layouts.tabs.LayersTab
import layouts.widgets.OperationButtonsListWidget
import layouts.widgets.PageNavigationWidget
from utils.InputListener import InputListener


class Workspace(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(InputListener())
