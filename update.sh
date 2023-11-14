#!/bin/bash

git pull

if [ ! -d "env" ]; then
	echo "Creating venv, please wait ..."
	python3 -m venv env
fi

source ./env/bin/activate
echo "Set venv to source"
echo "Updating packages, please wait ..."

pip install --upgrade pip >/dev/null 2>&1
pip install --upgrade wheel >/dev/null 2>&1
pip install --upgrade setuptools >/dev/null 2>&1
echo "Updated python internal pip packages"

pip install --upgrade -r requirements.txt >/dev/null 2>&1
echo "Installed/Updated dependencies"