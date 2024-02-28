#!/bin/bash

if [ $# -ne 5 ]; then
    echo "Incorrect number of parameters"
    echo "Specify Quadron bed file directory, G4Hunter bed file directory, G4Hunter window size, G4Hunter threshold, and output directory"
    exit
fi

quadron_dir=$1
g4hunter_dir=$2
g4hunter_window_size=$3
g4hunter_threshold=$4
output_dir=$5

echo "quadron_dir: <$quadron_dir>"
echo "g4hunter_dir: <$g4hunter_dir>"
echo "g4hunter_window_size: <$g4hunter_window_size>"
echo "g4hunter_threshold: <$g4hunter_threshold>"
echo "output_dir: <$output_dir>"

for species in "Gorilla_gorilla" "Pan_troglodytes" "Symphalangus_syndactylus" "Homo_sapiens" "Pongo_abelii" "Pan_paniscus" "Pongo_pygmaeus"
do
  echo "species: ${species}"

  for i in {1..22}; do python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir/$species -g $g4hunter_dir/$species -n $i -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir/$species -s $species; done

  python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir/$species -g $g4hunter_dir/$species -n X -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir/$species -s $species;

  python3 ./scripts/quadron_vs_g4hunter.py -q $quadron_dir/$species -g $g4hunter_dir/$species -n Y -w $g4hunter_window_size -t $g4hunter_threshold -o $output_dir/$species -s $species;
done
