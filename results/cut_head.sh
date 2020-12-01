#!/bin/bash
for file in *.sql
do
	tail -n +9 $file  > cut$file
	rm $file
	sed -i 's/Time: //g' cut$file
	sed -i 's/ms//g' cut$file
	cp cut$file $file
	rm cut$file

done
