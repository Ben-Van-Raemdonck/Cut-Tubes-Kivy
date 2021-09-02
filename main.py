from kivy.lang import Builder
from kivymd.app import MDApp
from plyer import filechooser
from kivymd.toast import toast


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_file('main.kv')

    def choose_file(self):
        path = filechooser.open_file(title='choose a bom list', filters=[('Excel file', '*.xlsx')])
        toast(path[0])


if __name__ == '__main__':
    MainApp().run()
