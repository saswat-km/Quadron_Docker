import argparse
import subprocess
from matplotlib import pyplot as plt
from os import path

import pandas as pd
from matplotlib_venn import venn2

column_names = ['chr', 'start', 'end', 'score', 'length', 'strand']

def quadron_vs_g4hunter(quadron_dir, g4hunter_dir, chromosome_num, g4hunter_window_size,
                        g4hunter_threshold, output_dir, species):

  quadron_bed_file_name = f"chr{chromosome_num}_out.bed"
  quadron_bed_file_path = path.join(quadron_dir, quadron_bed_file_name)
  print(f'quadron_bed_file_path: {quadron_bed_file_path}')
  df_quadron = pd.read_csv(quadron_bed_file_path, sep='\t', names=column_names, header=None)
  quadron_intervals_length = df_quadron["length"].sum()
  print(f"quadron_intervals_length: {quadron_intervals_length}")

  g4hunter_bed_file_name = f"chr{chromosome_num}-W{g4hunter_window_size}-S{g4hunter_threshold}-Merged-pruned.bed"
  g4hunter_bed_file_path = path.join(g4hunter_dir, g4hunter_bed_file_name)
  print(f'g4hunter_bed_file_path: {g4hunter_bed_file_path}')
  df_g4hunter = pd.read_csv(g4hunter_bed_file_path, sep='\t', names=column_names, header=None)
  g4hunter_intervals_length = df_g4hunter["length"].sum()
  print(f"g4hunter_intervals_length: {g4hunter_intervals_length}")

  intersect_file_name = f"{species}_chr{chromosome_num}_window{g4hunter_window_size}_threshold{g4hunter_threshold}_intersect.bed"
  intersect_file_path = path.join(output_dir, intersect_file_name)
  print(f'intersect_file_path: {intersect_file_path}')

  bedtools_intersect_cmd = f'bedtools intersect -a {quadron_bed_file_path} -b {g4hunter_bed_file_path}'
  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  print(f'error: {error}')

  with open(intersect_file_path, "w") as fp:
    fp.write(output.decode())

  df_intersect = pd.read_csv(intersect_file_path, sep='\t', names=["chr", "start", "end"], header=None, usecols=range(3))
  df_intersect["length"] = df_intersect["end"].astype(int) - df_intersect["start"].astype(int)
  intersect_intervals_length = df_intersect["length"].sum()
  print(f"intersect_intervals_length: {intersect_intervals_length}")

  venn_diagram_output_file_name =f"{species}_chr{chromosome_num}_window{g4hunter_window_size}_threshold{g4hunter_threshold}_venn.png"
  venn_diagram_output_file_path = path.join(output_dir, venn_diagram_output_file_name)
  print(f'venn_diagram_output_file_path: {venn_diagram_output_file_path}')

  generate_venn_diagram(quadron_intervals_length, g4hunter_intervals_length, intersect_intervals_length, venn_diagram_output_file_path)


def generate_venn_diagram(quadron_intervals_length, g4hunter_intervals_length, intersect_intervals_length, venn_diagram_output_file_path):
  venn_diagram_output_file_name = path.basename(venn_diagram_output_file_path)
  venn_diagram_title = venn_diagram_output_file_name.replace('_venn.png', '')

  plt.figure(figsize=(4,4))
  plt.title(venn_diagram_title)
  v = venn2(subsets = (quadron_intervals_length, g4hunter_intervals_length, intersect_intervals_length), set_labels = ('Quadron G4s', 'G4Hunter G4s'))
  plt.savefig(venn_diagram_output_file_path)


if __name__ == "__main__":
  argumentParser = argparse.ArgumentParser()

  argumentParser.add_argument("-q", "--quadron_dir", type=str, required=True)
  argumentParser.add_argument("-g", "--g4hunter_dir", type=str, required=True)
  argumentParser.add_argument("-n", "--chromosome_num", type=str, required=True)
  argumentParser.add_argument("-w", "--g4hunter_window_size", type=int, required=True)
  argumentParser.add_argument("-t", "--g4hunter_threshold", type=float, required=True)
  argumentParser.add_argument("-o", "--output_dir", type=str, required=True)
  argumentParser.add_argument("-s", "--species", type=str, required=True)

  args = argumentParser.parse_args()
  quadron_vs_g4hunter(args.quadron_dir, args.g4hunter_dir, args.chromosome_num, args.g4hunter_window_size, args.g4hunter_threshold, args.output_dir, args.species)
