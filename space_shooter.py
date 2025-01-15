from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout

# หน้าจอเลือกตัวละคร
class CharacterSelectScreen(Screen):
    selected_ship = StringProperty("")

    def __init__(self, **kwargs):
        super(CharacterSelectScreen, self).__init__(**kwargs)

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

        # ปรับขนาดปุ่มให้ใหญ่ขึ้น และบาลานด์การจัดเรียง
        grid_layout = GridLayout(cols=2, padding=10, spacing=20, size_hint=(1, 0.6))
        self.ship_buttons = []

        for i in range(1, 5):
            button = Button(
                text=f"ยานอวกาศ {i}",
                font_size=30,
                font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
                size_hint=(None, None),
                size=(450, 200)  # ขยายขนาดของปุ่มให้ใหญ่ขึ้น
            )
            button.bind(on_press=self.select_ship)
            grid_layout.add_widget(button)
            self.ship_buttons.append(button)

        layout.add_widget(grid_layout)
        self.add_widget(layout)

    def select_ship(self, instance):
        self.selected_ship = instance.text
        print(f"เลือก: {self.selected_ship}")

        # เปลี่ยนไปยังหน้าจอที่มีรูปยาน
        self.manager.current = 'ship_image_screen'
        ship_image_screen = self.manager.get_screen('ship_image_screen')
        ship_image_screen.set_ship(self.selected_ship)


# หน้าจอแสดงรูปยาน
class ShipImageScreen(Screen):
    selected_ship = StringProperty("")
    ship_image = None

    def __init__(self, **kwargs):
        super(ShipImageScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=30, padding=(20, 20, 20, 20))

        # เพิ่มรูปยาน
        self.ship_image = Image(size_hint=(None, None), size=(300, 300))
        layout.add_widget(self.ship_image)

        # สร้าง BoxLayout สำหรับปุ่มที่ด้านล่าง
        bottom_buttons_layout = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, None), 
            height=60,
            padding=(20, 0)  # กำหนด padding ด้านข้าง
        )

        # ปุ่มย้อนกลับอยู่ที่มุมซ้าย
        back_button = Button(
            text="ย้อนกลับ",
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0, 'y': 0}  # ปรับตำแหน่งให้ปุ่มอยู่ที่มุมล่างซ้าย
        )
        back_button.bind(on_press=self.go_back)
        bottom_buttons_layout.add_widget(back_button)

        # ปุ่มเริ่มเกมอยู่ที่มุมขวา
        start_button = Button(
            text="เริ่มเกม",
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'right': 1, 'y': 0}  # ปรับตำแหน่งให้ปุ่มอยู่ที่มุมล่างขวา
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

        # ปรับตำแหน่งยานให้อยู่กึ่งกลางหน้าจอ
        self.ship_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def go_back(self, instance):
        self.manager.current = 'select'

    def start_game(self, instance):
        # สามารถเพิ่มฟังก์ชันการเริ่มเกมที่นี่
        print(f"เริ่มเกมกับ {self.selected_ship}")
        # เปลี่ยนหน้าจอไปยังเกมจริง ๆ
        self.manager.current = 'game'


# หน้าจอเกม
class SpaceShooterGame(Screen):
    selected_ship = StringProperty("")
    velocity_x = 0

    def __init__(self, **kwargs):
        super(SpaceShooterGame, self).__init__(**kwargs)

        self.ship_image = Image(size_hint=(None, None), size=(300, 300))
        self.add_widget(self.ship_image)

        # ปุ่มย้อนกลับอยู่ที่มุมล่างซ้าย
        self.back_button = Button(
            text="ย้อนกลับ",
            font_name="C:/Users/Asus/Downloads/file-11-21-55-OQtwta/THSarabun.ttf",
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'x': 0, 'y': 0}  # ปรับตำแหน่งให้ปุ่มอยู่ที่มุมล่างซ้าย
        )
        self.back_button.bind(on_press=self.go_back)
        self.add_widget(self.back_button)

        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

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

        # ปรับตำแหน่งยานให้อยู่กึ่งกลางหน้าจอ
        self.ship_image.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def go_back(self, instance):
        self.manager.current = 'select'

    def update(self, dt):
        self.ship_image.x += self.velocity_x

    def on_key_down(self, instance, keyboard, keycode, scancode, modifiers):
        if keycode == 97:  # A
            self.velocity_x = -10
        elif keycode == 100:  # D
            self.velocity_x = 10

    def on_key_up(self, instance, keyboard, keycode):
        if keycode == 97:  # A
            self.velocity_x = 0
        elif keycode == 100:  # D
            self.velocity_x = 0

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
