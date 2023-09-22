from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from data import SessionGlobals


class PageNavigationWidget(BoxLayout):
    dropdown_button = ObjectProperty(Button)
    page_num_text = StringProperty()
    dropdown = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_dropdown_options()
        self.page_num_text = str(SessionGlobals.current_page + 1)

    def select_page(self, page_num: str):
        self.page_num_text = page_num
        SessionGlobals.current_page = int(page_num) - 1

    def open_dropdown(self):
        self.dropdown.open(self.dropdown_button)

    def create_dropdown_options(self):
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

    def add_new_page(self):
        SessionGlobals.total_pages += 1
        SessionGlobals.current_page = SessionGlobals.total_pages - 1
        self.create_dropdown_options()
        self.select_page(str(SessionGlobals.current_page + 1))

    def delete_page(self):
        if SessionGlobals.total_pages <= 1:
            return

        SessionGlobals.total_pages -= 1

        if SessionGlobals.current_page == SessionGlobals.total_pages:
            SessionGlobals.current_page -= 1

        self.create_dropdown_options()
        self.select_page(str(SessionGlobals.current_page + 1))

