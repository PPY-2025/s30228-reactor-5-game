from flask import Flask, render_template, request, jsonify, redirect, url_for
from database.db import save_score, get_leaderboard, get_user, create_user
from database.models import User
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/api/save_score', methods=['POST'])
def api_save_score():
    data = request.get_json()
    username = request.cookies.get('username')
    if not username:
        return jsonify({'error': 'No username found'}), 400
    
    survival_time = data.get('survival_time')
    if not survival_time:
        return jsonify({'error': 'No survival time provided'}), 400

    save_score(username, survival_time)
    return jsonify({'success': True})

@app.route('/api/leaderboard')
def api_leaderboard():
    leaderboard = get_leaderboard()
    return jsonify(leaderboard)

@app.route('/api/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    username = data.get('username')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    # Create or update user
    user = User(username=username, survival_time=0)
    create_user(user)
    
    response = jsonify({'success': True})
    response.set_cookie('username', username)
    return response

if __name__ == '__main__':
    app.run(debug=True) 