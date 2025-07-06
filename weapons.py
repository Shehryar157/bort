import pygame, time, random, menu, os, json
from speech import speak
from soundsystem import soundsystem
ss = soundsystem.get_instance()

unlocked_weapons = {}
locked_weapons = {}
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
    def __init__(self, name, power, cal, shell_type, range, capacity, bullet_count, price, reloading, drawing, firing_timer, time_limit, ds_object, rs_object, drawing_sound, firing_sound, reload_sound, click):
        self.name = name
        self.power= power
        self.cal = cal
        self.shell_type = shell_type
        self.range = range
        self.capacity = capacity
        self.bullet_count = bullet_count
        self.price = price
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
            available_sounds = [
                os.path.join("sounds/weapons", self.name, file)
                for file in os.listdir(os.path.join("sounds/weapons", self.name))
                if "fire" in file
            ]
            print(available_sounds)
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
    def buy(self, wealth_value):
        unlocked_weapons[self.name] = self
        wealth_value -= self.price
        ss.play(file="actions/buy" + str(random.randint(1, 3)) + ".ogg")
        speak(f"Purchased {self.name}")
        with open("game data/data.json", "r") as file:
            essential_stats = json.load(file)
        essential_stats["money"] = wealth_value
        with open("game data/data.json", "w") as file:
            json.dump(essential_stats, file)

m4 = weapon("M4 rifle", random.randint(8, 10), "5.56 caliber rounds", "5.56 shells", 12, 30, 30, None, False, False, time.time(), 0.2, None, None, "weapons/m4 rifle/draw.ogg", "weapons/m4 rifle/fire1.ogg", "weapons/m4 rifle/reload.ogg", "weapons/m4 rifle/click.ogg")
glock17 = weapon("glock17", random.randint(3, 4), ".9MM rounds", "9mm shells", 9, 17, 17, None, False, False, time.time(), 0.4, None, None, "weapons/glock17/draw.ogg", "weapons/glock17/fire1.ogg", "weapons/glock17/reload.ogg", "weapons/glock17/click.ogg")
mp5 = weapon("mp5 sub-machinegun", random.randint(6, 9), ".9MM rounds", "9mm shells", 12, 30, 30, 2000, False, False, time.time(), 0.15, None, None, "weapons/mp5 sub-machinegun/draw.ogg", "weapons/mp5 sub-machinegun/fire1.ogg", "weapons/mp5 sub-machinegun/reload.ogg", "weapons/mp5 sub-machinegun/click.ogg")

locked_weapons[mp5.name] = mp5
unlocked_weapons[m4.name] = m4
unlocked_weapons[glock17.name] = glock17

all_weapons = {
    m4.name: m4,
    glock17.name: glock17,
    mp5.name: mp5
}