#!/bin/bash

echo "$(git status)"
branch_fetch="fetch_data"
git fetch && git pull
git add -A
git commit -m "Save changes before switching branch"
git push
if [[ `git branch --list $branch_fetch` ]]; then
    echo "Branch name $branch_fetch exists, checkout to it."
    current_branch="$(git rev-parse --abbrev-ref HEAD)"
    if [[ "$current_branch" != "fetch_data" ]]; then
        git checkout $branch_fetch
        git fetch && git pull
    fi
else
    echo "Else case, script branch.sh"
    chmod +x ./scripts/branch.sh
    ./scripts/branch.sh
fi
