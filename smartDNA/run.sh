#!/bin/bash
process=`pgrep -U root "$1" | wc -l`
echo $process
if [ $process -ge 1 ]; then
echo It is not safe to kill this process...
else
pkill $1
echo $1 process killed...
fi
