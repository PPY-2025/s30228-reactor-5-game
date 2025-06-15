from flask import Flask, render_template, request, jsonify, send_from_directory
from database.db import save_score, get_leaderboard, create_user
from database.models import User
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create Flask app with explicit template and static folders
app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

# Configure MongoDB connection and security
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF

@app.route('/')
def index():
    logger.debug('Accessing index route')
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f'Error rendering index template: {str(e)}')
        raise

@app.route('/game')
def game():
    logger.debug('Accessing game route')
    try:
        return render_template('game.html')
    except Exception as e:
        logger.error(f'Error rendering game template: {str(e)}')
        raise

@app.route('/api/save_score', methods=['POST'])
def api_save_score():
    logger.debug('Accessing save_score route')
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
    logger.debug('Accessing leaderboard route')
    leaderboard = get_leaderboard()
    return jsonify(leaderboard)

@app.route('/api/start_game', methods=['POST'])
def start_game():
    logger.debug('Accessing start_game route')
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

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    logger.debug(f'Accessing static file: {path}')
    try:
        return send_from_directory('static', path)
    except Exception as e:
        logger.error(f'Error serving static file {path}: {str(e)}')
        raise

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    logger.info(f'Starting Flask application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False) 