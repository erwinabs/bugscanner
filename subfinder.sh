#!/bin/bash

# Ambil argumen pertama (domain)
DOMAIN="$1"

# Tentukan path subfinder
SUBFINDER_EXEC="$HOME/go/bin/subfinder"

# Tentukan path output
OUTPUT_PATH="/sdcard/${DOMAIN}.txt"

# Cek apakah domain diberikan
if [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <DOMAIN>"
    exit 1
fi

# Jalankan subfinder
"$SUBFINDER_EXEC" -d "$DOMAIN" -o "$OUTPUT_PATH"
