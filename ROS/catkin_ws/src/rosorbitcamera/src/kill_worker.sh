#!/bin/bash

x=$(date +%s%N | cut -b1-13)
# rosnode kill /orbit_face_tracking_n0
kill -9 $(ps aux | grep 'orbit_face_tracking_n' | grep -v grep | awk '{print $2}')
y=$(date +%s%N | cut -b1-13)
echo $y >> worker_timing.time
echo $(($y-$x))