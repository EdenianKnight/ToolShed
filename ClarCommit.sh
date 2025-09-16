#!/bin/bash

# A script to check clarity code and initiate a git commit.

echo "🚀 Running Clarinet checks..."
clarinet check

echo "✅ Clarinet checks complete."
echo "➡️ Staging all changes for commit..."
git add .

echo "📝 Opening editor to write commit message..."
git commit