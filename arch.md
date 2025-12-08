# Arch

```bash
adventure-game/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── game/
│   ├── __init__.py
│   ├── engine.py         # Game logic (parser, commands)
│   ├── world.py          # Rooms, items, NPCs
│   ├── player.py         # Player state
│   └── commands.py       # Command handlers
├── static/
│   ├── css/
│   │   └── terminal.css  # Retro terminal styling
│   └── js/
│       └── terminal.js   # Optional enhancements
├── templates/
│   └── index.html        # Main game interface
└── data/
    └── game_state.json   # Save game data (or SQLite)
```
---
# Arch with ansible
```bash
adventure-game/
├── app.py
├── requirements.txt
├── config.py              # Configuration management
├── .env.example           # Environment variables template
├── game/
│   ├── __init__.py
│   ├── engine.py
│   ├── world.py
│   ├── player.py
│   ├── commands.py
│   └── models/           # Modular content
│       ├── __init__.py
│       ├── enemies.py    # Enemy classes/data
│       ├── dungeons.py   # Map definitions
│       ├── treasures.py  # Item/treasure data
│       ├── scenarios.py  # Campaign scenarios
│       └── base.py       # Base classes
├── static/
│   ├── css/
│   │   └── terminal.css
│   ├── js/
│   │   └── terminal.js
│   └── fonts/           # Optional retro fonts
├── templates/
│   └── index.html
├── data/
│   ├── game_state.json
│   └── scenarios/       # JSON scenario definitions
├── ansible/
│   ├── playbook.yml     # Main deployment playbook
│   ├── inventory.ini    # Pi host configuration
│   └── roles/
│       ├── nginx/
│       ├── python/
│       └── app-deploy/
└── scripts/
    └── deploy.sh        # Quick deploy helper
```
