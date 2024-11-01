#!/bin/bash

echo "Grabbing latest XMLY URL..."
python getWebPageLink.py
echo "Grabbed, now start hexo building & deploying..."
hexo clean
hexo d
hexo clean

echo "Hexo building and deploying finished, now pushing source to GitHub..."
git stash && git pull
git add .
echo "Input the day of number:"
read numDay
git commit -m "Add Day${numDay} audio."
git push
echo "Done."