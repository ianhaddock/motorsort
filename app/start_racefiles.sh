#!/bin/bash

sleep_seconds=300

mins=$(echo $sleep_seconds / 60 | bc)

while true; do
    echo "$(date): starting"
    python racefiles.py
    echo "$(date): sleeping $mins minutes"

    n=0
    while (( n < $mins )); do
        sleep 60
        echo -n "."
        ((n++))
    done
    echo ""
done
