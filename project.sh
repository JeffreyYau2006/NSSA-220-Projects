#!/bin/bash
PROC_NAME="$1"
INTERVAL=5
OUTFILE="${PROC_NAME}_metrics.csv"

PS_OUTPUT= ps aux | egrep "$PROC_NAME"
OUTP="hi"
echo $PS_OUTPUT > text.txt
echo $OUTP > text.txt

#while true; do
	# Get metrics for all matching processes (excluding the grep itself)
#	PS_OUTPUT= ps aux | egrep "$PROC_NAME"
#	echo $PS_OUTPUT

#done




