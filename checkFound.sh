#!/bin/bash
cd "$(dirname "$0")"
if [ -f FOUND.txt ]; then
	cat FOUND.txt | /usr/local/bin/pb push
	echo $(date) >> found.log;
	cat FOUND.txt | found.log
fi
