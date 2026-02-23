from flask import Flask, render_template, request, session, jsonify
from config import config
import os
from game.engine import GameEngine

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app

app = create_app(os.environ.get('FLASK_ENV', 'production'))

@app.route('/')
def index():
    """Main game interface"""
    return render_template('index.html')

@app.route('/api/game/new', methods=['POST'])
def new_game():
    """Start a new game"""
    game_state = GameEngine.new_game()
    session['game_state'] = game_state
    
    return jsonify({
        'output': 'Welcome to the DailyDungeon!\n\nYou stand at the threshold of the forgotten dungeon, a labyrinth of peril and mystery. Whispers speak of untold treasures guarded by ancient foes.\n\nType "look" to examine your surroundings or "help" for commands.',
        'player': game_state['player'],
        'room': game_state['current_room'],
        'round': f"{game_state['round_number']}/{game_state['total_rounds']}"
    })

@app.route('/api/game/command', methods=['POST'])
def game_command():
    """Process game command"""
    data = request.get_json()
    command = data.get('command', '').strip().lower()
    
    # Get game state from session
    game_state = session.get('game_state')
    if not game_state:
        return jsonify({
            'output': '⚠️ No active game. Type "new" to start a new game.',
            'error': True
        })

# --- NEW MAP INTERCEPTION ---
    if command == "map":
        return jsonify({
            'output': '🗺️ You unfurl the ancient map...',
            'command': 'show_map', # Flag for index.html
            'player': game_state['player'],
            'room': game_state['current_room'],
            'round': f"{game_state['round_number']}/{game_state['total_rounds']}"
        })
    
    # Process command
    result = GameEngine.process_command(command, game_state)
    
    # Update session
    session['game_state'] = result['state']
    session.modified = True
    
    # Prepare response
    response = {
        'output': result['output'],
        'player': result['state']['player'],
        'room': result['state']['current_room'],
        'round': f"{result['state']['round_number']}/{result['state']['total_rounds']}",
        'game_over': result['state'].get('game_over', False),
        'victory': result['state'].get('victory', False)
    }
    
    return jsonify(response)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'game': 'OnlyDungeons'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
