#!/bin/sh

# setup network simulation
DL_KBPS="$1"
DL_MS="$2"
UL_KBPS="$2"
UL_MS="$3"
shift 4
echo "$DL_KBPS $DL_MS $UL_KBPS $UL_MS"

# run program
"$@"

