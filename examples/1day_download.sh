#!/bin/bash


# This script is intended to be run the same time once everyday. It will create download and sort videos by day

DATE=$(date +%F)
DOWNLOAD_DIR=$HOME/Videos/youtube/$DATE
mkdir -p $DOWNLOAD_DIR
python3 ../ysdm.py --output $DOWNLOAD_DIR --config $1 --since 86400
