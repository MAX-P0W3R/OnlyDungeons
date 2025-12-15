from flask import Flask, render_template, request, session, jsonify
from config import config
import os
import sqlite3
from pathlib import Path

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Ensure data directory exists
    Path('data').mkdir(exist_ok=True)
    
    return app

app = create_app(os.environ.get('FLASK_ENV', 'production'))

def get_db():
    """Get database connection"""
    db = sqlite3.connect(app.config['DATABASE_PATH'])
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = get_db()
    
    # Players table
    db.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Game sessions table
    db.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            current_room TEXT,
            inventory TEXT,
            health INTEGER DEFAULT 100,
            gold INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')
    
    db.commit()
    db.close()

@app.before_request
def before_request():
    """Initialize database on first request"""
    if not app.config['DATABASE_PATH'].exists():
        init_db()

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'environment': app.config['FLASK_ENV']
    })

@app.route('/api/game/command', methods=['POST'])
def game_command():
    """Handle game commands"""
    data = request.get_json()
    command = data.get('command', '').lower().strip()
    
    # TODO: Integrate with your game engine
    # from game.engine import process_command
    # response = process_command(command, session)
    
    # Placeholder response
    response = {
        'output': f'You entered: {command}',
        'room': 'Starting Room',
        'health': 100,
        'inventory': []
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
