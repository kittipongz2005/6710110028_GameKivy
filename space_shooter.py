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
from kivy.uix.progressbar import ProgressBar

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        background = Image(source='C:/Users/Asus/Desktop/รูป/21.jpg', allow_stretch=False, keep_ratio=True)
        self.add_widget(background)
        self.background_music = SoundLoader.load(r'C:\Users\Asus\Desktop\รูป\41.mp3')  # โหลดเสียงพื้นหลัง
        if self.background_music:
            self.background_music.loop = True  # ให้เสียงเล่นวนลูป
            self.background_music.play()
    
        start_label = Label(
            text="Space Shooter",
            size_hint=(None, None),
            color=(0.5, 0.5, 0.5, 1),  
            pos_hint={'center_x': 0.5, 'top': 0.95},  
            font_size='100sp'  
        )
        self.add_widget(start_label)

        start_button = Button(text="Start the game", size_hint=(0.2, 0.1), size=(200, 50), 
                          pos_hint={'center_x': 0.5, 'center_y': 0.2})
        start_button.bind(on_press=self.start_game)
        self.add_widget(start_button)

    def start_game(self, instance):
        self.manager.current = 'character_selection'

    def on_leave(self):
        if self.background_music:
            self.background_music.stop()


class CharacterSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/26.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.background_music = SoundLoader.load(r'C:\Users\Asus\Desktop\รูป\41.mp3')  # โหลดเสียงพื้นหลัง
        if self.background_music:
            self.background_music.loop = True  # ให้เสียงเล่นวนลูป
            self.background_music.play()


        title_label = Label(text="Select a spaceship", font_size=80, 
                        size_hint=(0.2, 0.1), size=(400, 200), 
                        pos_hint={'center_x': 0.5, 'top': 0.90})
        self.add_widget(title_label)

        self.character_images = [
            'C:/Users/Asus/Desktop/รูป/33.png',
            'C:/Users/Asus/Desktop/รูป/34.png',
            'C:/Users/Asus/Desktop/รูป/35.png',
            'C:/Users/Asus/Desktop/รูป/36.png'
        ]

        for i in range(4):
            character_button = Button(text=f"spaceship {i+1}", size_hint=(None, None), size=(200, 50), 
                                  pos_hint={'center_x': 0.5, 'center_y': 0.63 - i * 0.1})
            character_button.bind(on_press=lambda instance, i=i: self.select_character(i))
            self.add_widget(character_button)

    def select_character(self, character_id):
        self.manager.get_screen('game').selected_character = self.character_images[character_id]
        self.manager.current = 'character_screen'

    def on_enter(self):
        # เล่นเสียงพื้นหลังเมื่อเข้าสู่หน้าจอนี้
        if self.background_music:
            self.background_music.play()

    def on_leave(self):
        if self.background_music:
            self.background_music.stop()
    
class CharacterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/28.webp', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.background_music = SoundLoader.load(r'C:\Users\Asus\Desktop\รูป\42.mp3')  # โหลดเสียงพื้นหลัง
        if self.background_music:
            self.background_music.loop = True  # ให้เสียงเล่นวนลูป
            self.background_music.play()

        self.character_image = Image(size_hint=(None, None), size=(400, 400), 
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.character_image)

        # Bullet types selection
        self.bullet_types = [
            'C:/Users/Asus/Desktop/รูป/32.png',
            'C:/Users/Asus/Desktop/รูป/31.png', 
            'C:/Users/Asus/Desktop/รูป/30.png',
            'C:/Users/Asus/Desktop/รูป/29.png'
        ]
        self.bullet_2 = [
            'C:/Users/Asus/Desktop/รูป/37.png',
            'C:/Users/Asus/Desktop/รูป/38.png',
            'C:/Users/Asus/Desktop/รูป/39.png',
            'C:/Users/Asus/Desktop/รูป/40.png'
        ]
        
        self.selected_bullet = None
        
        # Bullet selection buttons
        for i in range(4):
            bullet_button = Button(
                text=f"                select", 
                size_hint=(0.15, 0.2), 
                color=(1, 0, 0, 1),
                size=(50, 100), 
                background_normal=self.bullet_types[i],
                pos_hint={'x': 0.7, 'y': 0.7 - i * 0.15} )
            bullet_button.bind(on_press=lambda instance, i=i: self.select_bullet(i))
            self.add_widget(bullet_button)

        # Start button (initially disabled)
        self.start_button = Button(text="Start", size_hint=(None, None), size=(150, 50),
                                   pos_hint={'x': 0.85, 'y': 0}, disabled=True)
        self.start_button.bind(on_press=self.start_game)
        self.add_widget(self.start_button)

        back_button = Button(text="Go Back", size_hint=(None, None), size=(150, 50),
                             pos_hint={'x': 0, 'y': 0})
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def on_enter(self):
        # Reset selection when screen is entered
        self.character_image.source = self.manager.get_screen('game').selected_character
        self.selected_bullet = None
        self.start_button.disabled = True
        if self.background_music:
            self.background_music.play()

    def select_bullet(self, bullet_id):
        # Store selected bullet and enable start button
        self.selected_bullet = self.bullet_types[bullet_id]
        self.start_button.disabled = False

    def start_game(self, instance):
    # เริ่มเกมได้เมื่อเลือกทั้งยานและกระสุน
        if self.selected_bullet:
            if self.background_music:
                self.background_music.stop()  # หยุดเสียงพื้นหลังเมื่อเปลี่ยนหน้า
            game_screen = self.manager.get_screen('game')
            game_screen.selected_bullet = self.selected_bullet  # ส่งต่อรูปภาพกระสุนที่เลือก
            self.manager.current = 'game'  # เปลี่ยนไปยังหน้าเล่นเกม

    def go_back(self, instance):
        self.manager.current = 'character_selection'
    
    def on_leave(self):
        if self.background_music:
            self.background_music.stop()

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = Image(source='C:/Users/Asus/Desktop/รูป/6.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        self.game_over_label = Label(text="Game Over!", font_size=50, color=(1, 0, 0, 1),
                                 size_hint=(None, None), size=(400, 100), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.7})
        self.add_widget(self.game_over_label)


        quit_button = Button(text="Exit the game", size_hint=(None, None), size=(200, 50),
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        quit_button.bind(on_press=self.quit_game)
        self.add_widget(quit_button)


        self.score_label = Label(text="", font_size=30, 
                             size_hint=(None, None), size=(400, 100), 
                             pos_hint={'center_x': 0.5, 'center_y': 0.55})
        self.add_widget(self.score_label)
        self.new_record_label = Label(
            text="", font_size=30, color=(1, 0, 0, 1),
            size_hint=(None, None), size=(400, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.45}
        )
        self.add_widget(self.new_record_label)

    def on_enter(self):

        game_screen = self.manager.get_screen('game')
        self.score_label.text = f"Your Score: {game_screen.game_widget.score}\nHight Score: {game_screen.game_widget.high_score}"
        if game_screen.game_widget.score > game_screen.game_widget.high_score:
            self.new_record_label.text = "New Record!"
        else:
            self.new_record_label.text = ""


        

    def retry_game(self, instance):
        game_screen = self.manager.get_screen('game')
        game_screen.reset_game()  # รีเซ็ตเกมใหม่ทั้งหมด
        game_screen.game_widget.score = 0  # รีเซ็ตคะแนนเป็น 0
        game_screen.game_widget.update_score_label()  # อัปเดตแสดงคะแนนใหม่
        self.manager.current = 'game'

    def quit_game(self, instance):
        App.get_running_app().stop()

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_bullet = None
        background = Image(source='C:/Users/Asus/Desktop/รูป/18.jpg', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)
        self.game_widget = GameWidget()
        self.add_widget(self.game_widget)

    def on_enter(self):
        self.game_widget.set_hero_image(self.selected_character)
        self.game_widget.selected_bullet = self.selected_bullet  # ส่งค่า selected_bullet ไปยัง GameWidget
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
  
        self.score = 0
        self.level = 1
        self.high_score = self.load_high_score()
        self.bullet_count = 100
        self.earth_health = 50 

        self.health_bar = ProgressBar(max=50, value=self.earth_health, size_hint=(0.6, None), height=30 , size=(800, 50))
        self.health_bar.pos = (Window.width * 0.1, 5)
        self.add_widget(self.health_bar)

        
        self.score_label = Label(
            text=f'Score: {self.score}\nHigh Score: {self.high_score}\nLevel: {self.level}',
            pos=(60, Window.height - 120),
            size_hint=(None, None),
            font_size=30
        )

        self.add_widget(self.score_label)
    

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
            self.ammo_powerups = []

        self.base_hero_speed = 500
        self.base_bullet_speed = 10
        self.base_asteroid_speed = 2
        self.update_speeds()

        self.game_over = False
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update_speeds(self):

        self.hero_speed = self.base_hero_speed + (self.level)
        self.bullet_speed = self.base_bullet_speed + (self.level)
        self.asteroid_speed = self.base_asteroid_speed + (self.level * 0.5)

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        with open('high_score.txt', 'w') as f:
            f.write(str(self.high_score))

    def set_hero_image(self, image_path):
        hero_image = Image(source=image_path).texture
        self.hero.texture = hero_image

    def start_asteroid_creation(self):
        Clock.schedule_interval(self.create_asteroid, max(1.0 - (self.level * 0.1), 0.3))
        Clock.schedule_interval(self.create_ammo_powerup, 10.0)  # เรียกทุก 10 วินาที


    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if text == 'i' and not self.game_over:  # ตรวจสอบว่ากดปุ่ม 'i' และเกมไม่จบ
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
        print("Shooting bullet!")  # แสดงข้อความเมื่อยิงกระสุน
        if self.bullet_count > 0:
            with self.canvas:
                if hasattr(self, 'selected_bullet') and self.selected_bullet:
                    print(f"Using bullet: {self.selected_bullet}")  # แสดงเส้นทางรูปภาพกระสุน
                    bullet_image = Image(source=self.selected_bullet, size=(10, 20))
                    bullet = Rectangle(
                        pos=(self.hero.pos[0] + self.hero.size[0] / 2 - 5, 
                            self.hero.pos[1] + self.hero.size[1]), 
                        size=(10, 20), 
                        texture=bullet_image.texture
                    )
                    self.bullets.append(bullet)
            self.bullet_count -= 1
            self.update_score_label()
        else:
            print("No bullets left!")  # แสดงข้อความเมื่อไม่มีลูกกระสุน
                
    def update_score_label(self):
        self.score_label.text = (f'Score: {self.score}\nHigh Score: {self.high_score}\n'
                             f'Level: {self.level}\nBullets: {self.bullet_count}')


    def create_ammo_powerup(self, dt):
        with self.canvas:
            x_pos = random.randint(0, Window.width - 30)
            y_pos = Window.height
            ammo_image = Image(source='C:/Users/Asus/Desktop/รูป/44.png', size=(30, 30))
            ammo_powerup = Rectangle(pos=(x_pos, y_pos), size=(30, 30), texture=ammo_image.texture)
            self.ammo_powerups.append(ammo_powerup)  # เพิ่มไปยัง self.ammo_powerups



    def create_asteroid(self, dt):
        with self.canvas:
            x_pos = random.randint(0, Window.width - 50)
            y_pos = Window.height
            asteroid_image = Image(source='C:/Users/Asus/Desktop/รูป/9.png', size=(50, 50))
            asteroid = Rectangle(pos=(x_pos, y_pos), size=(50, 50), texture=asteroid_image.texture)
            self.asteroids.append(asteroid)

    def show_game_over(self):
        self.game_over = True   
        self.parent.manager.current = 'game_over'

    def update(self, dt):
        if self.game_over:
            return

        self.move_step(dt)

        # อัปเดตการเคลื่อนที่ของ bullets
        for bullet in self.bullets:
            bullet.pos = (bullet.pos[0], bullet.pos[1] + self.bullet_speed)
            if bullet.pos[1] > Window.height:  # หากกระสุนหลุดจอ
                self.canvas.remove(bullet)
                self.bullets.remove(bullet)

        # อัปเดตการเคลื่อนที่ของ asteroids
        for asteroid in self.asteroids:
            asteroid.pos = (asteroid.pos[0], asteroid.pos[1] - self.asteroid_speed)
            if asteroid.pos[1] < 0:  # หากหลุดจอ
                self.earth_health -= 1  # ลดเลือดของโลก
                self.health_bar.value = self.earth_health  # อัปเดตหลอดเลือด
                self.canvas.remove(asteroid)
                self.asteroids.remove(asteroid)

        # อัปเดตการเคลื่อนที่ของ ammo_powerups
        for ammo in self.ammo_powerups:
            ammo.pos = (ammo.pos[0], ammo.pos[1] - self.asteroid_speed)
            if ammo.pos[1] < 0:
                self.canvas.remove(ammo)
                self.ammo_powerups.remove(ammo)

        # ตรวจสอบการชนของ bullets และ asteroids
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if self.check_collision(bullet, asteroid):
                    self.canvas.remove(bullet)
                    self.canvas.remove(asteroid)
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    self.score += 1
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                    self.update_score_label()
                    break

        # ตรวจสอบการชนของ hero กับ ammo_powerups
        for powerup in self.ammo_powerups:
            powerup.pos = (powerup.pos[0], powerup.pos[1] - self.asteroid_speed)

            if self.check_collision(self.hero, powerup):
                self.bullet_count += 50 
                self.update_score_label()
                self.canvas.remove(powerup)
                self.ammo_powerups.remove(powerup)

            elif powerup.pos[1] < 0:  # หากกระสุนหลุดจอ
                self.canvas.remove(powerup)
                self.ammo_powerups.remove(powerup)
        # ตรวจสอบการชนของ hero กับ asteroids
        for asteroid in self.asteroids:
            if self.check_collision(self.hero, asteroid):
                self.show_game_over()
                break

            if self.earth_health <= 0:
               self.show_game_over()
               break

        # เพิ่มระดับความยาก
        if self.score // 50 + 1 > self.level:
            self.level += 1
            self.update_speeds()
            self.update_score_label()

    def update_score_label(self):
        self.score_label.text = (f'Score: {self.score}\nHigh Score: {self.high_score}\n'
                         f'Level: {self.level}\nBullets: {self.bullet_count}')


    def check_collision(self, obj1, obj2):
        x1, y1 = obj1.pos
        w1, h1 = obj1.size
        x2, y2 = obj2.pos
        w2, h2 = obj2.size

        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)

    def reset_game(self):
        self.score = 0
        self.level = 1
        self.bullet_count = 100
        self.earth_health = 50
        self.game_over = False
        self.update_score_label()
        


class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(CharacterSelection(name='character_selection'))
        sm.add_widget(CharacterScreen(name='character_screen'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(GameOverScreen(name='game_over'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()