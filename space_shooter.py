from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import NumericProperty


class Spacecraft(Image):
    velocity_x = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Spacecraft, self).__init__(**kwargs)
        self.source = r'C:\Users\Asus\Desktop\รูป\1.png' 
        self.size_hint = (None, None)
        self.size = (120, 200)  

    def move(self):
        self.x += self.velocity_x


class SpaceShooterGame(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpaceShooterGame, self).__init__(**kwargs)
        self.spacecraft = Spacecraft()
        self.spacecraft.y = 50
        self.add_widget(self.spacecraft)
        self.bind(size=self._on_size)  

    def _on_size(self, *args):
        self.spacecraft.center_x = self.width / 2

    def update(self, dt):
        self.spacecraft.move()

class SpaceShooterApp(App):
    def build(self):
        game = SpaceShooterGame()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    SpaceShooterApp().run()
