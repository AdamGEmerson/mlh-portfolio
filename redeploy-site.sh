#!/bin/bash

# Get changes via git
cd ~/mlh-portfolio
git fetch && git reset origin/main --hard

# Docker launch
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d
echo "Done"
