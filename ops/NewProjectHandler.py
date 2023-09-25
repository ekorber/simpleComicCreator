from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from data import SessionGlobals
from data.ProjectData import ProjectData


class NewProjectMenu(BoxLayout):
    def __init__(self, handler, cancel, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        dpi_layout = BoxLayout(spacing=10, size_hint=(1, None), size=(1, 30))
        dpi_label = Label(text='DPI ', size_hint=(None, 1), size=(50, 1))
        self.dpi_input = TextInput(text="300", input_filter='int', halign='center')
        dpi_layout.add_widget(dpi_label)
        dpi_layout.add_widget(self.dpi_input)

        size_inches_label_wrapper_layout = BoxLayout(orientation='vertical', size_hint=(1, None), size=(1, 60))
        size_inches_label = Label(text='Size in inches', size_hint=(1, None), size=(1, 30))
        size_inches_label_wrapper_layout.add_widget(size_inches_label)

        size_inches_width_layout = BoxLayout(spacing=10, size_hint=(1, None), size=(1, 30))
        width_label = Label(text='Width ', size_hint=(None, 1), size=(50, 1))
        self.size_inches_width_input = TextInput(text="6.875", input_filter='float', halign='center')
        size_inches_width_layout.add_widget(width_label)
        size_inches_width_layout.add_widget(self.size_inches_width_input)

        size_inches_height_layout = BoxLayout(spacing=10, size_hint=(1, None), size=(1, 30))
        height_label = Label(text='Height ', size_hint=(None, 1), size=(50, 1))
        self.size_inches_height_input = TextInput(text="10.438", input_filter='float', halign='center')
        size_inches_height_layout.add_widget(height_label)
        size_inches_height_layout.add_widget(self.size_inches_height_input)

        button_wrapper_layout = BoxLayout(spacing=15, size_hint=(1, None), size=(1, 100))
        create_button = Button(text='Create Project', size_hint=(1, None), size=(1, 50),
                               pos_hint={'center_x': 0.5})
        create_button.bind(on_release=lambda x: self.process_create_button_click(handler))
        cancel_button = Button(text='Cancel', size_hint=(1, None), size=(1, 50),
                               pos_hint={'center_x': 0.5})
        cancel_button.bind(on_release=lambda x: cancel())
        button_wrapper_layout.add_widget(create_button)
        button_wrapper_layout.add_widget(cancel_button)

        self.add_widget(dpi_layout)
        self.add_widget(size_inches_label_wrapper_layout)
        self.add_widget(size_inches_width_layout)
        self.add_widget(size_inches_height_layout)
        self.add_widget(button_wrapper_layout)

    def process_create_button_click(self, handler):
        if not self.dpi_input.text or not self.size_inches_width_input.text or not self.size_inches_height_input.text:
            return

        handler.handle_new_project_submit(dpi=int(self.dpi_input.text), size_in_inches=(
                                                                        float(self.size_inches_width_input.text),
                                                                        float(self.size_inches_height_input.text)))


class NewProjectHandler(Widget):

    popup_window = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SessionGlobals.new_project_handler = self

    def open_new_project_window(self):
        self.popup_window = Popup(title="New Project",
                                  content=NewProjectMenu(self, cancel=lambda: self.cancel()),
                                  size_hint=(None, None), size=(500, 400))
        self.popup_window.open()

    def handle_new_project_submit(self, dpi: int, size_in_inches: (float, float)):
        SessionGlobals.editor.clear_screen()
        SessionGlobals.layers_tab.clear_layers_tab()

        SessionGlobals.project = ProjectData(dpi=dpi, size_in_inches=size_in_inches)

        SessionGlobals.layers_tab.populate_layers_tab()
        SessionGlobals.layers_tab.select_layer(SessionGlobals.project.get_active_layer_index())
        SessionGlobals.page_navigation_widget.refresh_view_no_external_refresh()

        SessionGlobals.editor.populate_screen()
        self.popup_window.dismiss()
        SessionGlobals.input_listener.keyboard_open()

    def cancel(self):
        self.popup_window.dismiss()
        SessionGlobals.input_listener.keyboard_open()
