#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Incorrect number of parameters"
  echo "Specify the input fasta files folder and the output folder"
  exit
fi

FastaFilesFolder=$1
OutputFolder=$2

echo "FastaFilesFolder: <$FastaFilesFolder>"
echo "OutputFolder: <$OutputFolder>"

for file_path in $(ls ${FastaFilesFolder}/*.fa)
do
  file_name=$(basename ${file_path})
  ./scripts/run_quadron.sh  ${file_path} ${OutputFolder}/${file_name/.fa/_out.txt} 8
done
