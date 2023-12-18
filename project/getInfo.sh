#!/bin/bash

# Define the output file
OUTPUT_FILE="cluster_usage_data.txt"

# Calculate 'starttime' and 'endtime'
# For example, set 'starttime' to yesterday and 'endtime' to today
STARTTIME=$(date --date="yesterday" +%Y-%m-%d)
ENDTIME=$(date +%Y-%m-%d)

# Collect data using sacct
sacct -P -o JobID,User,Account,Partition,State,AllocCPUS,Elapsed,Start,End,NCPUS,NNodes,TotalCPU,UserCPU,SystemCPU,CPUTime --allusers --duplicates --starttime $STARTTIME --endtime $ENDTIME > $OUTPUT_FILE


