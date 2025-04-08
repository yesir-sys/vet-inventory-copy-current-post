#!/bin/bash

echo "Starting GitHub upload process..."

# Configure Git if not already done
if [ -z "$(git config --global credential.helper)" ]; then
    git config --global credential.helper store
    git config --global http.postBuffer 524288000
    git config --global http.maxRequestBuffer 100M
    git config --global core.compression 9
fi

# Stage and commit files in chunks
echo "Staging Python files..."
git add "*.py"
git commit -m "Update Python files" || true

echo "Staging HTML files..."
git add "*.html"
git commit -m "Update HTML templates" || true

echo "Staging static files..."
git add "*.css" "*.js"
git commit -m "Update static files" || true

echo "Staging config files..."
git add "*.json" "*.yaml" "*.yml"
git commit -m "Update configuration files" || true

echo "Staging remaining files..."
git add .
git commit -m "Update remaining files" || true

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main --rebase || echo "Pull failed, continuing..."

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo "Upload completed!"
