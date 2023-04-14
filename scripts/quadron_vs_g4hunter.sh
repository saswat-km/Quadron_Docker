#!/bin/bash

if [ $# -ne 7 ]; then 
    echo "Incorrect number of parameters"
    echo "Specify Quadron bed file directory, G4Hunter bed file directory, bedtools intersect overlap percentage, G4Hunter window size, g4Hunter threshold, output directory, and species"
    exit
fi

quadron_dir=$1
g4hunter_dir=$2
overlap_percentage=$3
g4hunter_window_size=$4
g4hunter_threshold=$5
output_dir=$6
species=$7

echo "quadron_dir: <$quadron_dir>"
echo "g4hunter_dir: <$g4hunter_dir>"
echo "overlap_percentage: <$overlap_percentage>"
echo "g4hunter_window_size: <$g4hunter_window_size>"
echo "g4hunter_threshold: <$g4hunter_threshold>"
echo "output_dir: <$output_dir>"
echo "species: <$species>"

for i in {1..22}; do python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir -g $g4hunter_dir -n $i -p $overlap_percentage -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir -s $species; done

python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir -g $g4hunter_dir -n X -p $overlap_percentage -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir -s $species

python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir -g $g4hunter_dir -n Y -p $overlap_percentage -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir -s $species

