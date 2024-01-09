from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image as CorImg


class HBoxLayoutExample(App):
    def build(self):
        board = GridLayout(cols=8, size_hint=(None, None))
        for _ in range(64):
            board.add_widget(Button(background_color=[1, 1, 1, 1]))

        img_user = 
        img_user = BoxLayout(size_hint=(None, None))
        img_user.add_widget(Image())

        root = FloatLayout()
        root.add_widget(img_user)
        root.add_widget(board)

        root.bind(size=self.on_layout_size)
        return root

    @staticmethod
    def on_layout_size(instance, value):
        instance.children[0].width = instance.children[0].height = instance.height
        instance.children[0].x = (instance.width - instance.height) / 2
        instance.children[1].height = instance.children[1].width = (instance.width - instance.height) / 2
        print(instance.children[1], instance.children[1].width)


class HomePage(App):
    ...


if __name__ == "__main__":
    app = HBoxLayoutExample()
    app.run()
