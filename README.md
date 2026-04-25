# 🎮 Tile Wars

Play / Download: https://dodd623.itch.io/tile-wars

Tile Wars is a turn-based territory control game built in Python using Pygame. Players compete to dominate a grid by expanding into neutral territory and capturing opponents’ tiles, with AI-driven chaos ensuring every match plays out differently.

---

## 🧠 Overview

Tile Wars is designed around simple rules that create complex and unpredictable outcomes. The game supports both human and AI players, allowing for interactive play or full AI simulations.

The focus of the project is on:
- Game state management
- AI decision-making
- Emergent gameplay systems

---

## ⚙️ Features

- 1–8 player support (any mix of human and AI)
- AI vs AI simulation mode
- Randomized capture system (RNG-based outcomes)
- Domination victory condition
- Player elimination system
- Adjustable grid sizes (10x10 → 20x20)
- Real-time controls (pause, speed up, step turns)
- Event log for tracking game actions

---

## 🎮 Controls

### Setup Screen
- `UP/DOWN` → Change total players
- `LEFT/RIGHT` → Change number of human players
- `G` → Change grid size
- `TAB` → Select player
- `C` → Change player color
- `N` → Rename player
- `SPACE` → Start game

### In-Game
- `+ / -` → Adjust AI speed
- `P` → Pause / Resume
- `N` → Step one turn
- `R` → Restart match
- `H` → Return to setup

---

## 🏗️ Tech Stack

- Python
- Pygame
- Object-Oriented Design

---

## 🚀 Installation

### Option 1: Download (Recommended)
Download the game here:
👉 https://dodd623.itch.io/tile-wars

1. Download the `.zip`
2. Extract the files
3. Run `TileWars.exe`

---

### Option 2: Run from source

```bash
git clone https://github.com/dodd623/tile-wars.git
cd tile-wars
pip install pygame
python main.py
