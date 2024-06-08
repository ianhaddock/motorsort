#!/bin/bash

if [ ! $SLEEP_SECONDS ]; then
    sleep_seconds=300
else
    sleep_seconds=$SLEEP_SECONDS
fi

tic_rate=$(echo $sleep_seconds / 10 | bc)

if [ $tic_rate -lt 1 ]; then
    tic_rate=1
fi

while true; do
    echo "$(date): starting"
#    python racefiles.py
    echo "$(date): sleeping $sleep_seconds seconds"

    n=0
    while (( n < $sleep_seconds )); do
        sleep $tic_rate
        echo -n "."
        ((n=$n+$tic_rate))
    done
    echo ""
done
