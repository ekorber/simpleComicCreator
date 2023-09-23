# PROJECT
project = None           # The currently opened project
current_page: int = 0
current_layer: int = 0

# CANVAS
canvas_mouse_last_x = 0
canvas_mouse_last_y = 0
canvas_page_position: tuple[int, int] = (0, 0)

# OPERATORS
active_operation = None  # The currently active operation
