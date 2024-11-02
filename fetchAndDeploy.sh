#!/bin/bash

force_push=$1
if [ $force_push ]; then
    echo "[Warning] This time pushing will use --force parameter."
fi

echo "Please check out the playlist already exist:"
cat source/xutao.m3u
echo ""
echo "Continue?(Y/n)"
read -n 1 -s key
if [[ $key == 'n' ]]; then
    echo -e "Abort."
    exit 0
fi


echo "Grabbing latest XMLY playlist URL..."
python getWebPageLink.py
status=$?
if [ $status -eq 1 ]; then
    exit $deploy_status
fi
echo "Grabbed, now start hexo building & deploying..."
hexo clean
hexo d
status=$?
if [ $status -ne 0 ]; then
    echo "Hexo deploy failed."
    exit 0
fi
hexo clean

echo "Hexo building and deploying finished, now pushing source to GitHub..."
git add .
echo "Input the day of number:"
read numDay
echo "git commit -m \"Add Day${numDay} audio.\""
git commit -m "Add Day${numDay} audio."
if [ $force_push ]; then
    echo "git push --force"
    git push --force
else
    echo "git push"
    git push
fi
echo "Done."