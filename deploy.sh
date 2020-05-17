#!/bin/bash


git fetch --all
git reset --hard origin/feature_ly

if [ -d venv ]; then
	source venv/bin/activate
	pip install -r requirements.txt
	deactivate
fi

if [ -d venv ]; then
	source venv/bin/activate
	cd main
		python compile.py
		find app -name "*.py" | xargs rm -rf
	cd ..
	cd monitor
		python compile.py
		find app -name "*.py" | xargs rm -rf
	cd ..
	deactivate
fi
