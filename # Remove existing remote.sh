# Remove existing remote
git remote remove origin

# Add the correct remote
git remote add origin https://github.com/yesir-sys/vet-inventory-copy-current-post.git

# Configure Git to store credentials
git config --global credential.helper store

# Set up your GitHub credentials (you'll need to do this once)
# Generate a token at: GitHub.com → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
# When prompted:
# Username: your GitHub username
# Password: use your personal access token (not your GitHub password)

# Push to main branch
git push -u origin main
