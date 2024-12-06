#!/bin/bash

# Check if the file exists
if [[ -f /run/secrets/wattsy_secrets ]]; then
  source "$FILE_TO_SOURCE"

python3 src/main.py