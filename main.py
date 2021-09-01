from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        return Builder.load_file('main.kv')

    def file_manager_open(self):
        self.file_manager.show('/')

    def exit_manager(self):
        self.file_manager.close()

    def select_path(self, path):
        self.exit_manager()
        toast(path)


if __name__ == '__main__':
    MainApp().run()
