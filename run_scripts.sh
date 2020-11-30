#!/bin/bash
cd scripts
for file in *
do
	resfile=res_$file
	psql -f $file >> ../results/$resfile
done
