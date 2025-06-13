function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('visible');
    });
    
    // Show selected page
    document.getElementById(pageId).classList.add('visible');
}

function checkUsername() {
    const username = document.getElementById('username').value.trim();
    const startButton = document.getElementById('startButton');
    startButton.disabled = username.length < 3;
}

function startGame() {
    const username = document.getElementById('username').value.trim();
    
    fetch('/api/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/game';
        } else {
            alert('Error starting game: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error starting game. Please try again.');
    });
}

// Load leaderboard when the page loads
document.addEventListener('DOMContentLoaded', function() {
    loadLeaderboard();
});

function loadLeaderboard() {
    fetch('/api/leaderboard')
        .then(response => response.json())
        .then(data => {
            const leaderboardList = document.getElementById('leaderboard-list');
            leaderboardList.innerHTML = '';

            if (data.length === 0) {
                leaderboardList.innerHTML = `
                    <div class="leaderboard-info">
                        No technicians have survived long enough to be recognized.
                        <b>Remember: Excellence is mandatory. Failure is not tolerated.<br>
                        We’re always watching.</b>
                    </div>
                `;
                return; // don't process further
            }
            
            data.forEach((entry, index) => {
                const entryDiv = document.createElement('div');
                entryDiv.className = 'leaderboard-entry';
                
                const minutes = Math.floor(entry.survival_time / 60);
                const seconds = entry.survival_time % 60;
                const timeString = `${minutes}:${seconds.toString().padStart(2, '0')}`;
                
                entryDiv.innerHTML = `
                    <span class="rank">#${index + 1}</span>
                    <span class="username">${entry.username}</span>
                    <span class="time">${timeString}</span>
                `;
                
                leaderboardList.appendChild(entryDiv);
            });
        })
        .catch(error => {
            console.error('Error loading leaderboard:', error);
        });
}