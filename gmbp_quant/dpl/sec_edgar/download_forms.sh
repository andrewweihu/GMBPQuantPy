#!/bin/bash

# PARAMETERS
OUTPUT_DIR=./sec_data/
CACHE_DIR=./sec_data/cache

python -m secutils.download_sec \
    --output_dir=$OUTPUT_DIR \
    --form_types "144" \
    --num_workers=1 \
    --start_year=2020 \
    --end_year=2020 \
    --quarters 1 2 3 4 \
    --cache_dir=$CACHE_DIR