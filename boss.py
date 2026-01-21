import random
import math
from engine import *
from config import *
from combat import draw_grid

def final_boss_fight(player):
    grid_size = GRID_SIZE_BOSS
    stage = 1
    minions = []
    
    while stage <= 4 and player.hp > 0:
        print_slow(f"\n--- BOSS STAGE {stage} ---", color="yellow")
        boss_pos = [0, 7]
        player.pos = [14, 7]
        stage_hp = [BOSS_STAGE_1_HP, BOSS_STAGE_2_HP, BOSS_STAGE_3_HP, BOSS_STAGE_4_HP][stage-1]
        
        if stage == 3:
            minions = []
            for _ in range(4):
                m = Enemy("Minion", 200, 10, 0, (0,0), 0, [("Bolt", 2, 6, 5, None)])
                m.pos = [random.randint(0, 14), random.randint(0, 14)]
                minions.append(m)

        while stage_hp > 0 and player.hp > 0:
            draw_grid(player.pos, boss_pos, size=grid_size, minions=minions)
            print(f"❤️ {player.name}: {player.hp}/{player.max_hp} | 😈 Boss: {stage_hp} HP")
            if minions: print(f"🛡️ Minions active: {len(minions)}")
            choice = input("1. Move | 2. Attack | 3. Item > ")
            
            if choice == "1":
                move_pts = 3
                for _ in range(move_pts):
                    m = input("Dir: ").lower()
                    dx, dy = 0, 0
                    if m == 'w': dy = -1
                    elif m == 's': dy = 1
                    elif m == 'a': dx = -1
                    elif m == 'd': dx = 1
                    player.pos = [max(0, min(14, player.pos[0]+dx)), max(0, min(14, player.pos[1]+dy))]
            
            elif choice == "2":
                target_pos = boss_pos
                is_minion = False
                if minions:
                    print("Select target: 1. Boss " + " ".join([f"{i+2}. Minion {i+1}" for i in range(len(minions))]))
                    try:
                        t_choice = int(input("> "))
                        if t_choice > 1:
                            target_pos = minions[t_choice-2].pos
                            is_minion = True
                    except: pass
                
                dist = math.sqrt((player.pos[0]-target_pos[0])**2 + (player.pos[1]-target_pos[1])**2)
                if dist <= player.equipped_weapon.range:
                    if stage == 3 and not is_minion:
                        print_slow("🛡️ The Boss is shielded by minions!", color="cyan")
                    else:
                        dmg = player.equipped_weapon.roll(player, dist)
                        if is_minion:
                            minions[t_choice-2].hp -= dmg
                            if minions[t_choice-2].hp <= 0:
                                print_slow("💥 Minion destroyed!")
                                minions.pop(t_choice-2)
                        else:
                            stage_hp -= dmg
                            print_slow(f"💥 Dealt {dmg} damage to Dread Knight!")
                else: print("❌ Out of range!")

            elif choice == "3":
                if player.inventory["Health Potion"] > 0:
                    player.hp = min(player.max_hp, player.hp + POTION_HEAL_AMOUNT)
                    player.inventory["Health Potion"] -= 1
                    print_slow(f"🧪 Healed {POTION_HEAL_AMOUNT} HP!")

            # Boss Logic
            if stage == 1: # Fast
                for _ in range(10):
                    if boss_pos[0] < player.pos[0]: boss_pos[0] += 1
                    elif boss_pos[0] > player.pos[0]: boss_pos[0] -= 1
                    if boss_pos[1] < player.pos[1]: boss_pos[1] += 1
                    elif boss_pos[1] > player.pos[1]: boss_pos[1] -= 1
                if math.sqrt((player.pos[0]-boss_pos[0])**2 + (player.pos[1]-boss_pos[1])**2) <= 1.5:
                    player.hp -= 40
                    print_slow("⚠️ Boss strikes!")
            elif stage == 2: # Sniper
                dmg = 60 + int(math.sqrt((player.pos[0]-boss_pos[0])**2 + (player.pos[1]-boss_pos[1])**2) * 2)
                player.hp -= dmg
                print_slow(f"🎯 Sniper shot! Dealt {dmg}!")
            elif stage == 3: # Minions
                for m in minions:
                    if math.sqrt((player.pos[0]-m.pos[0])**2 + (player.pos[1]-m.pos[1])**2) <= 5:
                        player.hp -= 20
                        print_slow("⚠️ Minion attacks!")
            elif stage == 4: # Regen & Teleport
                stage_hp += BOSS_REGEN_PER_TURN
                boss_pos = [random.randint(0, 14), random.randint(0, 14)]
                player.hp -= 80
                print_slow("🌀 Teleport & Burst!")

        if player.hp <= 0:
            if input("Reattempt? (y/n): ").lower() == 'y':
                player.hp = player.max_hp
                return final_boss_fight(player)
            return False
        stage += 1
    
    if stage > 4:
        return True
    return False
