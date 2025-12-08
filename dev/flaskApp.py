# app.py (Flask backend)

from flask import Flask, render_template, request, jsonify, session
from game.engine import GameEngine
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    session['game_state'] = GameEngine.new_game()
    return jsonify({
        'output': GameEngine.get_intro(),
        'prompt': '> '
    })

@app.route('/command', methods=['POST'])
def process_command():
    command = request.json.get('command', '').strip().lower()
    game_state = session.get('game_state', {})
    
    # Process command through game engine
    result = GameEngine.process_command(command, game_state)
    
    # Update session
    session['game_state'] = result['state']
    
    return jsonify({
        'output': result['output'],
        'prompt': '> '
    })

@app.route('/save', methods=['POST'])
def save_game():
    # Implement save functionality
    pass

@app.route('/load', methods=['POST'])
def load_game():
    # Implement load functionality
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)