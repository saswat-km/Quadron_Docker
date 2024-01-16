import argparse

def textToBed(input_text_file, output_bed_file, chromosome_name):
  data = open(input_text_file, 'r')
  data = data.readlines()

  f = open(output_bed_file, "w")

  # Write header
  f.write("Chrom\tStart\tStop\tScore\tStrand\tLength\n")

  adjust = 1 #adjust for quadron to bed conversion: bed file is zero-based
  for i in range(0, len(data)):
      crit = data[i].split()
      if crit[0] == "DATA:" and crit[4] != "NA":
          start = int(crit[1])
          length = int(crit[3])
          f.write("%s\t%i\t%i\t%.2f\t%s\t%i\n" %(chromosome_name, start-adjust, length+start-adjust, float(crit[4]), crit[2], length))


if __name__ == "__main__":
  argParser = argparse.ArgumentParser()

  argParser.add_argument("-i", "--input_text_file", type=str, required=True)
  argParser.add_argument("-o", "--output_bed_file", type=str, required=True)
  argParser.add_argument("-n", "--chromosome_name", type=str, required=True)
  args = argParser.parse_args()

  textToBed(args.input_text_file, args.output_bed_file, args.chromosome_name)
