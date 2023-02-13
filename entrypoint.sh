#!/bin/bash

if [ $# -lt 2 ] || [ $# -gt 4 ]; then 
    echo "Incorrect number of parameters"
    echo "Specify Fasta file, Output file, Number of CPUs (optional. Default is 8), and SeqPartitionBy (optional. Default is 1000000)"
fi

FastaFile=$1
OutFile=$2
nCPU=${3:-8}
SeqPartitionBy=${4:-1000000}

echo "<$FastaFile> <$OutFile> <$nCPU> <$SeqPartitionBy>"
cd ./scripts
Rscript run_quadron.R $FastaFile $OutFile $nCPU $SeqPartitionBy
