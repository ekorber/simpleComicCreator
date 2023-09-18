from abc import ABC, abstractmethod
from enum import Enum
from data import AppGlobals as App
import lib.GuiHandler as Gui


class OperationType(Enum):
    NONE = 0
    PAN = 1
    TRANSLATE = 2
    ROTATE = 3
    SCALE = 4


class Operator(ABC):

    def register(self, start_key: str):
        Gui.canvas.bind(start_key, lambda e: self.begin())
        Gui.canvas.bind('<Motion>', lambda e: self.mouse_movement(e))
        Gui.canvas.bind('<Button-2>', lambda e: self.apply())
        Gui.canvas.bind('<Button-3>', lambda e: self.cancel())

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def update_loop(self):
        pass

    @abstractmethod
    def mouse_movement(self, e):
        pass

    @abstractmethod
    def apply(self):
        pass

    @abstractmethod
    def cancel(self):
        pass


def page_and_layer_in_bounds():
    result = (0 <= App.current_page < len(App.project.pages)
              and 0 <= App.current_layer < len(App.project.pages[App.current_page].layers))

    if not result:
        print(f'Page or Layer out of bounds! Page: {App.current_page}, Layer: {App.current_layer}')

    return result


def can_operator_begin():
    return len(App.project.pages[App.current_page].layers) > 0
