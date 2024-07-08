#!/bin/bash

# Reset tmux and get changes via git
tmux kill-server
cd ~/mlh-portfolio
git fetch && git reset origin/main --hard

# Install any dependencies into the virtual environment
source python3-virtualenv/bin/activate

pip install -r requirements.txt

# Launch the new tmux session and run the server
tmux new-session -d -s portfolio "source python3-virtualenv/bin/activate && flask run --host=0.0.0.0"

echo "Done"
