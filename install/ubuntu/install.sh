#!/usr/bin/env sh

IsInstalled() {
	directory=$1
	if [ -d $directory ]; then
		return 1
	else
		return 0
	fi
}

RootDir=$1

sudo -E apt-get install proxychains w3af nmap openjdk-7-jre wapiti skipfish tor 