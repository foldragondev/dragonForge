import random
import os
from engine import *
from combat import battle
from boss import final_boss_fight

def show_credits():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_slow("🔥 DRAGONFORGE: THE ULTIMATE CHRONICLES 🔥", color="yellow")
    print_slow("\n--- CREDITS ---")
    print_slow("Lead Developer: David :)")
    print_slow("AI Collaborators: ChatGPT, Gemini, Manus")
    print_slow("\nTHANK YOU FOR PLAYING!")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_slow("🔥 DRAGONFORGE: THE ULTIMATE CHRONICLES 🔥", color="yellow", delay=0.05)
    name = input("Enter your name, Hero: ")
    p = Player(name)
    p.equipped_weapon = WEAPONS_DB["Rusty Dagger"]
    p.weapons.append(WEAPONS_DB["Rusty Dagger"])
    
    REGIONS = {
        "Whispering Woods": {"enemies": ["Goblin Scout", "Sniper Goblin"], "boss": "Ancient Treant"},
        "Frozen Tundra": {"enemies": ["Ice Wraith"], "boss": "Alpha Wolf"}
    }

    while True:
        print(f"\n📍 {p.current_region} | ❤️ {p.hp}/{p.max_hp} | 💰 {p.coins} | Lvl {p.level}")
        print("-" * 40)
        print("1. Adventure | 2. Shop | 3. Sanctuary | 4. Stats | 5. FINAL BOSS | 6. Quit")
        
        choice = input("> ")
        
        if choice == "1":
            reg = REGIONS[p.current_region]
            enemy = random.choice(reg['enemies'])
            battle(p, enemy)
        elif choice == "2":
            print(f"Coins: {p.coins}")
            shop_items = list(WEAPONS_DB.values())[1:]
            for i, w in enumerate(shop_items):
                print(f"{i+1}. {w.name} ({w.cost})")
            try:
                c = int(input("Buy: "))
                w = shop_items[c-1]
                if p.coins >= w.cost:
                    p.coins -= w.cost; p.weapons.append(w); p.equipped_weapon = w
                    print(f"Equipped {w.name}!")
            except: pass
        elif choice == "3":
            if p.level >= 3 and not p.dragons:
                d = Dragon("Ember", 200, 1, 5, 10, 45, 3, 1, "Fire Blast")
                p.dragons.append(d); p.equipped_dragon = d
                print_slow("🐉 Ember joined!")
            elif p.dragons:
                print("You already have a dragon companion.")
        elif choice == "4":
            print(f"Lvl: {p.level} | Weapon: {p.equipped_weapon.name}")
            input("Enter to continue...")
        elif choice == "5":
            if p.level < 15: print("Too weak! Need Lvl 15.")
            else:
                if final_boss_fight(p):
                    show_credits()
                    break
        elif choice == "6": break

if __name__ == "__main__":
    main()
