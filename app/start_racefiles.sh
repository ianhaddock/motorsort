#!/bin/bash

# if env var set use that, otherwise use default
#
if [ ! $SLEEP_SECONDS ]; then
    sleep_seconds=300
else
    sleep_seconds=$SLEEP_SECONDS
fi

# take seconds and divide by ten for progress indicator
# if value is zero seconds, use 1 second instead
#
tic_rate=$(echo $sleep_seconds / 10 | bc)
if [ $tic_rate -lt 1 ]; then
    tic_rate=1
fi

# if env var is zero, run then quit. Otherwise loop 
# every $sleep_seconds forever
#
while true; do
    echo "$(date): Starting"
    python racefiles.py

    if [ $sleep_seconds == 0 ]; then
        echo "$(date): Exiting."
        exit 0
    fi

    echo "$(date): Sleeping $sleep_seconds seconds"

    n=0
    while (( n < $sleep_seconds )); do
        sleep $tic_rate
        echo -n "."
        ((n=$n+$tic_rate))
    done
    echo ""
done
