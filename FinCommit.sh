#!/bin/bash

# A script to commit and push changes for a specific file.

# A more suitable commit message
COMMIT_MESSAGE="README.md file updated"

echo "➡️ Staging changes..."
git add .

echo "📝 Committing changes with message: '$COMMIT_MESSAGE'..."
git commit -m "$COMMIT_MESSAGE"

echo "☁️ Pushing changes to the remote branch..."
git push