#!/bin/bash


PID_FILE="server.pid"
LOG_FILE="server.log"


if [ $1 == "start" ]; then
	source ../venv/bin/activate
	python manager.py > $LOG_FILE 2>&1 &
	echo $! > $PID_FILE

	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo
fi


if [ $1 == "stop" ]; then
	if [ -f $PID_FILE ]; then
		read line < $PID_FILE
		pkill -P $line
		rm $PID_FILE
	fi

	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo
fi
