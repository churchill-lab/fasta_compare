#!/usr/bin/env python

import argparse
import os
import subprocess
import sys

import pysam

def write_header(header, out):
    out.write(">")
    out.write(header)
    out.write("\n")

def write_sequence(sequence, out):
    for i in xrange(0, len(sequence), 60):
        out.write(sequence[i:i+60])
        out.write("\n")

def muscle_it(fasta_file):
    subprocess.call(['muscle', '-clw', '-in', fasta_file])

def diff_files(file1, file2):

    fasta_1 = pysam.FastaFile(file1)
    fasta_2 = pysam.FastaFile(file2)


    fa_equal = {}
    fa_diff = {}

    for seq_id1 in fasta_1.references:
        if seq_id1 in fasta_2.references:

            if fasta_1.fetch(seq_id1) == fasta_2.fetch(seq_id1):
                print "Comparing {} ... EQUAL".format(seq_id1)
                fa_equal[seq_id1] = seq_id1
            else:
                print "Comparing {} ... DIFFERENT".format(seq_id1)
                fa_diff[seq_id1] = seq_id1

                muscle_file = "muscle_{}.fa".format(seq_id1)
                mf = open(muscle_file, "w")

                write_header(seq_id1 + "_1", mf)
                write_sequence(fasta_1.fetch(seq_id1), mf)

                write_header(seq_id1 + "_2", mf)
                write_sequence(fasta_2.fetch(seq_id1), mf)

                mf.close()

                muscle_it(muscle_file)
                os.remove(muscle_file)

    if len(fa_equal) == 0 and len(fa_diff) == 0:
        print "No matching id's found in files."
    else:
        print "# EQUAL ENTRIES: {0}".format(len(fa_equal))
        print "# DIFFERENT ENTRIES: {0}".format(len(fa_diff))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fasta1")
    parser.add_argument("fasta2")
    args = parser.parse_args()

    try:
        diff_files(args.fasta1, args.fasta2)
    except Exception:
        print "Error occurred, please make sure 'muscle' executable is on your path"



