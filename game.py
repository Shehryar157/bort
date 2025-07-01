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

def startGame():
    
    ss.set_music("music/game1.ogg", volume=25)
    clock = pygame.time.Clock()
    char = classes.player(random.randint(1, 10), 0, 100, 1, 0, None, {weapons.m4.name: weapons.m4}, {})
    _9mm_cal_bullets = 45
    _556cal_bullets = 90
    _762cal_bullets = 0
    char.inv[".9MM rounds"] = _9mm_cal_bullets
    char.inv["5.56 caliber rounds"] = _556cal_bullets
    char.inv["7.62 caliber rounds"] = _762cal_bullets
    spawned_zombies = 0
    fence = classes.wall(5, 100, False)
    zombies = []
    zombies.append(classes.zombie(random.randint(1, 10), random.randint(21, 25), 10, random.randint(5, 8), 0.7, [0.8, 0.9, 1, 1.2, 1.3, 1.5, 1.6], time.time()))
    wave = 1
    enemy_number = 10
    fence = classes.wall(5, 100, False)
    spawn_timer = time.time()
    while fence.health > 0:
        ss.update_spatial_audio(char.x, char.y)
        if char.weapon is not None:
            char.weapon.check()
        wave_enemies = wave*enemy_number
        if char.kills == wave_enemies:
            wave += 1
        if time.time() - spawn_timer >= random.randint(3, 5):
            zombies.append(classes.zombie(random.randint(1, 10), random.randint(21, 25), 10, random.randint(5, 8), 0.7, [0.8, 0.9, 1, 1.2, 1.3, 1.5, 1.6], time.time()))
            spawned_zombies += 1
            spawn_timer = time.time()
        for undead in zombies:
            undead.check(char, fence)
        bullets_for_removal = []
        enemies_for_removal = []
        for bullet in list(weapons.bullets_list):
            bullet.move()
            for enemy_obj in list(zombies):
                if bullet.x == enemy_obj.x and bullet.y == enemy_obj.y:
                    enemy_obj.health -= bullet.damage
                    ss.play(file=enemy_obj.impact_sound, source_object=enemy_obj)
                    if bullet in weapons.bullets_list:
                        weapons.bullets_list.remove(bullet)
                    if enemy_obj.health <= 0:
                        zombies.remove(enemy_obj)
                        char.kills += 1
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
                        #pan, volume = topdown_audio.play_sound(char.x, char.y, 0, 0)
                        #bump.pan = pan
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                    if char.x != 10:
                        char.move(direction)
                    else:
                        ss.play(file="actions/bump.ogg")
                        #pan, volume = topdown_audio.play_sound(char.x, char.y, 11, 0)
                        #bump.pan = pan
                        #bump.volume = 0 - volume
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
                elif event.key == pygame.K_a and char.weapon is not None:
                    speak(f"{char.weapon.bullet_count}")
                elif event.key == pygame.K_r and char.weapon is not None and char.weapon.bullet_count < char.weapon.capacity and char.weapon.reloading == False:
                    char.weapon.reload(char)
                elif event.key == pygame.K_SPACE and char.weapon is not None and char.weapon.drawing == False and char.weapon.reloading == False:
                    char.weapon.fire(char)
        if fence.health <= 0:
            break
        clock.tick(60)
    m2 = menu.menu()
    def postgame_menu():
        while True:
            m2.reset()
            m2.add_item(f"You were overrun at level {char.level}")
            m2.add_item(f"About {spawned_zombies} zombies spawned on the field")
            m2.add_item(f"You took down {char.kills} zombies")
            choice = m2.run(intromsg="Post game stats")
            break
        
    postgame_menu()

main()