from data.ProjectData import ProjectData
from ops.Operations import OperationType

# INPUT
input_listener = None

# WORKSPACE
editor = None
op_button_list = None
layers_tab = None

# PROJECT
project = ProjectData()

# OPERATIONS
active_operation: OperationType = OperationType.TRANSLATE
