import random
import math
from engine import *
from config import *

def draw_grid(player_pos, enemy_pos, size=10, minions=None):
    print("\n" + "—" * (size * 2 + 2))
    for y in range(size):
        row = "|"
        for x in range(size):
            if [x, y] == player_pos: row += " P"
            elif [x, y] == enemy_pos: row += " E"
            elif minions and [x, y] in [m.pos for m in minions]: row += " m"
            else: row += " ."
        print(row + " |")
    print("—" * (size * 2 + 2))

def battle(player, enemy_name, is_boss=False):
    enemy_template = ENEMIES_DB.get(enemy_name)
    if enemy_template is None:
        print_slow(f"⚠️ Error: Enemy '{enemy_name}' not found!", color="red")
        return False

    enemy = Enemy(enemy_template.name, enemy_template.max_hp, enemy_template.level, 
                  enemy_template.element, enemy_template.coins, enemy_template.xp, 
                  enemy_template.attacks)
    
    grid_size = GRID_SIZE_NORMAL
    player.pos = [grid_size-1, grid_size//2]
    enemy.pos = [0, grid_size//2]
    
    print_slow(f"\n⚔️  BATTLE START: {player.name} vs {enemy.name}!", color="red")
    
    while player.hp > 0 and enemy.hp > 0:
        draw_grid(player.pos, enemy.pos, size=grid_size)
        print(f"❤️ {player.name}: {player.hp}/{player.max_hp} | 😈 {enemy.name}: {enemy.hp}/{enemy.max_hp}")
        print("1. Move | 2. Attack | 3. Item | 4. Flee")
        choice = input("> ")
        
        if choice == "1":
            move_pts = max(1, (player.stats["agi"] // 5) + random.randint(1, 3))
            for _ in range(move_pts):
                m = input("Dir (WASD): ").lower()
                dx, dy = 0, 0
                if m == 'w': dy = -1
                elif m == 's': dy = 1
                elif m == 'a': dx = -1
                elif m == 'd': dx = 1
                player.pos = [max(0, min(grid_size-1, player.pos[0]+dx)), max(0, min(grid_size-1, player.pos[1]+dy))]
            
        elif choice == "2":
            dist = math.sqrt((player.pos[0]-enemy.pos[0])**2 + (player.pos[1]-enemy.pos[1])**2)
            if dist <= player.equipped_weapon.range:
                dmg = player.equipped_weapon.roll(player, dist)
                enemy.hp -= dmg
                print_slow(f"💥 Dealt {dmg} damage!")
            else: print_slow("❌ Out of range!")

        elif choice == "3":
            if player.inventory["Health Potion"] > 0:
                player.hp = min(player.max_hp, player.hp + POTION_HEAL_AMOUNT)
                player.inventory["Health Potion"] -= 1
                print_slow(f"🧪 Healed {POTION_HEAL_AMOUNT} HP!")

        elif choice == "4":
            if not is_boss: return False
            print("❌ Cannot flee from a boss!")

        if enemy.hp > 0:
            dist = math.sqrt((player.pos[0]-enemy.pos[0])**2 + (player.pos[1]-enemy.pos[1])**2)
            if dist > 1.5:
                if enemy.pos[0] < player.pos[0]: enemy.pos[0] += 1
                elif enemy.pos[0] > player.pos[0]: enemy.pos[0] -= 1
            atk_name, a_num, a_d, a_range, a_spec = enemy.choose_attack(dist)
            e_dmg = int(sum(random.randint(1, a_d) for _ in range(a_num)) * ENEMY_DMG_MULT)
            player.hp -= e_dmg
            print_slow(f"⚠️ {enemy.name} uses {atk_name} for {e_dmg}!")

    if player.hp <= 0: return False
    player.gain_xp(enemy.xp)
    player.coins += int(random.randint(*enemy.coins) * COIN_DROP_MULT)
    return True
