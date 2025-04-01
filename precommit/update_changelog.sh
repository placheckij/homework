#!/bin/sh

# Get the latest commit message
latest_commit_message=$(cat .git/COMMIT_EDITMSG)

# Get the current version from pyproject.toml
version=$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml)

# Get the current date
current_date=$(date +"%Y-%m-%d")

# Split the version into major, minor, and patch
IFS='.' read -r major minor patch <<< "$version"

# Determine the type of version bump
if echo "$latest_commit_message" | grep -q "#BREAKING"; then
  major=$((major + 1))
  minor=0
  patch=0
  update_changelog=true
elif echo "$latest_commit_message" | grep -q "#FEAT"; then
  minor=$((minor + 1))
  patch=0
  update_changelog=true
elif echo "$latest_commit_message" | grep -q "#BUG"; then
  patch=$((patch + 1))
  update_changelog=true
else
  update_changelog=false
fi

# Construct the new version
new_version="$major.$minor.$patch"

# Update the version in pyproject.toml
sed -i '' "s/^version = \".*\"/version = \"$new_version\"/" pyproject.toml

# If the commit message contains one of the tags, update the changelog
if [ "$update_changelog" = true ]; then
  # Get the current date
  current_date=$(date +"%Y-%m-%d")

  # Check if current version section already exists in CHANGELOG.md
  if ! grep -q "^## $new_version" CHANGELOG.md; then
    # Add a new section with the current version
    echo "\n## $new_version ($current_date)" >> CHANGELOG.md
  fi

  # Remove tags from the commit message
  clean_commit_message=$(echo "$latest_commit_message" | sed 's/#BREAKING//g' | sed 's/#FEAT//g' | sed 's/#BUG//g')

  # Append the cleaned commit message to CHANGELOG.md
  echo "- $clean_commit_message" >> CHANGELOG.md

  # Add CHANGELOG.md and pyproject.toml to the staging area
  git add CHANGELOG.md pyproject.toml
else
  # Add only pyproject.toml to the staging area
  git add pyproject.toml
fi

# Commit the changes
git commit --no-verify --allow-empty-message -m ""

# breaking test
