#!/bin/bash
base_url="https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/"
prefix="wget -e robots=off --cut-dirs=3 --user-agent=Mozilla/5.0 --reject="index.html*" --no-parent --recursive --relative --level=1 --no-directories"
mkdir incoming
cd incoming

years=(2016 2015 2014 2013 2012 2011 2010 2009 2008)
for y in ${years[*]}
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

