import argparse
import subprocess
from os import path

def quadron_vs_g4hunter(quadron_dir, g4hunter_dir, chromosome_num, overlap_percentage, 
                        g4hunter_window_size, g4hunter_threshold, output_dir, species):

  quadron_bed_file_name = f"quadron_{species}_chr{chromosome_num}.bed"
  quadron_bed_file_path = path.join(quadron_dir, quadron_bed_file_name)
  print(f'quadron_bed_file_path: {quadron_bed_file_path}')

  g4hunter_bed_file_name = f"g4hunter_{species}_{g4hunter_window_size}_{chromosome_num}_{g4hunter_threshold}.bed"
  g4hunter_bed_file_path = path.join(g4hunter_dir, g4hunter_bed_file_name)
  print(f'g4hunter_bed_file_path: {g4hunter_bed_file_path}')

  generate_quadron_g4hunter_intersect_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                                             g4hunter_window_size, g4hunter_threshold, output_dir, species)

  generate_quadron_only_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                               g4hunter_window_size, g4hunter_threshold, output_dir, species)

  generate_g4hunter_only_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                                 g4hunter_window_size, g4hunter_threshold, output_dir, species)

def generate_quadron_g4hunter_intersect_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                                               g4hunter_window_size, g4hunter_threshold, output_dir, species):

  output_file_name = f"quadron_vs_g4hunter_window{g4hunter_window_size}_threshold{g4hunter_threshold}_{species}_chr{chromosome_num}_intersect.bed"
  output_file_path = path.join(output_dir, output_file_name)
  print(f'output_file_path: {output_file_path}')

  bedtools_intersect_cmd = f'bedtools intersect -wa -wb -f {overlap_percentage} -a {quadron_bed_file_path} -b {g4hunter_bed_file_path}' 

  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  # print(f'output: {output}')
  print(f'error: {error}')
  
  with open(output_file_path, "w") as fp:
    fp.write(output.decode())


def generate_quadron_only_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                                 g4hunter_window_size, g4hunter_threshold, output_dir, species):
  
  output_file_name = f"quadron_vs_g4hunter_window{g4hunter_window_size}_threshold{g4hunter_threshold}_{species}_chr{chromosome_num}_quadron_only.bed"
  output_file_path = path.join(output_dir, output_file_name)
  print(f'output_file_path: {output_file_path}')

  bedtools_intersect_cmd = f'bedtools intersect -v -f {overlap_percentage} -a {quadron_bed_file_path} -b {g4hunter_bed_file_path}'

  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  # print(f'output: {output}')
  print(f'error: {error}')
  
  with open(output_file_path, "w") as fp:
    fp.write(output.decode())


def generate_g4hunter_only_report(quadron_bed_file_path, g4hunter_bed_file_path, chromosome_num, overlap_percentage,
                                  g4hunter_window_size, g4hunter_threshold, output_dir, species):
  
  output_file_name = f"quadron_vs_g4hunter_window{g4hunter_window_size}_threshold{g4hunter_threshold}_{species}_chr{chromosome_num}_g4hunter_only.bed"
  output_file_path = path.join(output_dir, output_file_name)
  print(f'output_file_path: {output_file_path}')

  bedtools_intersect_cmd = f'bedtools intersect -v -f {overlap_percentage} -b {quadron_bed_file_path} -a {g4hunter_bed_file_path}'

  process = subprocess.Popen(bedtools_intersect_cmd.split(), stdout=subprocess.PIPE)
  output, error = process.communicate()
  # print(f'output: {output}')
  print(f'error: {error}')
  
  with open(output_file_path, "w") as fp:
    fp.write(output.decode())


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
  quadron_vs_g4hunter(args.quadron_dir, args.g4hunter_dir, args.chromosome_num, args.overlap_percentage,
                      args.g4hunter_window_size, args.g4hunter_threshold, args.output_dir, args.species)



