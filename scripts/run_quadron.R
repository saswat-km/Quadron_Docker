###############################################################################
# Added lines to run Quadron in specific R environment                        #
###############################################################################

require(renv)
renv::restore()
library(xgboost)
sessionInfo()

print("NOTE: Loading Quadron core...", quote=FALSE)

# This specifies the location of quadron. Please set to the folder where
# you performed 'git clone https://github.com/aleksahak/Quadron'  This provides
# the 'Quadron-master' folder with 'Quadron.lib'
base::load("/Quadron/Quadron.lib")

# this is the actual command, that reads in the fasta file, and outputs the
# quadron file. the fasta input file requirements are a bit unclear to me, but
# a two line fasta (one line header, the other just the sequence) works fine. 
# for the output file, there are two things to consider: First, the position
# given for any motif is 1-based, i.e. it does not correspond to a bed file. 
# To remedy, simply subtract 1 from the given position. Second, it seems to
# me that quadron does not really understand fasta id headers, i.e. to get
# chromosome IDs, it is best to split the input reference file by chromosome.
# The example outputfile below should illustrate tat. There you can also
# see that the #DATA lines are the ones of interest, but do not contain
# the ID header

args = commandArgs(trailingOnly=TRUE)
argsLen <- length(args);
if (argsLen < 2 || argsLen > 4) {
  stop("Specify Fasta file, Output file, Number of CPUs (optional. Default is 8), and SeqPartitionBy (optional. Default is 1000000)", call.=FALSE) 
} 

FastaFile_in = paste0(args[1])
OutFile_in = paste0(args[2])
nCPU_in <- if (argsLen < 3) 8 else strtoi(args[3]);
SeqPartitionBy_in <- if (argsLen < 4) 1000000 else strtoi(args[4]);

sprintf("FastaFile_in: %s", FastaFile_in)
sprintf("OutFile_in: %s", OutFile_in)
sprintf("nCPU_in: %s", nCPU_in)
sprintf("SeqPartitionBy_in: %s", SeqPartitionBy_in)

Quadron(FastaFile= FastaFile_in, 
        OutFile  = OutFile_in,
        nCPU     = nCPU_in,
        SeqPartitionBy = SeqPartitionBy_in)

# Example output file:

#NOTE: *:)* Sequence-Based Prediction of DNA Quadruplex Structures *(:*
#NOTE: Date - Fri Jan  6 05:27:26 2023
#NOTE: Parsing the sequence...
#NOTE: The digested sequence is of 16715-nt length.
#NOTE: Scanning the sequence for G4 motifs...
#NOTE: Extracting features using 8 processing core(s).
#NOTE: Pre-processing the extracted features...
#NOTE: Executing the Quadron core...
#NOTE: Formatting and saving the results...
#HEADER: **********************************************************************
#HEADER: POS - position of the genomic start for the PQS_L12, i.e. potential
#HEADER:       quadruplex sequence with canonical G3+ tracts and maximum
#HEADER:       loop size of 12 nt. The genomic start position thus
#HEADER        corresponds to 5'-start for PQS_L12 sequence, if that
#HEADER:       is in the '+' strand, and to 3'-end for the one in '-' strand.
#HEADER: STR - strand where the PQS_L12 is located. The supplied sequence is
#HEADER:       treated as '+'.
#HEADER: L   - length of the retrieved PQS_L12 motif.
#HEADER: Q   - Quadron prediction of the corresponding G4-seq mismatch level
#HEADER:       for a polymerase stalling at quadruplex sites. NA indicates that
#HEADER:       the PQS_L12 is too close to the sequence termini for the 50-nt
#HEADER:       flanks to be analysed, as required for Quadron predictions.
#HEADER:       Q values above 19 indicate that the corresponding PQS_L12 is
#HEADER:       a highly stable G-quadruplex.
#HEADER: SEQUENCE - PQS_L12 sequence in the supplied + strand. If, for a
#HEADER:       particular PQS_L12, str is '+', then this is the PQS_L12 sequence
#HEADER:       in 5'-3' direction. Otherwise, for '-' strand motifs, SEQUENCE
#HEADER:       would be reverse complementary to the actual PQS_L12 (i.e.
#HEADER:       complementary to its 3'-5'span).
#HEADER: **********************************************************************
#HEADER: POS STR L    Q SEQUENCE
#HEADER: **********************************************************************
#DATA:    52 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA:   885 + 23 14.38 GGGCAGGGGCTCCCTGGGCTGGG
#DATA:  1916 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA:  2751 + 29 17.47 GGGCGAAGGGGCGAGCCAGGGGTAAGGGG
#DATA:  3787 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA:  4622 + 15 32.93 GGGAGGGAGGGAGGG
#DATA:  5635 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA:  6470 + 15 30.17 GGGTGGGTGGGTGGG
#DATA:  7483 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA:  8318 + 22 21.96 GGGGCCGGGGCCGGGGCCGGGG
#DATA:  9338 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA: 10173 + 22 29.70 GGGGTGGGGGGAGGGGGGAGGG
#DATA: 11193 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA: 12036 + 18 30.86 GGGAGGGAGGTGGGGGGG
#DATA: 13052 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#DATA: 13887 + 27 32.85 GGGGGATGGGGTTGGAATGGGGGCGGG
#DATA: 14912 + 33  9.42 GGGCGCGTCAGCGGGTGTTGGCGGGTGTCGGGG
#NOTE: ************************************************************************
#NOTE: Quadron is done!
#NOTE: For questions and bug reports, please contact Alex Sahakyan via
#NOTE: aleksahak[at]cantab.net attaching all the relevant files.
