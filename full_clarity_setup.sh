#!/bin/bash

# A comprehensive script to automate the entire Clarity project setup process.

# --- Configuration ---
GITHUB_USERNAME="YourGitHubUsername"

# The GitHub PAT is now stored securely as a Replit Secret.
if [ -z "$GITHUB_PAT" ]; then
  echo "❌ Error: GITHUB_PAT environment variable not found."
  echo "Please add your GitHub Personal Access Token as a secret in the Replit Secrets tab (lock icon)."
  exit 1
fi

# --- Argument Validation ---
if [ "$#" -ne 3 ]; then
  echo "❌ Error: This script requires three arguments."
  echo "Usage: ./full_clarity_setup.sh <project_name> <branch_name> <contract_name>"
  exit 1
fi

PROJECT_NAME=$1
BRANCH_NAME=$2
CONTRACT_NAME=$3

echo "🚀 Starting automated Clarity project setup..."

# 1. Create a new Clarinet project and handle the 'Y' prompt.
echo "1. Creating project using 'clarinet new $PROJECT_NAME'..."
yes Y | clarinet new "$PROJECT_NAME"

if [ ! -d "$PROJECT_NAME" ]; then
  echo "❌ Error: Failed to create project directory '$PROJECT_NAME'."
  exit 1
fi

# 2. Change into the new project directory.
cd "$PROJECT_NAME"
echo "2. Changed directory to '$PROJECT_NAME'."

# 3. Create a README.md file.
echo "3. Creating README.md..."
echo "# $PROJECT_NAME" > README.md

# 4. Initialize Git.
echo "4. Initializing Git repository..."
git init

# --- Add New Steps: Copy Scripts and Configure Gitignore ---
echo "5. Copying utility scripts into the project folder..."
cp ../ToolShed/ClarCommit.sh .
cp ../ToolShed/FinCommit.sh .

echo "6. Adding scripts to .gitignore to prevent tracking..."
echo "" >> .gitignore
echo "# Ignore utility scripts" >> .gitignore
echo "ClarCommit.sh" >> .gitignore
echo "FinCommit.sh" >> .gitignore

# The rest of the script continues as before...

# 7. Stage all new files.
echo "7. Staging initial files..."
git add .

# 8. Commit the changes.
echo "8. Committing initial setup..."
git commit -m "Initial file system setup with Clarinet, README.md, and utility scripts"

# 9. Set the remote repository URL.
REMOTE_URL="https://${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/${PROJECT_NAME}.git"
echo "9. Setting remote repository to '$REMOTE_URL'..."
git remote add origin "$REMOTE_URL"

# 10. Push changes to the 'main' branch.
echo "10. Pushing initial commit to 'main'..."
git push -u origin main

# 11. Create a new branch.
echo "11. Creating and checking out a new branch: '$BRANCH_NAME'..."
git checkout -b "$BRANCH_NAME"

# 12. Create the new contract.
echo "12. Creating new contract: '$CONTRACT_NAME'..."
clarinet contract new "$CONTRACT_NAME"

# 13. Open the contract in the Replit editor.
echo "13. Opening contract in the editor..."
code "contracts/$CONTRACT_NAME.clar"

echo "✅ All steps completed! Project '$PROJECT_NAME' is ready."
echo

echo "Great Job 🎉! Your Clarity project setup is complete. You can now start developing your smart contract."