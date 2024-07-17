#!/bin/bash

# Get changes via git
cd ~/mlh-portfolio
git fetch && git reset origin/main --hard

# Install any dependencies into the virtual environment
source python3-virtualenv/bin/activate

pip install -r requirements.txt
deactivate

# Restart the service
systemctl restart myportfolio

echo "Done"
