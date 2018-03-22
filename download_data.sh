#!/bin/bash
base_url="https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/2016/"
prefix="wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories"
mkdir incoming
cd incoming

 #`$prefix $base_url`
for f in *.zip
do
	unzip $f
done

