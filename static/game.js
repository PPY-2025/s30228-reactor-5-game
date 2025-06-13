// Game state
let reactor = {
    heat: 0,
    pressure: 0,
    coolant: 100,
    timeAlive: 0,
    coolDownCooldown: 0,
    pressureReleaseCooldown: 0,
    activeMalfunctions: [],
    malfunction: false,
    valveJammed: false,
    sensorFault: false,
    controlsLocked: false,
    redButton: false
};

// Game settings
const TICK_RATE = 3000; // 3 seconds per tick
let gameInterval;
let isGameOver = false;

// UI Elements
const coolantBar = document.getElementById('coolant-bar');
const pressureBar = document.getElementById('pressure-bar');
const heatBar = document.getElementById('heat-bar');
const malfunctionLog = document.querySelector('#malfunction-log');

// Initialize game
function initGame() {
    reactor = {
        heat: 0,
        pressure: 0,
        coolant: 100,
        timeAlive: 0,
        coolDownCooldown: 0,
        pressureReleaseCooldown: 0,
        activeMalfunctions: [],
        malfunction: false,
        valveJammed: false,
        sensorFault: false,
        controlsLocked: false,
        redButton: false
    };
    isGameOver = false;
    updateUI();
    gameInterval = setInterval(gameTick, TICK_RATE);
}

// Game tick function
function gameTick() {
    if (isGameOver) return;

    reactor.timeAlive++;
    reactor.heat += 5;
    reactor.pressure += 7;

    if (reactor.coolDownCooldown > 0) reactor.coolDownCooldown--;
    if (reactor.pressureReleaseCooldown > 0) reactor.pressureReleaseCooldown--;

    // Process active malfunctions
    for (let i = reactor.activeMalfunctions.length - 1; i >= 0; i--) {
        const mal = reactor.activeMalfunctions[i];
        applyMalfunctionEffect(mal);
        mal.duration--;
        if (mal.duration <= 0) {
            fixMalfunction(mal.name);
            reactor.activeMalfunctions.splice(i, 1);
        }
    }

    // Random malfunction chance
    if (!reactor.activeMalfunctions.length && Math.random() < 0.2) {
        triggerRandomMalfunction();
    }

    updateUI();
    checkGameOver();
}

// Malfunction handling
function triggerRandomMalfunction() {
    const malfunctions = [
        { name: "Coolant Leak", duration: 4, effect: "coolantLeak" },
        { name: "Valve Jam", duration: 5, effect: "valveJam" },
        { name: "Power Surge", duration: 3, effect: "powerSurge" },
        { name: "Sensor Malfunction", duration: 4, effect: "sensorMalfunction" },
        { name: "Control Lockout", duration: 4, effect: "controlLockout" }
    ];

    const mal = malfunctions[Math.floor(Math.random() * malfunctions.length)];
    reactor.activeMalfunctions.push(mal);
    reactor.malfunction = true;
    addLogEntry(`WARNING: ${mal.name} detected!`, 'warning');
}

function applyMalfunctionEffect(mal) {
    switch (mal.effect) {
        case "coolantLeak":
            reactor.coolant = Math.max(0, reactor.coolant - 5);
            break;
        case "valveJam":
            reactor.valveJammed = true;
            break;
        case "powerSurge":
            reactor.heat += 10;
            break;
        case "sensorMalfunction":
            reactor.sensorFault = true;
            break;
        case "controlLockout":
            reactor.controlsLocked = true;
            break;
    }
}

// Action handlers
function handleAction(action) {
    if (isGameOver) return;

    switch (action) {
        case 'coolant':
            if (reactor.coolant > 0 && reactor.coolDownCooldown === 0 && !reactor.controlsLocked) {
                reactor.heat = Math.max(0, reactor.heat - 10);
                reactor.coolant -= 10;
                reactor.coolDownCooldown = 3;
                addLogEntry("Cooling system activated", 'info');
            }
            break;
        case 'pressure':
            if (!reactor.valveJammed && reactor.pressureReleaseCooldown === 0 && !reactor.controlsLocked) {
                reactor.pressure = Math.max(0, reactor.pressure - 15);
                reactor.pressureReleaseCooldown = 3;
                addLogEntry("Pressure release valve opened", 'info');
            }
            break;
        case 'fix-leak':
            if (!reactor.controlsLocked) {
                fixMalfunction("Coolant Leak");
            }
            break;
        case 'unjam-valve':
            if (!reactor.controlsLocked) {
                fixMalfunction("Valve Jam");
            }
            break;
        case 'fix-surge':
            if (!reactor.controlsLocked) {
                fixMalfunction("Power Surge");
            }
            break;
        case 'fix-sensor':
            if (!reactor.controlsLocked) {
                fixMalfunction("Sensor Malfunction");
            }
            break;
        case 'panic':
            reactor.redButton = true;
            checkGameOver();
            break;
    }
    updateUI();
}

function fixMalfunction(name) {
    const index = reactor.activeMalfunctions.findIndex(m => m.name === name);
    if (index === -1) return;

    reactor.activeMalfunctions.splice(index, 1);
    reactor.malfunction = false;

    switch (name) {
        case "Valve Jam":
            reactor.valveJammed = false;
            reactor.pressure = Math.max(0, reactor.pressure - 5);
            break;
        case "Power Surge":
            reactor.heat = Math.max(0, reactor.heat - 10);
            break;
        case "Sensor Malfunction":
            reactor.sensorFault = false;
            break;
        case "Control Lockout":
            reactor.controlsLocked = false;
            break;
    }

    addLogEntry(`${name} fixed successfully`, 'info');
}

// UI updates
function updateUI() {
    const bars = document.querySelectorAll('.status-indicator');

    if (reactor.sensorFault) {
        bars.forEach(bar => {
            bar.style.display = 'none';
        });
    } else {
        bars.forEach(bar => {
            bar.style.display = 'flex';
        });
    }

    // Update status bars
    coolantBar.style.width = `${reactor.coolant}%`;
    pressureBar.style.width = `${(reactor.pressure / 120) * 100}%`;
    heatBar.style.width = `${reactor.heat}%`;

    coolantBar.style.backgroundColor = '#00ff00';

    // Update status bar colors based on danger levels
    updateStatusBarColor(pressureBar, reactor.pressure, 100);
    updateStatusBarColor(heatBar, reactor.heat, 80);

    updateButtonStates();
}

function updateStatusBarColor(bar, value, threshold) {
    if (value >= threshold) {
        bar.style.backgroundColor = '#ff0000';
    } else if (value >= threshold * 0.7) {
        bar.style.backgroundColor = '#ffff00';
    } else {
        bar.style.backgroundColor = '#00ff00';
    }
}

function updateButtonStates() {
    const buttons = document.querySelectorAll('.control-button');

    buttons.forEach(button => {
        if (!button.classList.contains('always-active')) {
            if (reactor.controlsLocked ||
                (button.classList.contains('coolant') && reactor.coolDownCooldown) ||
                (button.classList.contains('pressure') && (reactor.pressureReleaseCooldown || reactor.valveJammed))) {
                button.disabled = true;
                button.style.opacity = '0.5';
                button.style.pointerEvents = 'none';
            } else {
                button.disabled = false;
                button.style.opacity = '1';
                button.style.pointerEvents = 'auto';
            }
        }
    });
}

function addLogEntry(message, type = 'info') {
    const entry = document.createElement('div');
    entry.className = `malfunction-entry ${type}`;
    entry.textContent = message;
    malfunctionLog.appendChild(entry);
    malfunctionLog.scrollTop = malfunctionLog.scrollHeight;
}

// Game over handling
function checkGameOver() {
    let gameOverMessage = null;

    if (reactor.coolant <= 0) {
        gameOverMessage = "You ran out of coolant! Sorry, it will hurt.";
    } else if (reactor.heat >= 100) {
        gameOverMessage = "Reactor meltdown! Heat exceeded safe limits.";
    } else if (reactor.pressure >= 120) {
        gameOverMessage = "Reactor exploded! Pressure too high.";
    } else if (reactor.redButton) {
        gameOverMessage = "Self-destructing protocol activated!";
    }

    if (gameOverMessage) {
        isGameOver = true;
        clearInterval(gameInterval);
        addLogEntry("GAME OVER: " + gameOverMessage, 'danger');
        
        // Save score to server
        fetch('/api/save_score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                survival_time: reactor.timeAlive * 3
            })
        });

        // Show game over overlay
        const overlay = document.getElementById('game-over-overlay');
        const messageElement = document.getElementById('game-over-message');
        messageElement.textContent = gameOverMessage;
        overlay.classList.remove('hidden');
    }
}

function restartGame() {
    const overlay = document.getElementById('game-over-overlay');
    overlay.classList.add('hidden');
    initGame();
}

function quitToMenu() {
    window.location.href = '/';
}

// Initialize game when page loads
window.onload = initGame; 