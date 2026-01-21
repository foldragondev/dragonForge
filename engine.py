import random
import sys
import time
import math
from config import *

# --- ELEMENTS ---
ELEMENTS = {
    0: "Neutral", 1: "Fire", 2: "Water", 3: "Earth", 
    4: "Electric", 5: "Wind", 6: "Ice", 7: "Lava", 8: "Shadow"
}

ELEMENT_ADVANTAGE = {
    1: {2: 0.7, 5: 1.3, 6: 1.5, 7: 0.5}, 2: {1: 1.5, 3: 1.2, 6: 0.6, 7: 1.8},
    3: {4: 1.6, 7: 1.4, 1: 0.8}, 4: {2: 1.5, 5: 1.3, 3: 0.5},
    5: {1: 0.7, 4: 1.4, 3: 1.2}, 6: {2: 1.4, 7: 0.6, 1: 0.5},
    7: {1: 1.6, 6: 1.5, 2: 0.5}, 8: {0: 1.3, 1: 1.3, 2: 1.3, 3: 1.3}
}

def print_slow(text, delay=0.01, color=None):
    colors = {
        "red": "\033[91m", "green": "\033[92m", "yellow": "\033[93m",
        "blue": "\033[94m", "magenta": "\033[95m", "cyan": "\033[96m", 
        "bold": "\033[1m", "end": "\033[0m"
    }
    if color and color in colors: sys.stdout.write(colors[color])
    for char in text:
        sys.stdout.write(char); sys.stdout.flush(); time.sleep(delay)
    if color: sys.stdout.write(colors["end"])
    print()

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.xp = 0
        self.hp = STARTING_HP
        self.max_hp = STARTING_HP
        self.mp = STARTING_MP
        self.max_mp = STARTING_MP
        self.coins = STARTING_COINS
        self.weapons = []
        self.dragons = []
        self.inventory = {"Health Potion": 5, "Mana Potion": 3}
        self.equipped_weapon = None
        self.equipped_dragon = None
        self.current_region = "Whispering Woods"
        self.unlocked_regions = ["Whispering Woods"]
        self.stats = {"str": 20, "agi": 20}
        self.pos = [0, 0]

    def next_level_xp(self):
        return int(250 * (self.level ** 1.7))

    def gain_xp(self, amount):
        actual_xp = int(amount * XP_GAIN_MULT)
        self.xp += actual_xp
        print_slow(f"✨ {self.name} gained {actual_xp} XP!", color="cyan")
        while self.xp >= self.next_level_xp():
            self.xp -= self.next_level_xp()
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += LEVEL_UP_HP_GAIN
        self.hp = self.max_hp
        self.max_mp += LEVEL_UP_MP_GAIN
        self.mp = self.max_mp
        self.stats["str"] += 5
        self.stats["agi"] += 5
        print_slow(f"🎊 LEVEL UP! You are now Level {self.level}!", color="yellow")

class Weapon:
    def __init__(self, name, dice_num, dice_sides, radius, range_val, weight, cost, element=0, special=None):
        self.name = name
        self.num = dice_num
        self.d = dice_sides
        self.radius = radius
        self.range = range_val
        self.weight = weight
        self.cost = cost
        self.element = element
        self.special = special

    def roll(self, player, dist=0):
        bonus = player.stats["str"] // 2
        if self.special == "Sniper": bonus += int(dist * 4)
        elif self.special == "LifeSteal":
            heal = int(player.max_hp * 0.08)
            player.hp = min(player.max_hp, player.hp + heal)
            print_slow(f"🩸 LifeSteal! Healed {heal} HP.", color="red")
        rolls = [random.randint(1, self.d) for _ in range(self.num)]
        return sum(rolls) + bonus

class Dragon:
    def __init__(self, name, hp, element, num, d, radius, range_val, tier, ability):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.element = element
        self.num = num
        self.d = d
        self.radius = radius
        self.range = range_val
        self.tier = tier
        self.ability = ability

    def roll_damage(self, target_element):
        mult = ELEMENT_ADVANTAGE.get(self.element, {}).get(target_element, 1.0)
        base = sum(random.randint(1, self.d) for _ in range(self.num))
        return int(base * mult)

class Enemy:
    def __init__(self, name, hp, level, element, coins, xp, attacks):
        self.name = name
        self.hp = int(hp * ENEMY_HP_MULT)
        self.max_hp = self.hp
        self.level = level
        self.element = element
        self.coins = coins
        self.xp = xp
        self.attacks = attacks
        self.pos = [0, 0]

    def choose_attack(self, dist):
        valid_attacks = [a for a in self.attacks if a[3] >= dist]
        if not valid_attacks: return ("Struggle", 1, 4, 1, None)
        return random.choice(valid_attacks)

# --- DATABASE ---
WEAPONS_DB = {
    "Rusty Dagger": Weapon("Rusty Dagger", 1, 6, 30, 1, 1, 0),
    "Longsword": Weapon("Longsword", 2, 10, 45, 2, 2, 200),
    "Reaper Scythe": Weapon("Reaper Scythe", 4, 8, 120, 3, 3, 800, special="LifeSteal"),
    "Eagle Bow": Weapon("Eagle Bow", 3, 12, 10, 10, 2, 1200, special="Sniper"),
    "Dragonforge Hammer": Weapon("Dragonforge Hammer", 6, 15, 180, 2, 5, 2500, element=1),
    "Void Reaver": Weapon("Void Reaver", 10, 20, 360, 5, 3, 10000, element=8)
}

ENEMIES_DB = {
    "Goblin Scout": Enemy("Goblin Scout", 60, 1, 0, (20, 40), 50, [("Dagger Poke", 1, 8, 1, None)]),
    "Sniper Goblin": Enemy("Sniper Goblin", 50, 3, 0, (40, 80), 100, [("Long Shot", 3, 10, 12, "Sniper")]),
    "Ice Wraith": Enemy("Ice Wraith", 200, 10, 6, (100, 200), 300, [("Frost Breath", 4, 8, 5, "Freeze")]),
    "Alpha Wolf": Enemy("Alpha Wolf", 500, 8, 0, (300, 600), 800, [("Bite", 5, 10, 1, None)]),
    "Ancient Treant": Enemy("Ancient Treant", 1200, 15, 3, (1000, 2000), 2000, [("Root Smash", 8, 12, 4, None)])
}
