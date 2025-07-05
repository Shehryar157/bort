import pygame, menu, classes, time, random, weapons
from speech import speak
from soundsystem import soundsystem
ss = soundsystem.get_instance()
pygame.init()
pygame.display.set_mode((600, 400))
pygame.display.set_caption("menu")
m = menu.menu()
def main():
    while True:
        ss.set_music("music/menumusic.ogg", volume=50)
        m.reset() #Make sure nothing is left in our menu 
        m.add_item("play")
        m.add_item("store")
        m.add_item("exit")
        choice = m.run(intromsg="Hello")
        print(m.menu_choices[choice])
        if m.menu_choices[choice] == "play":
            startGame()
        elif m.menu_choices[choice] == "exit":
            break

def startGame():
    ss.set_music("music/game1.ogg", volume=20)
    clock = pygame.time.Clock()
    char = classes.player(random.randint(1, 10), 0, 100, "100%", 0, 0, 0, None, {weapons.m4.name: weapons.m4, weapons.glock17.name: weapons.glock17}, {})
    for firearm in char.weapons:
        char.weapons[firearm].reset()
    _9mm_cal_bullets = 45
    _556cal_bullets = 90
    _762cal_bullets = 0
    char.inv[".9MM rounds"] = _9mm_cal_bullets
    char.inv["5.56 caliber rounds"] = _556cal_bullets
    char.inv["7.62 caliber rounds"] = _762cal_bullets
    fired_shots = 0
    successful_shots = 0
    spawned_zombies = 0
    min_spawn_time = 7
    max_spawn_time = 10
    fence = classes.wall(4, 100, False)
    zombies = []
    zombies.append(classes.zombie(3, random.randint(1, 10), random.randint(21, 25), 10, random.randint(3, 5), 0.7, [0.8, 0.9, 1, 1.2, 1.3, 1.5, 1.6], time.time()))
    wave = 1
    progress_to_wave = 0
    enemy_number = 5
    spawn_timer = time.time()
    while fence.health > 0:
        char.accuracy = 100 if fired_shots == 0 and successful_shots == 0 else successful_shots * 100 / fired_shots
        if progress_to_wave >= enemy_number:
            wave += 1
            enemy_number = wave * 5
        ss.update_spatial_audio(char.x, char.y)
        if char.weapon is not None:
            char.weapon.check()
        wave_enemies = wave*enemy_number
        if char.kills == wave_enemies:
            wave += 1
        if wave in (1, 2):
            min_spawn = 7
            max_spawn = 10
        elif wave in (3, 4):
            min_spawn = 6
            max_spawn = 9
        elif wave in (5, 6):
            min_spawn = 5
            max_spawn = 8
        elif wave in (7, 8, 9):
            min_spawn = 4
            max_spawn = 7
        elif wave in (10, 11):
            min_spawn = 3
            max_spawn = 7
        elif wave in (12, 13, 14):
            min_spawn = 2
            max_spawn = 5
        elif wave >= 15:
            min_spawn = 1
            max_spawn = 5
        if time.time() - spawn_timer >= random.randint(min_spawn_time, max_spawn_time):
            zombies.append(classes.zombie(3, random.randint(1, 10), random.randint(21, 25), 10, random.randint(3, 5), 0.9, [0.8, 0.9, 1, 1.2, 1.3, 1.5, 1.6], time.time()))
            spawned_zombies += 1
            spawn_timer = time.time()
        for undead in zombies:
            undead.check(char, fence)
        for thing in list(classes.things):
            if thing.x == char.x and thing.y == char.y:
                thing.get(char)
                classes.things.remove(thing)
        bullets_for_removal = []
        enemies_for_removal = []
        for bullet in list(weapons.bullets_list):
            bullet.move()
            for enemy_obj in list(zombies):
                if bullet.x == enemy_obj.x and bullet.y == enemy_obj.y:
                    enemy_obj.health -= bullet.damage
                    successful_shots += 1
                    ss.play(file=enemy_obj.impact_sound, source_object=enemy_obj)
                    if bullet in weapons.bullets_list:
                        weapons.bullets_list.remove(bullet)
                    if enemy_obj.health <= 0:
                        enemy_obj.death(char)
                        zombies.remove(enemy_obj)
                        char.kills += 1
                        progress_to_wave += 1
                        char.last_comms_point += 1
                        if char.last_comms_point >= char.required_kills and char.used_comms == True:
                            char.last_comms_point= 0
                            char.used_comms = False
                if bullet.y >= char.weapon.range and bullet in weapons.bullets_list:
                    weapons.bullets_list.remove(bullet)
                    break
        for enemy_obj in enemies_for_removal:
            if enemy_obj in zombies:
                zombies.remove(enemy_obj)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = -1
                    if char.x != 1:
                        char.move(direction)
                    else:
                        ss.play(file="actions/bump.ogg")
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                    if char.x != 10:
                        char.move(direction)
                    else:
                        ss.play(file="actions/bump.ogg")
                elif event.key == pygame.K_c:
                    speak(f"{char.x}")
                elif event.key == pygame.K_w:
                    char.weapon_inv()
                elif event.key == pygame.K_i:
                    char.item_inv()
                elif event.key == pygame.K_h:
                    speak(f"{fence.health}")
                elif event.key == pygame.K_k:
                    speak(f"{char.kills}")
                elif event.key == pygame.K_l:
                    speak(f"{wave}")
                elif event.key == pygame.K_e:
                    speak(f"{round(char.accuracy, 2)}%")
                elif event.key == pygame.K_ESCAPE:
                    break
                elif event.key == pygame.K_s:
                    speak(f"{char.score} score")
                elif event.key == pygame.K_m:
                    speak(f"{char.cash} Dinar")
                elif event.key == pygame.K_o and char.last_comms_point >= char.required_kills and char.used_comms == False:
                    char.comms()
                elif event.key == pygame.K_a and char.weapon is not None:
                    speak(f"{char.weapon.bullet_count}")
                elif event.key == pygame.K_r and char.weapon is not None and char.weapon.bullet_count < char.weapon.capacity and char.weapon.reloading == False:
                    char.weapon.reload(char)
                elif event.key == pygame.K_SPACE and char.weapon is not None and char.weapon.drawing == False and char.weapon.reloading == False and time.time() - char.weapon.firing_timer >= char.weapon.time_limit:
                    char.weapon.fire(char)
                    fired_shots += 1
        if fence.health <= 0:
            break
            ss.destroy()
        clock.tick(60)
    m2 = menu.menu()
    def postgame_menu():
        while True:
            m2.reset()
            m2.add_item(f"You were overrun at wave {wave}")
            m2.add_item(f"About {spawned_zombies} zombies spawned on the field")
            m2.add_item(f"You took down {char.kills} zombies")
            choice = m2.run(intromsg="Post game stats")
            break
        
    postgame_menu()

main()