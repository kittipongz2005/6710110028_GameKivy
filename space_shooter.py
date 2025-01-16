from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from random import randint

# หน้าจอเลือกตัวละคร
class CharacterSelectScreen(Screen):
    selected_ship = StringProperty("")

    def __init__(self, **kwargs):
        super(CharacterSelectScreen, self).__init__(**kwargs)

        # เพิ่มพื้นหลัง
        background = Image(
            source=r'C:\Users\Asus\Desktop\รูป\5.jpg',
            allow_stretch=True,
            size_hint=(1.35, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(background)

        layout = BoxLayout(orientation='vertical', spacing=30, padding=(20, 20, 20, 20))

        self.character_label = Label(
            text="เลือกตัวละคร",
            font_size=50,
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(1, 0.2),
            halign="center",
            valign="middle"
        )
        self.character_label.bind(size=self.character_label.setter('text_size'))
        layout.add_widget(self.character_label)

        grid_layout = GridLayout(cols=2, padding=10, spacing=20, size_hint=(1, 0.6))
        self.ship_buttons = []

        for i in range(1, 5):
            button = Button(
                text=f"ยานอวกาศ {i}",
                font_size=30,
                font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                size_hint=(None, None),
                size=(450, 200)
            )
            button.bind(on_press=self.select_ship)
            grid_layout.add_widget(button)
            self.ship_buttons.append(button)

        layout.add_widget(grid_layout)
        self.add_widget(layout)

    def select_ship(self, instance):
        self.selected_ship = instance.text
        print(f"เลือก: {self.selected_ship}")

        self.manager.current = 'ship_image_screen'
        ship_image_screen = self.manager.get_screen('ship_image_screen')
        ship_image_screen.set_ship(self.selected_ship)


# หน้าจอแสดงรูปยาน
class ShipImageScreen(Screen):
    selected_ship = StringProperty("")
    ship_image = None

    def __init__(self, **kwargs):
        super(ShipImageScreen, self).__init__(**kwargs)

        # เพิ่มพื้นหลัง
        background = Image(
            source=r'C:\Users\Asus\Desktop\รูป\5.jpg',
            allow_stretch=True,
            size_hint=(1.35, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(background)

        layout = BoxLayout(orientation='vertical', spacing=30, padding=(20, 20, 20, 20))

        self.ship_image = Image(size_hint=(None, None), size=(300, 300))
        layout.add_widget(self.ship_image)

        bottom_buttons_layout = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, None), 
            height=60,
            padding=(20, 0)
        )

        back_button = Button(
            text="ย้อนกลับ",
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0, 'y': 0}
        )
        back_button.bind(on_press=self.go_back)
        bottom_buttons_layout.add_widget(back_button)

        start_button = Button(
            text="เริ่มเกม",
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'right': 1, 'y': 0}
        )
        start_button.bind(on_press=self.start_game)
        bottom_buttons_layout.add_widget(start_button)

        layout.add_widget(bottom_buttons_layout)
        self.add_widget(layout)

    def set_ship(self, ship_name):
        self.selected_ship = ship_name
        self.update_ship_image()

    def update_ship_image(self):
        if self.selected_ship == "ยานอวกาศ 1":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\1.png'
        elif self.selected_ship == "ยานอวกาศ 2":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\2.png'
        elif self.selected_ship == "ยานอวกาศ 3":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\3.png'
        elif self.selected_ship == "ยานอวกาศ 4":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\4.png'

        self.ship_image.pos_hint = {'center_x': 0.5, 'y': 0.1}

    def go_back(self, instance):
        self.manager.current = 'select'

    def start_game(self, instance):
        self.manager.current = 'game'
        game_screen = self.manager.get_screen('game')
        game_screen.set_ship(self.selected_ship)


# หน้าจอเกม
class SpaceShooterGame(Screen):
    selected_ship = StringProperty("")
    ship_image = None
    bullets = []
    enemies = []
    score = 0
    score_label = None

    def __init__(self, **kwargs):
        super(SpaceShooterGame, self).__init__(**kwargs)
        self.ship_image = Image(size_hint=(None, None), size=(100, 100))
        self.ship_image.pos_hint = {'center_x': 0.5, 'y': 0.1}
        self.add_widget(self.ship_image)

        # เพิ่มพื้นหลัง
        background = Image(
            source=r'C:\Users\Asus\Desktop\รูป\5.jpg',
            allow_stretch=True,
            size_hint=(1.35, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(background)
        
        self.score_label = Label(
            text=f"คะแนน: {self.score}",
            font_size=30,
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0.5, 'top': 1}
        )
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 2.0)

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        # เพิ่มการจับการลากของเมาส์
        self.bind(on_touch_move=self.on_touch_move)

    def set_ship(self, ship_name):
        self.selected_ship = ship_name
        self.update_ship_image()

    def update_ship_image(self):
        if self.selected_ship == "ยานอวกาศ 1":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\1.png'
        elif self.selected_ship == "ยานอวกาศ 2":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\2.png'
        elif self.selected_ship == "ยานอวกาศ 3":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\3.png'
        elif self.selected_ship == "ยานอวกาศ 4":
            self.ship_image.source = r'C:\Users\Asus\Desktop\รูป\4.png'

        self.ship_image.pos_hint = {'center_x': 0.5, 'y': 0.1}  # ยานอยู่ที่ตำแหน่งเริ่มต้น

    def on_touch_move(self, instance, touch):
        # เคลื่อนยานให้ตามตำแหน่งเมาส์
        self.ship_image.center = touch.pos

    def on_key_down(self, instance, keyboard, keycode, scancode, modifiers):
        if keycode == 97:  # A
            self.velocity_x = -10
        elif keycode == 100:  # D
            self.velocity_x = 10
        elif keycode == 119:  # W
            self.velocity_y = 10
        elif keycode == 115:  # S
            self.velocity_y = -10
        elif keycode == 32:  # Space (ยิงกระสุน)
            self.fire_bullet()

    def on_key_up(self, instance, keyboard, keycode):
        if keycode == 97 or keycode == 100:
            self.velocity_x = 0
        elif keycode == 119 or keycode == 115:
            self.velocity_y = 0

    def update(self, dt):
        self.update_bullets()
        self.update_enemies()

    def spawn_enemy(self, dt):
        enemy = Image(
            source=r'C:\Users\Asus\Desktop\รูป\enemy.png',
            size_hint=(None, None),
            size=(50, 50)
        )
        enemy.pos = (randint(0, Window.width-50), Window.height)
        self.add_widget(enemy)
        self.enemies.append(enemy)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.y += 10
            if bullet.top > Window.height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.y -= 5
            if enemy.collide_widget(self.ship_image):  # ตรวจสอบชนกับยาน
                print("Game Over!")
                self.manager.current = 'select'
                return

            for bullet in self.bullets:
                if bullet.collide_widget(enemy):  # ตรวจสอบชนระหว่างกระสุนและศัตรู
                    self.update_score(10)  # เพิ่มคะแนนเมื่อชน
                    self.remove_widget(bullet)
                    self.remove_widget(enemy)
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break  # ออกจากลูปเมื่อเจอการชน
            if enemy.y + enemy.height < 0:  # ถ้าศัตรูหลุดออกจากหน้าจอ
                self.remove_widget(enemy)
                self.enemies.remove(enemy)

    def fire_bullet(self):
        bullet = Image(
            source=r'C:\Users\Asus\Desktop\รูป\bullet.png',
            size_hint=(None, None),
            size=(10, 30)
        )
        bullet.pos = (self.ship_image.center_x - 5, self.ship_image.top)
        self.add_widget(bullet)
        self.bullets.append(bullet)

    def update_score(self, points):
        self.score += points
        self.score_label.text = f"คะแนน: {self.score}"


# แอปหลัก
class SpaceShooterApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(CharacterSelectScreen(name='select'))
        screen_manager.add_widget(ShipImageScreen(name='ship_image_screen'))
        screen_manager.add_widget(SpaceShooterGame(name='game'))
        return screen_manager


if __name__ == '__main__':
    SpaceShooterApp().run()
