from kivy.uix.floatlayout import FloatLayout

from data import SessionGlobals
from data.ProjectData import ProjectData
from ops.FileHandler import FileHandler
from ops.InputListener import InputListener
import layouts.tabs.EditorTab
import layouts.tabs.ToolOptionsTab
import layouts.tabs.LayersTab
import layouts.widgets.OperationButtonsListWidget
import layouts.widgets.PageNavigationWidget
import layouts.widgets.TopMenuBar
from ops.NewProjectHandler import NewProjectHandler
from ops.Operations import OperationType


class Workspace(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(InputListener())
        self.add_widget(FileHandler())
        self.add_widget(NewProjectHandler())
        SessionGlobals.active_operation = OperationType.TRANSLATE
        SessionGlobals.project = ProjectData()

