from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.core.window import Window
from kivy.clock import Clock
import random
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/5.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        start_button = Button(text="เริ่มเกม", size_hint=(None, None), size=(200, 50), font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                              pos_hint={'center_x': 0.5, 'center_y': 0.2})
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

    def start_game(self, instance):
        self.manager.current = 'character_selection'

class CharacterSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        title_label = Label(text="เลือกตัวละคร", font_size=50, font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                            size_hint=(None, None), size=(300, 100), pos_hint={'center_x': 0.5, 'top': 1})
        self.add_widget(title_label)

        self.character_images = [
            'C:/Users/Asus/Desktop/รูป/1.png',
            'C:/Users/Asus/Desktop/รูป/2.png',
            'C:/Users/Asus/Desktop/รูป/3.png',
            'C:/Users/Asus/Desktop/รูป/4.png'
        ]

        for i in range(4):
            character_button = Button(text=f"ตัวละคร {i+1}", size_hint=(None, None), size=(200, 50), font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                                      pos_hint={'center_x': 0.5, 'center_y': 0.6 - i * 0.1})
            character_button.bind(on_press=lambda instance, i=i: self.select_character(i))
            self.add_widget(character_button)

    def select_character(self, character_id):
        self.manager.get_screen('game').selected_character = self.character_images[character_id]
        self.manager.current = 'character_screen'

class CharacterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        self.character_image = Image(size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.6})
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

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        game_over_label = Label(text="Game Over!", font_size=50, color=(1, 0, 0, 1),
                                font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                                size_hint=(None, None), size=(400, 100), pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(game_over_label)

        quit_button = Button(text="ออกจากเกม", size_hint=(None, None), size=(200, 50),
                             font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                             pos_hint={'center_x': 0.5, 'center_y': 0.2})
        quit_button.bind(on_press=self.quit_game)  # Bind quit_game function here
        self.add_widget(quit_button)

    def retry_game(self, instance):
        self.manager.get_screen('game').reset_game()
        self.manager.get_screen('game').set_hero_image(self.manager.get_screen('game').selected_character)
        self.manager.current = 'game'

    def quit_game(self, instance):
        App.get_running_app().stop()  # This stops the application


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/12.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

    def on_enter(self):
        self.game_widget.set_hero_image(self.selected_character)
        Clock.schedule_once(self.start_asteroids, 1.0)

    def start_asteroids(self, dt):
        self.game_widget.start_asteroid_creation()

    def on_leave(self):
        self.game_widget.reset_game()

    def set_hero_image(self, image_path):
        self.game_widget.set_hero_image(image_path)

    def reset_game(self):
        self.game_widget.reset_game()


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

        self.game_over = False

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def set_hero_image(self, image_path):
        self.hero_image = Image(source=image_path, size=(100, 100), pos=self.hero.pos)
        self.add_widget(self.hero_image)

    def start_asteroid_creation(self):
        Clock.schedule_interval(self.create_asteroid, 1.0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'i' and not self.game_over:
            self.shoot_bullet()
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
            bullet_image = Image(source='C:/Users/Asus/Desktop/รูป/8.png', size=(10, 20))
            bullet = Rectangle(pos=(self.hero.pos[0] + self.hero.size[0] / 2 - 5, self.hero.pos[1] + self.hero.size[1]), size=(10, 20), texture=bullet_image.texture)
            self.bullets.append(bullet)

    def create_asteroid(self, dt):
        with self.canvas:
            x_pos = random.randint(0, Window.width - 50)
            asteroid_image = Image(source='C:/Users/Asus/Desktop/รูป/9.png', size=(50, 50))
            asteroid = Ellipse(pos=(x_pos, Window.height), size=(50, 50), texture=asteroid_image.texture)
            self.asteroids.append(asteroid)

    def update(self, dt):
        if self.game_over:
            return

        self.move_step(dt)

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
                if self.check_collision(bullet, asteroid):
                    self.canvas.remove(bullet)
                    self.canvas.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

        for asteroid in self.asteroids:
            if self.check_asteroid_collision(asteroid):
                self.show_game_over()

    def check_collision(self, bullet, asteroid):
        bullet_center = (bullet.pos[0] + bullet.size[0] / 2, bullet.pos[1] + bullet.size[1] / 2)
        asteroid_center = (asteroid.pos[0] + asteroid.size[0] / 2, asteroid.pos[1] + asteroid.size[1] / 2)
        distance = ((bullet_center[0] - asteroid_center[0]) ** 2 + (bullet_center[1] - asteroid_center[1]) ** 2) ** 0.5
        return distance < (bullet.size[0] / 2 + asteroid.size[0] / 2)

    def check_asteroid_collision(self, asteroid):
        hero_center = (self.hero.pos[0] + self.hero.size[0] / 2, self.hero.pos[1] + self.hero.size[1] / 2)
        asteroid_center = (asteroid.pos[0] + asteroid.size[0] / 2, asteroid.pos[1] + asteroid.size[1] / 2)
        distance = ((hero_center[0] - asteroid_center[0]) ** 2 + (hero_center[1] - asteroid_center[1]) ** 2) ** 0.5
        return distance < (self.hero.size[0] / 2 + asteroid.size[0] / 2)

    def show_game_over(self):
        self.game_over = True
        self.parent.manager.current = 'game_over'

    def reset_game(self):
        self.game_over = False
        self.bullets.clear()
        self.asteroids.clear()
        self.hero.pos = (Window.width / 2, 50)



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

        self.game_over = False

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def set_hero_image(self, image_path):
        hero_image = Image(source=image_path).texture
        self.hero.texture = hero_image

    def start_asteroid_creation(self):
        Clock.schedule_interval(self.create_asteroid, 1.0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'i' and not self.game_over:
            self.shoot_bullet()
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
            bullet_image = Image(source='C:/Users/Asus/Desktop/รูป/8.png', size=(10, 20))
            bullet = Rectangle(pos=(self.hero.pos[0] + self.hero.size[0] / 2 - 5, self.hero.pos[1] + self.hero.size[1]), size=(10, 20), texture=bullet_image.texture)
            self.bullets.append(bullet)

    def create_asteroid(self, dt):
        with self.canvas:
            x_pos = random.randint(0, Window.width - 50)
            asteroid_image = Image(source='C:/Users/Asus/Desktop/รูป/9.png', size=(50, 50))
            asteroid = Ellipse(pos=(x_pos, Window.height), size=(50, 50), texture=asteroid_image.texture)
            self.asteroids.append(asteroid)

    def update(self, dt):
        if self.game_over:
            return

        self.move_step(dt)

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
                if self.check_collision(bullet, asteroid):
                    self.canvas.remove(bullet)
                    self.canvas.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)

        for asteroid in self.asteroids:
            if self.check_asteroid_collision(asteroid):
                self.show_game_over()

    def check_collision(self, bullet, asteroid):
        bullet_center = (bullet.pos[0] + bullet.size[0] / 2, bullet.pos[1] + bullet.size[1] / 2)
        asteroid_center = (asteroid.pos[0] + asteroid.size[0] / 2, asteroid.pos[1] + asteroid.size[1] / 2)
        distance = ((bullet_center[0] - asteroid_center[0]) ** 2 + (bullet_center[1] - asteroid_center[1]) ** 2) ** 0.5
        return distance < (bullet.size[0] / 2 + asteroid.size[0] / 2)

    def check_asteroid_collision(self, asteroid):
        hero_center = (self.hero.pos[0] + self.hero.size[0] / 2, self.hero.pos[1] + self.hero.size[1] / 2)
        asteroid_center = (asteroid.pos[0] + asteroid.size[0] / 2, asteroid.pos[1] + asteroid.size[1] / 2)
        distance = ((hero_center[0] - asteroid_center[0]) ** 2 + (hero_center[1] - asteroid_center[1]) ** 2) ** 0.5
        return distance < (self.hero.size[0] / 2 + asteroid.size[0] / 2)

    def show_game_over(self):
        self.game_over = True
        self.parent.manager.current = 'game_over'

    def reset_game(self):
        self.game_over = False
        self.bullets.clear()
        self.asteroids.clear()
        self.hero.pos = (Window.width / 2, 50)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(CharacterSelection(name='character_selection'))
        sm.add_widget(CharacterScreen(name='character_screen'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(GameOverScreen(name='game_over'))
        return sm

if __name__ == '__main__':
    MyApp().run()
