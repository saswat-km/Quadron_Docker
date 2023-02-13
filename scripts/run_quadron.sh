#!/bin/bash

if [ $# -lt 2 ] || [ $# -gt 4 ]; then 
    echo "Incorrect number of parameters"
    echo "Specify input file, output file, number of CPUs (optional. Default is 8), and SeqPartitionBy (optional. Default is 1000000)"
    exit   
fi

FastaFile=$1
OutFile=$2
nCPU=${3:-8}
SeqPartitionBy=${4:-1000000}

echo "<$FastaFile> <$OutFile> <$nCPU> <$SeqPartitionBy>"

FastaFileName=`basename $FastaFile`
OutDir=`dirname $OutFile`
OutFileName=`basename $OutFile`

DOCKER_CMD="docker run -v $FastaFile:/$FastaFileName -v $OutDir:/output kxk302/quadron:1.0.0 /$FastaFileName /output/$OutFileName $nCPU $SeqPartitionBy"
echo $DOCKER_CMD
$DOCKER_CMD
