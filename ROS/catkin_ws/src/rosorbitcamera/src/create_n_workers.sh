#!/bin/bash

echo Creating $1 ROS worker nodes.
j=1
for (( i=0; i<$1; i++ ))
do
	rosrun rosorbitcamera worker.py $i $j &

	if [ $j -eq 4 ]
	then
		let j=0
	fi
	let j=j+1
done  