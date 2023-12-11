#!/bin/bash

fasta_files_folder=${1:-"/Users/kxk302/workspace/non-B_gfa/v2/input"}
output_folder=${2:-"/Users/kxk302/workspace/Quadron_Docker/output/v2"}

species_list="Gorilla_gorilla Pan_troglodytes Symphalangus_syndactylus Homo_sapiens Pongo_abelii Pan_paniscus Pongo_pygmaeus" 

for species in ${species_list}
do
  echo "species: ${species}"
  ./scripts/run_quadrons.sh ${fasta_files_folder}/${species}/seqs_srcdir ${output_folder}/${species}
done
