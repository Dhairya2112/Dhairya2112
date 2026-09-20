#!/usr/bin/env bash
# Publish dist/ to the `assets` branch as a single orphan commit (no history bloat).
# In CI: needs GH_PUSH_TOKEN and GITHUB_REPOSITORY. Locally, set PUBLISH_REMOTE to test.
set -euo pipefail
REMOTE="${PUBLISH_REMOTE:-https://x-access-token:${GH_PUSH_TOKEN:?}@github.com/${GITHUB_REPOSITORY:?}.git}"
cd "$(dirname "$0")/../dist"
rm -rf .git
git init -q -b assets
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
git commit -q -m "render $(date -u +%Y-%m-%dT%H:%MZ)"
git push -q --force "$REMOTE" assets
echo "published $(ls | tr '\n' ' ')to branch assets"
