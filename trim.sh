#!/bin/bash
cd results
for file in *.sqle
do
	sed -i -E 's/([0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9])//g' $file
	sed -i 's/()//g' $file
done
