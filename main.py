from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from plyer import filechooser
from cut_tubes import cut_tubes


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        pass
        # return Builder.load_file('main.kv')

    def choose_file(self):
        bom_path = filechooser.open_file(title='choose a bom list', filters=[('Excel file', '*.xlsx')])[0]

        self.root.ids.top_label.text = 'A text file with the optimal way to cut the tubes was created at:\n' \
                                       f'{bom_path[:-5]} - cut tubes.txt\n'

        tubes_results = {
            'Constructiebuis vierkant': cut_tubes(['Constructiebuis vierkant', 'koker'], bom_path, 6000, True, 3),
            'Rechthoekige buis': cut_tubes(['Rechthoekige buis'], bom_path),
            'HDPE100 Drukbuis': cut_tubes(['HDPE100 Drukbuis', 'PE buis'], bom_path),
            'PVC Drukbuis': cut_tubes(['PVC Drukbuis', 'PVC buis'], bom_path, 5000),
            'Hoeklijn': cut_tubes(['Hoeklijn', 'L-profiel'], bom_path),
            'Draadstang': cut_tubes(['DIN 976-1A', 'draadstang'], bom_path, 3000)
        }
        # pass if there is no Diameter or Thickness column
        try:
            tubes_results['Gelaste ronde buis'] = cut_tubes(['EN 10217-7', 'ronde buis'], bom_path, use_size=False)
        except ValueError:
            self.root.ids.top_label.text += '\n Warning: No column Diameter or Thickness was found'

        # Add labels to tubes_table
        for tube, tube_dict in tubes_results.items():
            multiple_sizes = False
            if tube_dict[0]:
                self.root.ids.tubes_table.add_widget(MDLabel(text=f'{tube}'))
                for size, size_result in tube_dict[0].items():
                    if size_result[0]:
                        if multiple_sizes:
                            self.root.ids.tubes_table.add_widget(MDLabel())
                        self.root.ids.tubes_table.add_widget(MDLabel(text=f'{size}'))
                        self.root.ids.tubes_table.add_widget(MDLabel(text=f'{len(size_result[0])}'))
                        multiple_sizes = True

        if any([v[1] for v in tubes_results.values()]):
            self.root.ids.top_label.text += '\n Warning: Missing data, please check the warnings txt file to see the ' \
                                            'components with missing data'


if __name__ == '__main__':
    MainApp().run()
