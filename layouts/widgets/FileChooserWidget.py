from kivy.uix.boxlayout import BoxLayout

from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView


class FileChooserWidget(BoxLayout):

    def __init__(self, open_file, cancel, **kwargs):
        super(FileChooserWidget, self).__init__(**kwargs)

        container = BoxLayout(orientation='vertical')
        button_layout = BoxLayout(size_hint=(1, 0.2))

        filechooser = FileChooserIconView(filters=['*.jpg', '*.webp', '*.png'])

        open_btn = Button(text='Select Image', size_hint=(.5, 1))
        open_btn.bind(on_release=lambda x: open_file(filechooser.path, filechooser.selection))

        cancel_btn = Button(text='Cancel', size_hint=(.5, 1))
        cancel_btn.bind(on_release=lambda x: cancel())

        button_layout.add_widget(open_btn)
        button_layout.add_widget(cancel_btn)

        container.add_widget(filechooser)
        container.add_widget(button_layout)
        self.add_widget(container)

