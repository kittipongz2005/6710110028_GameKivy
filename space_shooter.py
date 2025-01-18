from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Rectangle, Ellipse
from kivy.core.window import Window
from kivy.clock import Clock
import random
from kivy.core.audio import SoundLoader

# หน้าจอหลัก (Main Menu)
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source=r'C:\Users\Asus\Desktop\รูป\5.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        start_button = Button(text="เริ่มเกม", size_hint=(None, None), size=(200, 50), font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                              pos_hint={'center_x': 0.5, 'center_y': 0.2})
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

    def start_game(self, instance):
        self.manager.current = 'character_selection'


# หน้าจอเลือกตัวละคร (Character Selection)
class CharacterSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source=r'C:\Users\Asus\Desktop\รูป\6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        self.character_images = [
            r'C:\Users\Asus\Desktop\รูป\1.png',
            r'C:\Users\Asus\Desktop\รูป\2.png',
            r'C:\Users\Asus\Desktop\รูป\3.png',
            r'C:\Users\Asus\Desktop\รูป\4.png'
        ]

        for i in range(4):
            character_button = Button(text=f"ตัวละคร {i+1}", size_hint=(None, None), size=(200, 50), font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                                      pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1})
            character_button.bind(on_press=lambda instance, i=i: self.select_character(i))
            self.add_widget(character_button)

    def select_character(self, character_id):
        self.manager.get_screen('game').selected_character = self.character_images[character_id]
        self.manager.current = 'character_screen'


# หน้าจอแสดงผลตัวละครที่เลือก (Character Screen)
class CharacterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source=r'C:\Users\Asus\Desktop\รูป\6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        self.character_image = Image(size_hint=(None, None), size=(200, 200),
                                     pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.character_image)

        start_button = Button(text="เริ่ม", size_hint=(None, None), size=(150, 50),
                              font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                              pos_hint={'x': 0.85, 'y': 0})
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

        back_button = Button(text="ย้อนกลับ", size_hint=(None, None), size=(150, 50),
                             font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                             pos_hint={'x': 0.05, 'y': 0})
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def on_enter(self):
        self.character_image.source = self.manager.get_screen('game').selected_character

    def start_game(self, instance):
        self.manager.current = 'game'

    def go_back(self, instance):
        self.manager.current = 'character_selection'


# หน้าจอเกม (Game Screen)
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

    def on_enter(self):
        self.game_widget.set_hero_image(self.selected_character)


# เกม
class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound = SoundLoader.load('test.mp3')
        if self.sound:
            self.sound.play()

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self.pressed_keys = set()

        with self.canvas:
            self.hero = Rectangle(pos=(Window.width / 2, 50), size=(100, 100))
            self.bullets = []
            self.asteroids = []

        self.hero_speed = 500
        self.bullet_speed = 10
        self.asteroid_speed = 2
        self.asteroid_spawn_interval = 2.0  # เริ่มต้นที่ 2 วินาที
        self.asteroid_timer = 0.0

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def set_hero_image(self, image_path):
        self.hero.source = image_path

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

    def move_step(self, dt):
        cur_x, cur_y = self.hero.pos
        step = self.hero_speed * dt

        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step

        cur_x = max(0, min(cur_x, Window.width - self.hero.size[0]))
        cur_y = max(0, min(cur_y, Window.height - self.hero.size[1]))

        self.hero.pos = (cur_x, cur_y)

    def shoot_bullet(self):
        with self.canvas:
            bullet = Rectangle(pos=(self.hero.pos[0] + self.hero.size[0] / 2 - 5, self.hero.pos[1] + self.hero.size[1]), size=(10, 20))
            self.bullets.append(bullet)

    def create_asteroid(self):
        with self.canvas:
            x_pos = random.randint(0, Window.width - 50)
            asteroid_image = Image(source=r'C:\Users\Asus\Desktop\รูป\9.png', size=(50, 50))
            asteroid = Ellipse(pos=(x_pos, Window.height), size=(50, 50), texture=asteroid_image.texture)
            self.asteroids.append(asteroid)

    def update(self, dt):
        self.move_step(dt)
        self.asteroid_timer += dt

        if self.asteroid_timer >= self.asteroid_spawn_interval:
            self.create_asteroid()
            self.asteroid_timer = 0
            self.asteroid_spawn_interval = max(0.5, self.asteroid_spawn_interval - 0.05)

        for bullet in self.bullets:
            bullet.pos = (bullet.pos[0], bullet.pos[1] + self.bullet_speed)
            if bullet.pos[1] > Window.height:
                self.canvas.remove(bullet)
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            asteroid.pos = (asteroid.pos[0], asteroid.pos[1] - self.asteroid_speed)
            if asteroid.pos[1] < 0:
                self.canvas.remove(asteroid)
                self.asteroids.remove(asteroid)

        self.check_collisions()

    def check_collisions(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.collide_widget(asteroid):
                    self.canvas.remove(bullet)
                    self.canvas.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    return


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(CharacterSelection(name='character_selection'))
        sm.add_widget(CharacterScreen(name='character_screen'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == '__main__':
    app = MyApp()
    app.run()
