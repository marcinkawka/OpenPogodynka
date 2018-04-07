#!/bin/bash

mkdir incoming
cd incoming
'''
#Pobieranie danych hydrologicznych
base_url="https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/"
prefix="wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories"

mkdir dane_hydrologiczne
cd dane_hydrologiczne

for y in $(seq 1951 2016);
do
	mkdir $y
	cd $y
	`$prefix $base_url$y'/'`

	for f in *.zip
	do
		unzip $f
	done
	
	cd ..
done
cd ..
'''

#Pobieranie danych meteorologicznych
base_url="https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/"
prefix="wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories"

mkdir dane_meteorologiczne
cd dane_meteorologiczne

subdir="klimat/"
for y in $(seq 2001 2017);
do
	mkdir $y
	cd $y
	`$prefix $base_url$subdir$y'/'`

	for f in *.zip
	do
		unzip $f
	done
	
	cd ..
done
cd ..