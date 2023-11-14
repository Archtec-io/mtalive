#!/bin/bash

if [ ! -d "env" ]; then
	echo "No venv created, please run 'update.sh'"
	exit 1
fi

source ./env/bin/activate
echo "Set venv to source"

while getopts e:a:p: flag
do
	case "${flag}" in
		e) export mtalive_minetest_path=${OPTARG};;
		a) export mtalive_listening_address=${OPTARG};;
		p) export mtalive_listening_port=${OPTARG};;
		*) echo "usage: $0 [-v] [-r]" >&2
			exit 1 ;;
	esac
done

python mtalive.py