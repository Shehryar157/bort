import pygame, time, random, menu, weapons
from speech import speak
from soundsystem import soundsystem
ss = soundsystem.get_instance()

things = []
class wall:
    def __init__(self, y=5, health=100, electrified=False):
        self.y = y
        self.health = health
        self.electrified = electrified

class player:
    def __init__(self, x=random.randint(1, 10), y=0, health=100, accuracy=100, score=0, cash=0, kills=0, weapon=None, weapons={weapons.m4.name: weapons.m4}, inv={}):
        self.x = x
        self.y = y
        self.health = health
        self.accuracy = accuracy
        self.score = score
        self.cash = cash
        self.kills = kills
        self.weapon = weapon
        self.weapons = weapons
        self.inv = inv
        self.lastMove_time = time.time()
        self.last_comms_point = 0
        self.required_kills = 1
        self.used_comms = False
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
        item_menu()
    def comms(self):
        comms_menu = menu.menu()
        def make_comms_menu():
            comms_menu.reset()
            comms_menu.add_item("Request .9MM ammo")
            comms_menu.add_item("Request 5.56 caliber ammo")
            comms_menu.add_item("Request 7.62 caliber ammo")
            choice = comms_menu.run()
            if comms_menu.menu_choices[choice] == "Request .9MM ammo":
                self.inv[".9MM rounds"] = self.inv.get(".9MM rounds", 0) + 60
            elif comms_menu.menu_choices[choice] == "Request 5.56 caliber ammo":
                self.inv["5.56 caliber rounds"] = self.inv.get("5.56 caliber rounds", 0) + 60
            elif comms_menu.menu_choices[choice] == "Request 7.62 caliber ammo":
                self.inv["7.62 caliber rounds"] = self.inv.get("7.62 caliber rounds", 0) + 60
            self.used_comms = True
        make_comms_menu()

class enemy:
    def __init__(self, score, x, y, health, strength, speed, times_list, attack_timer, loot_sound="items/money_loop1.ogg", bodyfall=None):
        self.score = score
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
        self.bodyfall = bodyfall
        self.loot_sound = loot_sound
    def move(self, char, fence):
        glist = ["dirt", "grass"]
        ground_type = random.choice(glist)
        step_number = str(random.randint(1, 11)) + ".ogg"
        self.moving_sound = "footsteps/" + ground_type + "/step" + step_number
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
    def death(self, char):
        char.score += self.score + (4 if self.y >= 21 else 2 if self.y >= 13 else 0)
        ss.play(file=self.bodyfall, source_object=self)
        global things
        things.append(currency("Dinar", random.randint(200, 350), self.x, 0, "items/money_loop1.ogg", "items/get_Dinar1.ogg"))

class zombie(enemy):
    def __init__(self, score, x, y, health, strength, speed, times_list, attack_timer, loot_sound="items/money_loop1.ogg", bodyfall=None):
        if bodyfall is None:
            bodyfall = "actions/bodyfall" + str(random.randint(1, 3)) + ".ogg"
        super().__init__(score, x, y, health, strength, speed, times_list, attack_timer, loot_sound, bodyfall)

class item:
    def __init__(self, name, x, y, static_sound, pickup_sound):
        self.name = name
        self.x = x
        self.y = y
        self.static_sound = static_sound
        self.pickup_sound = pickup_sound
        self.static_sound_obj = None
        self.loop_sound()
    def get(self, char):
        ss.play(file=self.pickup_sound, pan=25)
        speak(f"{self.name}")
        if self.name == "Dinar" and self.amount:
            char.cash += self.amount
        else:
            char.inv[self.name] = self
        self.static_sound_obj.stop()
    def loop_sound(self):
        if self.static_sound_obj is None or not self.static_sound_obj.playing:
            self.static_sound_obj = ss.play(file=self.static_sound, looping=True, source_object=self)

class currency(item):
    def __init__(self, name, amount, x, y, static_sound, pickup_sound):
        super().__init__(name, x, y, static_sound, pickup_sound)
        self.amount = amount