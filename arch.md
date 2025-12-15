# Arch

```bash
dailydungeon/
├── app.py                      # Flask entry point
├── requirements.txt
├── config.py                   # Environment-based config
├── .env.example
├── deploy.sh                   # Manual deployment
├── game/
│   ├── __init__.py
│   ├── engine.py              # Core game logic (migrate from OnlyDungeons.py)
│   ├── world.py               # Rooms, locations
│   ├── player.py              # Player state & progression
│   ├── commands.py            # Command parser
│   └── models/
│       ├── __init__.py
│       ├── enemies.py
│       ├── items.py
│       └── dungeons.py
├── static/
│   ├── css/
│   │   └── terminal.css       # Move from dev/
│   └── js/
│       └── terminal.js
├── templates/
│   ├── base.html
│   └── index.html             # Move from dev/
├── data/
│   └── .gitkeep              # SQLite DB will go here
├── tests/                     # Future unit tests
│   └── __init__.py
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions
├── .gitignore
└── README.md
```