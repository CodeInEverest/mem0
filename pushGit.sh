#!/bin/sh
commitStr=""
if [ $# -gt 0 ]; then
    commitStr="$1"
else
    commitStr="fix"
fi

branch="master"
if [ $# -gt 1 ]; then
    branch=$2
fi
git add .
git commit -a -m "$commitStr"
git push origin $branch

echo "finish!"

