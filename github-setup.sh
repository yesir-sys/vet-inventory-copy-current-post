#!/bin/bash

# Remove existing Git setup
rm -rf .git

# Initialize new Git repository
git init

# Set Git configurations
git config --global credential.helper store
git config --global http.postBuffer 524288000
git config --global http.maxRequestBuffer 100M
git config --global core.compression 9

# Add all files to staging
git add .

# Commit the files
git commit -m "Initial commit"

# Add the remote repository
git remote add origin https://github.com/yesir-sys/vet-inventory-copy-current-post.git

# Fetch remote repository
git fetch origin

# Try to pull first (this might fail if histories are unrelated)
git pull origin main --allow-unrelated-histories || echo "Pull failed, continuing with push"

# Force push to GitHub (use with caution - this will overwrite remote changes)
git push -u origin main --force
