#!/bin/bash


export UWSGI_INI_FILENAME="uwsgi/uwsgi.ini"
export UWSGI_PID_FILENAME="uwsgi/uwsgi.pid"


if [ $1 == "start" ]; then
	source ../venv/bin/activate
	uwsgi $UWSGI_INI_FILENAME > /dev/null 2>&1 &

	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo -n .

	echo
	ps -ef | grep "PLASTIC"
fi


if [ $1 == "stop" ]; then
	source ../venv/bin/activate
	uwsgi --stop $UWSGI_PID_FILENAME

	sleep 1; echo -n .
	sleep 1; echo -n .
	sleep 1; echo -n .

	echo
	ps -ef | grep "PLASTIC"
fi
