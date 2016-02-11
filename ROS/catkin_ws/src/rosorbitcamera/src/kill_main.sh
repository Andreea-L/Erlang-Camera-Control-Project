#!/bin/bash

x=$(date +%s%N | cut -b1-13)
rosnode kill /orbit_face_tracking_main
y=$(date +%s%N | cut -b1-13)
echo $y >> main_timing.time
echo $(($y-$x))