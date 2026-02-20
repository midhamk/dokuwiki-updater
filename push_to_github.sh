#!/bin/bash

# GitHub Push Script for DokuWiki Updater
# ========================================
#
# INSTRUCTIONS:
# 1. Create a new repository on GitHub:
#    - Go to https://github.com/new
#    - Name it (e.g., "dokuwiki-updater")
#    - Don't initialize with README, .gitignore, or license
#    - Click "Create repository"
#
# 2. Copy your repository URL from GitHub
#    It will look like: https://github.com/YOUR_USERNAME/YOUR_REPO.git
#
# 3. Edit this script and replace YOUR_USERNAME and YOUR_REPO below
#
# 4. Make this script executable:
#    chmod +x push_to_github.sh
#
# 5. Run the script:
#    ./push_to_github.sh
git init && git add first.py push_to_github.sh README.md .gitignore && git commit -m "Initial commit: DokuWiki page updater script"
# ========================================
# EDIT THESE LINES WITH YOUR GITHUB INFO:
# ========================================
GITHUB_USERNAME="midhamk"
GITHUB_REPO="dokuwiki-updater"

# ========================================
# No need to edit below this line
# ========================================

REPO_URL="https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git"

echo "Pushing to: $REPO_URL"
echo ""

# Add remote origin
git remote add origin "$REPO_URL"

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main

echo ""
echo "✓ Done! Your code is now on GitHub at:"
echo "  https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}"
