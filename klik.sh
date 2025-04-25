#!/bin/bash

# Run setupo.sh using source
if [ -f setupo.sh ]; then
    echo "Running setupo.sh..."
    source setupo.sh
else
    echo "Error: setupo.sh not found."
    exit 1
fi

# Run start.sh after setupo.sh completes
if [ -f start.sh ]; then
    echo "Running start.sh..."
    bash start.sh
else
    echo "Error: start.sh not found."
    exit 1
fi
