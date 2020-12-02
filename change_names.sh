#!/bin/bash
cd results
for file in *.sqle
do
	newfile=${file::-1}
	mv $file $newfile
done
