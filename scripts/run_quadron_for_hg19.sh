#!/bin/bash

if [ $# -lt 2 ]; then
  echo "Incorrect number of parameters"
  echo "Specify the input fasta files folder, the output folder, and optionally, the fasta file extension (default: .fa)"
  exit
fi

FastaFilesFolder=$1
OutputFolder=$2
FastaExt=${3:-".fa"}

echo "FastaFilesFolder: <$FastaFilesFolder>"
echo "OutputFolder: <$OutputFolder>"
echo "FastaExt: <$FastaExt>"

for file_path in $(ls ${FastaFilesFolder}/*${FastaExt})
do
  file_name=$(basename ${file_path})
  ./scripts/run_quadron.sh  ${file_path} ${OutputFolder}/${file_name/${FastaExt}/_out.txt} 8
done
