import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200

def test_game_page(client):
    """Test that the game page loads successfully."""
    response = client.get('/game')
    assert response.status_code == 200

def test_leaderboard_endpoint(client):
    """Test that the leaderboard API endpoint returns successfully."""
    response = client.get('/api/leaderboard')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_start_game_endpoint(client):
    """Test that the start game API endpoint works correctly."""
    response = client.post('/api/start_game', 
                         json={'username': 'test_user'})
    assert response.status_code == 200
    assert response.json['success'] is True

def test_save_score_endpoint(client):
    """Test that the save score API endpoint works correctly."""
    # First start a game to set the username cookie
    client.post('/api/start_game', json={'username': 'test_user'})
    
    # Then try to save a score
    response = client.post('/api/save_score', 
                         json={'survival_time': 100})
    assert response.status_code == 200
    assert response.json['success'] is True 