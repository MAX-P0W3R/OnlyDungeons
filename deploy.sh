#!/bin/bash
set -e

echo "🎲 Starting OnlyDungeons deployment..."

cd /opt/dailydungeon

# Pull latest changes
echo "📥 Pulling latest code..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database initialization if needed
echo "🗄️ Checking database..."
python3 -c "from app import init_db; init_db()" 2>/dev/null || echo "Database init will run on first request"

# Restart the service
echo "🔄 Restarting service..."
sudo systemctl restart dailydungeon

echo "✅ Deployment complete!"
echo "🌐 Site should be live at https://coldharbor.app"
