#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Incorrect number of parameters"
  echo "Specify the Quadron output folder"
  exit
fi

OutputFolder=$1

echo "OutputFolder: <$OutputFolder>"

for file_path in $(ls ${OutputFolder}/*_out.txt)
do
  file_name=$(basename ${file_path})
  chromosome=${file_name%%_out.txt}
  echo "Chromosome: <$chromosome>"
  python3 ./scripts/quadron_txt2bed.py -i ${file_path} -o ${OutputFolder}/${file_name/_out.txt/_GQ.tsv} -n $chromosome
done
