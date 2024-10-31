#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: <Daily Title> <link>"
    exit 1
fi

day=$1
link=$2

{
    echo "#EXTINF:-1, $day"
    echo "$link"
} >> ./source/xutao.m3u

{
    echo ""
    echo ""
    echo "$day"
    echo "$link"
} >> ./source/_posts/直链.md

echo "$day $link appended to xutao.m3u and 直链.md."
