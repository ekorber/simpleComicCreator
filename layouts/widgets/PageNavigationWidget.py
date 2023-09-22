from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data import SessionGlobals


class PageNavigationWidget(BoxLayout):
    dropdown_button = ObjectProperty(Button)
    page_num_text = StringProperty('1')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.dropdown = DropDown()
        for index in range(SessionGlobals.total_pages):

            btn = Button(text='%d' % (index + 1), size_hint_y=None, height=30)

            # for each button, attach a callback that will call the select() method
            # on the dropdown. We'll pass the text of the button as the data of the
            # selection.
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))

            # then add the button inside the dropdown
            self.dropdown.add_widget(btn)

        self.dropdown.bind(on_select=lambda instance, x: self.select_page(str(x)))

    def select_page(self, text: str):
        self.page_num_text = text

    def open_dropdown(self):
        self.dropdown.open(self.dropdown_button)

    def add_new_page(self):
        pass

    def delete_page(self):
        pass
