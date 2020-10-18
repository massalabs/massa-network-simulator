#!/bin/sh

# setup network simulation
UL_KBITPS="$1"
UL_MS="$2"
shift 2

# upload
tc qdisc add dev eth0 root handle 1:0 tbf rate "${UL_KBITPS}kbit" buffer "$((UL_KBITPS>1600 ? UL_KBITPS : 1600))" limit 10000
tc qdisc add dev eth0 parent 1:0 handle 10: netem delay "${UL_MS}ms"  # loss 0.03%

# run program
"$@"

