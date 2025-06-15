# ☢️ Reactor 5  ![CI Pipeline](https://github.com/PPY-2025/s30228-reactor-5-game/actions/workflows/ci.yml/badge.svg)
Reactor 5 is a terminal-style survival game where players fight against the ticking clock of a nuclear meltdown. Built with Python and Flask for the backend and HTML + CSS + JS for the interface, it stores user data and survival scores in MongoDB.

## Environment Variables
This project uses environment variables, so use [.env.example file](https://github.com/PPY-2025/s30228-reactor-5-game/blob/main/.env.example) as guide to create your `.env` file in the root of the project. These will be automatically picked up by Docker Compose.

## Local Setup with Docker
1. Clone the repo
```
git clone https://github.com/PPY-2025/s30228-reactor-5-game.git
cd s30228-reactor-5-game
```
 2. Run with Docker Compose
```
docker-compose up --build
```
3. Access the app<br>
Open your browser or test on: http://localhost:5001<br><br>
4. Stop container
```
docker-compose down
```
## ⚙️ System Requirements
- Docker Desktop (For Docker and Docker Compose)
- Mac, Linux, or Windows
- Internet connection
