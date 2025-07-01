import pygame, time, random, menu
from speech import speak
from soundsystem import soundsystem
ss = soundsystem.get_instance()

bullets_list = []

class projectile:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self    .lastshot_time = time.time()
    def move(self):
        current_time = time.time()
        if current_time - self.lastshot_time>= 0.01:
            self.y += 1
            self.lastshot_time = time.time()


class magazine:
    def __init__(self, type, bullets):
        self.type = type
        self.bullets = bullets

mag1 = magazine("9MM", 15)

class weapon:
    def __init__(self, name, power, cal, range, capacity, bullet_count, reloading, drawing, ds_object, rs_object, drawing_sound, firing_sound, reload_sound, click):
        self.name = name
        self.power= power
        self.cal = cal
        self.range = range
        self.capacity = capacity
        self.bullet_count = bullet_count
        self.drawing = drawing
        self.reloading = reloading
        self.ds_object = ds_object
        self.rs_object = rs_object
        self.drawing_sound = drawing_sound
        self.firing_sound = firing_sound
        self.reload_sound = reload_sound
        self.click = click
    def draw(self, char):
        self.drawing = True
        char.weapon = self
        self.drawing_sound= ss.play(file=self.drawing_sound)
        return self.drawing_sound
    def fire(self, char):
        if self.bullet_count > 0:
            global bullets_list
            bullets_list.append(projectile(char.x, char.y+1, self.power))
            self.bullet_count -= 1
            ss.play(file=self.firing_sound)
        else:
            ss.play(file=self.click)
    def reload(self, char):
        if self.reloading == True: return
        needed_mag = self.cal
        if needed_mag in char.inv and char.inv[needed_mag] > 0:
            required_bullets = self.capacity - self.bullet_count
            transferable_bullets = min(required_bullets, char.inv[needed_mag])
            self.reloading = True
            self.bullet_count += transferable_bullets
            char.inv[needed_mag] -= transferable_bullets
            self.rs_object= ss.play(file=self.reload_sound)
    def check(self):
        if self.ds_object is not None and self.ds_object.playing:
            pass
        else:
            self.drawing = False
            self.ds_object = None
        if self.rs_object is not None and self.rs_object.playing:
            pass
        else:
            self.reloading = False
            self.rs_object = None

m4 = weapon("M4 rifle", random.randint(8, 10), "5.56 caliber rounds", 12, 30, 30, False, False, None, None, "weapons/m4/draw.ogg", "weapons/m4/fire.ogg", "weapons/m4/reload.ogg", "weapons/m4/click.ogg")