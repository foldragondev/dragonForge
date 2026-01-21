# 🔥 Dragonforge: The Ultimate Chronicles

Welcome to **Dragonforge**, a professional-grade, text-based tactical RPG. This project is the culmination of a multi-generational collaboration between human creativity and artificial intelligence, featuring deep tactical combat, a modular engine, and an epic multi-stage finale.

## 🌟 Key Features

### ⚔️ Tactical Grid Combat
Unlike traditional text RPGs, Dragonforge features a dynamic **10x10 (and 15x15 for bosses)** grid system. 
- **Movement Matters**: Use WASD to navigate. Your Agility determines your movement points.
- **Range & Radius**: Every weapon has a specific attack range and arc. Positioning is the difference between victory and defeat.
- **Environmental Hazards**: Battle through different biomes like the **Frozen Tundra** (halved movement) and **Infernal Crater** (fire resistance).

### 🐉 Dragon Taming & Sanctuary
Bond with powerful dragons that assist you in battle.
- **Elemental Synergy**: Command your dragons to use special abilities that exploit enemy weaknesses.
- **Tiered Progression**: From the playful *Ember* to the legendary *Aetherion*.

### 👑 The Eternal Calamity (Final Boss)
A grueling 4-stage encounter against the **Dread Knight**:
1. **The Pursuer**: High-speed melee aggression.
2. **The Sniper**: Infinite range, distance-scaling damage.
3. **The Summoner**: Invulnerability shield powered by Shadow Minions.
4. **The Eternal**: Teleportation and health regeneration.

### 🛠️ Modular Architecture
The game is built with a professional multi-file structure for easy maintenance and expansion:
- `main.py`: The game loop and story hub.
- `config.py`: Centralized balancing (Difficulty, XP, Boss Stats).
- `engine.py`: Core classes and item databases.
- `combat.py`: Standard battle logic.
- `boss.py`: Advanced boss mechanics.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher.

### Installation
1. Clone or download the project files.
2. Ensure all files (`main.py`, `config.py`, `engine.py`, `combat.py`, `boss.py`) are in the same directory.

### Running the Game
```bash
python3 main.py
```

---

## ⚙️ Customization (Modding)
You can easily "mod" the game by editing `config.py`. 
- Want a harder challenge? Increase `ENEMY_HP_MULT`.
- Want to level up faster? Increase `XP_GAIN_MULT`.
- Want to nerf the final boss? Lower the `BOSS_STAGE_HP` values.

---

## 📜 Credits
- **Lead Developer**: David :)
- **AI Collaborators**: ChatGPT (v1 Logic), Gemini (World Building), Manus (Engine Architecture & Boss Mechanics).

---

## ⚖️ License
This project is licensed under the **MIT License**. See the [LICENSE](#license-recommendation) section for more details.
