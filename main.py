from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Necessary imports for kv files
import layouts.screens.Workspace
import layouts.screens.SignUpForm


class SignUpWindow(Screen):
    pass


class LoginWindow(Screen):
    pass


class WorkspaceWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class Application(App):
    def build(self):
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Application().run()
