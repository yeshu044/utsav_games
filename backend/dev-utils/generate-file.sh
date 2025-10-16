cd /Users/yeshwanth.bd/personal/utsav-games/backend

# Create main app directory structure
mkdir -p app/{api,models,schemas,services,utils,websockets}
mkdir -p app/core
mkdir -p alembic/versions
mkdir -p tests

# Create __init__.py files for Python packages
touch app/__init__.py
touch app/api/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch app/websockets/__init__.py
touch app/core/__init__.py
touch tests/__init__.py

# Create main application files
touch app/main.py
touch app/database.py

# Create core configuration files
touch app/core/config.py
touch app/core/security.py

# Create API route files
touch app/api/auth.py
touch app/api/events.py
touch app/api/games.py
touch app/api/levels.py
touch app/api/media.py
touch app/api/progress.py
touch app/api/leaderboard.py

# Create model files
touch app/models/user.py
touch app/models/event.py
touch app/models/game.py
touch app/models/level.py
touch app/models/media.py
touch app/models/progress.py
touch app/models/otp.py

# Create schema files
touch app/schemas/user.py
touch app/schemas/auth.py
touch app/schemas/event.py
touch app/schemas/game.py
touch app/schemas/level.py
touch app/schemas/media.py
touch app/schemas/progress.py
touch app/schemas/leaderboard.py

# Create service files
touch app/services/auth_service.py
touch app/services/otp_service.py
touch app/services/game_service.py
touch app/services/leaderboard_service.py
touch app/services/media_service.py

# Create utility files
touch app/utils/validators.py
touch app/utils/helpers.py
touch app/utils/dependencies.py

# Create WebSocket file
touch app/websockets/leaderboard_ws.py

# Create test files
touch tests/test_auth.py
touch tests/test_games.py
touch tests/test_events.py
touch tests/test_leaderboard.py

# Create root level files
touch requirements.txt
touch .env
touch .env.example
touch .gitignore
touch README.md
touch alembic.ini

# Create a simple run script
touch run.sh
chmod +x run.sh