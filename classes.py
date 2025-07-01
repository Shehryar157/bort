import pygame, time, random, menu, weapons
from speech import speak
from soundsystem import soundsystem
ss = soundsystem.get_instance()

class wall:
    def __init__(self, y=5, health=100, electrified=False):
        self.y = y
        self.health = health
        self.electrified = electrified

class player:
    def __init__(self, x=random.randint(1, 10), y=0, health=100, level=1, kills=0, weapon=None, weapons={weapons.m4.name: weapons.m4}, inv={}):
        self.x = x
        self.y = y
        self.health = health
        self.level = level
        self.kills = kills
        self.weapon = weapon
        self.weapons = weapons
        self.inv = inv
        self.lastMove_time = time.time()
    def move(self, direction):
        current_time = time.time()
        if current_time -self.lastMove_time >= 0.2:
            self.x += direction
            self.lastMove_time = time.time()
    def weapon_inv(self):
        m = menu.menu()
        def makemenu():
            m.reset() #Make sure nothing is left in our menu 
            for key in self.weapons:
                m.add_item(key)
            choice = m.run(intromsg="Weapons")
            print(m.menu_choices[choice])
            chosen_weapon_name = m.menu_choices[choice]
            chosen_weapon = self.weapons[chosen_weapon_name]
            if chosen_weapon == self.weapon:
                speak("You are already wielding this")
            else:
                chosen_weapon.draw(self)
        makemenu()
    def item_inv(self):
        m = menu.menu()
        def item_menu():
            m.reset() #Make sure nothing is left in our menu 
            for key, value in self.inv.items():
                if value > 0:
                    m.add_item(f"{key}, {value}")
            choice = m.run(intromsg="Inventory")
            print(m.menu_choices[choice])
        item_menu()

class enemy:
    def __init__(self, x, y, health, strength, speed, times_list, attack_timer):
        self.x = x
        self.y = y
        self.health = health
        self.strength= strength
        self.speed = speed
        self.times_list = [0.8, 0.9, 1, 1.2, 1.3, 1.5, 1.6]
        self.attack_timer = attack_timer
        self.attack_timer = time.time()
        self.lastmove_time = time.time()
        self.moving_sound = None
        self.damage_sound = "enemies/fence_damage1.ogg"
        self.impact_sound = "enemies/bullet impact1.ogg"
    def move(self, char, fence):
        glist = ["dirt", "grass"]
        ground_type = random.choice(glist)
        step_number = str(random.randint(1, 11)) + ".ogg"
        self.moving_sound = "footsteps/" + ground_type + "/step" + step_number
        print(self.moving_sound)
        timer = time.time()
        if timer - self.lastmove_time >= self.speed and self.y > fence.y:
            self.y -= 1
            ss.play(file=self.moving_sound, source_object=self)
            self.lastmove_time = timer
    def attack(self, char, fence):
        self.passed_time = time.time()
        self.rt = random.choice(self.times_list)
        if self.passed_time - self.attack_timer >= self.rt:
            fence.health -= self.strength
            ss.play(file=self.damage_sound, source_object=self)
            self.attack_timer = time.time()
    def check(self, char, fence):
        if self.health > 0:
            self.move(char, fence)
        if self.y == fence.y:
            self.attack(char, fence)

class zombie(enemy):
    def __init__(self, x, y, health, strength, speed, times_list, attack_timer):
        super().__init__(x, y, health, strength, speed, times_list, attack_timer)