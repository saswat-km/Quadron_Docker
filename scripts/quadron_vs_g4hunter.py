import argparse
import subprocess
from matplotlib import pyplot as plt
from os import path

import pandas as pd
from matplotlib_venn import venn2

column_names = ['chr1','start1','end1','score1','strand1','length1','chr2','start2','end2','score2','strand2','length2']

def quadron_vs_g4hunter(quadron_dir, g4hunter_dir, chromosome_num, overlap_percentage, 
                        g4hunter_window_size, g4hunter_threshold, output_dir, species):

  quadron_bed_file_name = f"quadron_{species}_chr{chromosome_num}.bed"
  quadron_bed_file_path = path.join(quadron_dir, quadron_bed_file_name)
  print(f'quadron_bed_file_path: {quadron_bed_file_path}')

  g4hunter_bed_file_name = f"g4hunter_{species}_{g4hunter_window_size}_{chromosome_num}_{g4hunter_threshold}.bed"
  g4hunter_bed_file_path = path.join(g4hunter_dir, g4hunter_bed_file_name)
  print(f'g4hunter_bed_file_path: {g4hunter_bed_file_path}')

  quadron_output_file_name = f"{species}_chr{chromosome_num}_window{g4hunter_window_size}_threshold{g4hunter_threshold}_quadron.bed"
  quadron_output_file_path = path.join(output_dir, quadron_output_file_name)
  print(f'quadron_output_file_path: {quadron_output_file_path}')

  g4hunter_output_file_name =f"{species}_chr{chromosome_num}_window{g4hunter_window_size}_threshold{g4hunter_threshold}_g4hunter.bed"
  g4hunter_output_file_path = path.join(output_dir, g4hunter_output_file_name)
  print(f'g4hunter_output_file_path: {g4hunter_output_file_path}')

  venn_diagram_output_file_name =f"{species}_chr{chromosome_num}_window{g4hunter_window_size}_threshold{g4hunter_threshold}_venn.png"
  venn_diagram_output_file_path = path.join(output_dir, venn_diagram_output_file_name)
  print(f'venn_diagram_output_file_path: {venn_diagram_output_file_path}')

  generate_quadron_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                          g4hunter_window_size, g4hunter_threshold, output_dir, species, quadron_output_file_path)

  generate_g4hunter_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                           g4hunter_window_size, g4hunter_threshold, output_dir, species, g4hunter_output_file_path)

  generate_venn_diagram(quadron_output_file_path, g4hunter_output_file_path, venn_diagram_output_file_path)


def generate_quadron_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                            g4hunter_window_size, g4hunter_threshold, output_dir, species, output_file_path):

  bedtools_intersect_cmd = f'bedtools intersect -wa -wb -f {overlap_percentage} -r -a {quadron_bed_file_path} -b {g4hunter_bed_file_path} -loj'

  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  # print(f'output: {output}')
  print(f'error: {error}')
  
  with open(output_file_path, "w") as fp:
    fp.write(output.decode())

def generate_g4hunter_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                             g4hunter_window_size, g4hunter_threshold, output_dir, species, output_file_path):

  bedtools_intersect_cmd = f'bedtools intersect -wa -wb -f {overlap_percentage} -r -a {g4hunter_bed_file_path} -b {quadron_bed_file_path} -loj'

  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  # print(f'output: {output}')
  print(f'error: {error}')
  
  with open(output_file_path, "w") as fp:
    fp.write(output.decode())


def generate_venn_diagram(quadron_output_file_path, g4hunter_output_file_path, venn_diagram_output_file_path):
  df_quadron = pd.read_csv(quadron_output_file_path, sep='\t', names=column_names, header=None)
  quadron_intersect = df_quadron[df_quadron['chr2'] != '.'].shape[0]
  quadron_only = df_quadron[df_quadron['chr2'] == '.'].shape[0]

  df_g4hunter = pd.read_csv(g4hunter_output_file_path, sep='\t', names=column_names, header=None)
  g4hunter_intersect = df_g4hunter[df_g4hunter['chr2'] != '.'].shape[0]
  g4hunter_only = df_g4hunter[df_g4hunter['chr2'] == '.'].shape[0]
  quadron_intersect_percentage = quadron_intersect / (quadron_intersect + quadron_only)

  venn_diagram_output_file_name = path.basename(venn_diagram_output_file_path)
  venn_diagram_title = venn_diagram_output_file_name.replace('_venn.png', '')

  print(f'quadron_output_file_path: {quadron_output_file_path}')
  print(f'quadron_intersect: {quadron_intersect}')
  print(f'quadron_only: {quadron_only}')
  print(f'g4hunter_output_file_path: {g4hunter_output_file_path}')
  print(f'g4hunter_intersect: {g4hunter_intersect}')
  print(f'g4hunter_only: {g4hunter_only}')

  plt.figure(figsize=(4,4))
  plt.title(venn_diagram_title)
  v = venn2(subsets = (quadron_only, g4hunter_only, quadron_intersect), set_labels = ('Quadron G4s', 'G4Hunter G4s'))
  plt.savefig(venn_diagram_output_file_path)


if __name__ == "__main__":
  argumentParser = argparse.ArgumentParser()

  argumentParser.add_argument("-q", "--quadron_dir", type=str, required=True)
  argumentParser.add_argument("-g", "--g4hunter_dir", type=str, required=True)
  argumentParser.add_argument("-n", "--chromosome_num", type=str, required=True)
  argumentParser.add_argument("-p", "--overlap_percentage", type=float, required=True)
  argumentParser.add_argument("-w", "--g4hunter_window_size", type=int, required=True)
  argumentParser.add_argument("-t", "--g4hunter_threshold", type=float, required=True)
  argumentParser.add_argument("-o", "--output_dir", type=str, required=True)
  argumentParser.add_argument("-s", "--species", type=str, required=True, default="hsapiens", choices=["hsapiens"])

  args = argumentParser.parse_args()
  quadron_vs_g4hunter(args.quadron_dir, args.g4hunter_dir, args.chromosome_num, args.overlap_percentage, args.g4hunter_window_size, args.g4hunter_threshold, args.output_dir, args.species)



