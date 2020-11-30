#!/bin/bash
for file in *.sql
do
	tail -n +9 $file > cut$file
	rm $file
	cp cut$file $file
	rm cut$file

done
