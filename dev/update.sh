#!/bin/bash
cd /home/pi/adventure-game
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart adventure-game
echo "Game updated and restarted!"