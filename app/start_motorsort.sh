#!/bin/bash -e

# create custom track and images directories
#
mkdir -p /custom/{tracks,images,flags}

# fill custom image and track directories if empty
#
if [ -z "$(ls -A /custom/tracks)" ]; then
    cp /config/tracks/* /custom/tracks/
fi

if [ -z "$(ls -A /custom/images)" ]; then
    cp /config/images/* /custom/images/
fi

if [ -z "$(ls -A /custom/flags)" ]; then
    cp /config/flags/* /custom/flags/
fi

if [ ! -z /custom/series_prefix.json ]; then
    cp /config/series_prefix.json /custom/series_prefix.json
fi

if [ ! -z /custom/session_map.json ]; then
    cp /config/session_map.json /custom/session_map.json
fi

if [ ! -z /custom/weekend_order.json ]; then
    cp /config/weekend_order.json /custom/weekend_order.json
fi

if [ ! -z /custom/fonts.json ]; then
    cp /config/fonts.json /custom/fonts.json
fi

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
# every $sleep_seconds forever unless an error is returned
#
while true; do
    echo "$(date): Starting"
    python motorsort.py

    if [ $? != 0 ]; then
       exit 1
    elif [ $sleep_seconds == 0 ]; then
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
