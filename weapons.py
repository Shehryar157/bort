import pygame, time, random, menu, os
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
    def __init__(self, name, power, cal, shell_type, range, capacity, bullet_count, reloading, drawing, firing_timer, time_limit, ds_object, rs_object, drawing_sound, firing_sound, reload_sound, click):
        self.name = name
        self.power= power
        self.cal = cal
        self.shell_type = shell_type
        self.range = range
        self.capacity = capacity
        self.bullet_count = bullet_count
        self.drawing = drawing
        self.reloading = reloading
        self.firing_timer = firing_timer
        self.time_limit = time_limit
        self.ds_object = ds_object
        self.rs_object = rs_object
        self.drawing_sound = drawing_sound
        self.firing_sound = firing_sound
        self.reload_sound = reload_sound
        self.click = click
        self.firing_timer = time.time()
        self.reset()
    def draw(self, char):
        self.drawing = True
        char.weapon = self
        self.ds_object = ss.play(file=self.drawing_sound)
        return self.drawing_sound
    def fire(self, char):
        if self.bullet_count > 0:
            global bullets_list
            bullets_list.append(projectile(char.x, char.y+1, self.power))
            self.bullet_count -= 1
            firing_sounds = os.listdir("sounds/weapons/" + self.name)
            available_sounds = []
            for file in firing_sounds:
                if "fire" not in file:
                    firing_sounds.remove(file)
                else:
                    file = os.path.join("sounds/weapons/" + self.name, file)
                    available_sounds.append(file)
            available_sounds = [file.removeprefix("sounds/") for file in available_sounds]
            self.firing_sound = random.choice(available_sounds)
            ss.play(file=self.firing_sound, pitch=random.randint(90, 110))
            shelldrop_sound = "weapons/shells/" + self.shell_type + str(random.randint(1, 4)) + ".ogg"
            ss.play(file=shelldrop_sound)
            self.firing_timer = time.time()
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
    def reset(self):
        self.bullet_count = self.capacity

m4 = weapon("M4 rifle", random.randint(8, 10), "5.56 caliber rounds", "5.56 shells", 12, 30, 30, False, False, time.time(), 0.2, None, None, "weapons/m4 rifle/draw.ogg", "weapons/m4 rifle/fire1.ogg", "weapons/m4 rifle/reload.ogg", "weapons/m4 rifle/click.ogg")
glock17 = weapon("glock17", random.randint(3, 4), "9mm", "9mm shells", 9, 17, 17, False, False, time.time(), 0.4, None, None, "weapons/glock17/draw.ogg", "weapons/glock17/fire1.ogg", "weapons/glock17/reload.ogg", "weapons/glock17/click.ogg")