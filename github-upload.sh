#!/bin/bash

echo "Starting GitHub upload process..."

# Remove existing Git setup if it exists
if [ -d .git ]; then
    echo "Removing existing Git setup..."
    rm -rf .git
fi

# Initialize new Git repository
echo "Initializing new Git repository..."
git init

# Configure Git settings
echo "Configuring Git settings..."
git config --global credential.helper store
git config --global http.postBuffer 524288000
git config --global http.maxRequestBuffer 100M
git config --global core.compression 9
git config --global core.bigFileThreshold 50m
git config --global core.autocrlf input

# Stage files in chunks to avoid memory issues
echo "Staging files..."
git add "*.py"
git commit -m "Add Python files"

git add "*.html"
git commit -m "Add HTML templates"

git add "*.css" "*.js"
git commit -m "Add static files"

git add "*.json" "*.yaml" "*.yml"
git commit -m "Add configuration files"

git add .
git commit -m "Add remaining files"

# Create and switch to main branch
echo "Setting up main branch..."
git branch -M main

# Add remote repository
echo "Adding remote repository..."
git remote add origin https://github.com/yesir-sys/vet-inventory-copy-current-post.git

# Attempt to pull first (if repository exists)
echo "Syncing with remote repository..."
git pull origin main --allow-unrelated-histories || echo "No existing remote history, continuing..."

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main --force

echo "GitHub upload process completed!"
