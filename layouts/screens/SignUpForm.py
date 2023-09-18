from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout


class SignUpForm(GridLayout):

    first_name = ObjectProperty(None)
    email = ObjectProperty(None)

    def submit_button_pressed(self):
        print(f"New user signed up! Name: {self.first_name.text}, Email: {self.email.text}")
