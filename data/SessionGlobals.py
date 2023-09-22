from objects.LayerCollection import LayerCollection
from ops.Operations import OperationType

# INPUT
input_listener = None

# WORKSPACE
editor = None
op_button_list = None
layers_tab = None

# LAYERS
layer_collection = LayerCollection()

# OPERATIONS
active_operation: OperationType = OperationType.TRANSLATE

# PAGES
current_page = 0
total_pages = 1
