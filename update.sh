#!/bin/bash

git pull

if [ ! -d "env" ]; then
	echo "Creating venv, please wait ..."
	python3 -m venv env
else
	echo "Venv already exists"
fi

source ./env/bin/activate
echo "Set venv to source"
echo "Updating packages, please wait ..."

pip install --upgrade pip wheel setuptools >/dev/null 2>&1
echo "Updated python internal pip packages"

pip install --upgrade -r requirements.txt >/dev/null 2>&1
echo "Installed/Updated dependencies"
