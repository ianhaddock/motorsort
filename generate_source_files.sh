#!/bin/bash -e
#
# File renaming and linking
# v1 20231217

while read -r line; do
    echo -e "Creating $2/$line\n"
    touch "$2/$line"
done <$1
