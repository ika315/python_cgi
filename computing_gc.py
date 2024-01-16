#!/usr/bin/python3

import sys
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-f", dest="filepath", help="path - path to file in which the fasta file is located")
(options, args) = parser.parse_args()

filepath = options.filepath


def count_gc(sequence):
    sum_gc = 0

    total_nucleotides = len(sequence)

    for nucleotide in sequence:
        if nucleotide == "G" or nucleotide == "C":
            sum_gc += 1

    gc_content = sum_gc / total_nucleotides * 100

    # format is generally used to replace a value with another desired value
    # takes the value in parentheses and inserts it into the formatted string (6f)

    return gc_content


def find_max_gc(fasta_dict):
    max_gc_id = ""
    max_gc_content = 0

    for sequence_id, sequence in fasta_dict.items():
        current_gc_content = count_gc(sequence)
        if current_gc_content > max_gc_content:
            max_gc_content = current_gc_content
            max_gc_id = sequence_id

    return max_gc_id, "{:.6f}".format(max_gc_content)

fasta_dict = {}
current_id = ""
current_seq = []

with open(filepath, "r") as my_file:
    for line in my_file:
        line = line.strip()
        if line.startswith(">"):
            fasta_dict[current_id] = ''.join(current_seq)

            current_id = line[1:]

            current_seq = []

            continue

        current_seq.append(line)

    fasta_dict[current_id] = ''.join(current_seq)
    fasta_dict = {k: v for k, v in fasta_dict.items() if k and v}  # removes empty key&value pairs

    # writing into output file
    result_tuple = find_max_gc(fasta_dict)
    max_seq_id, max_seq = result_tuple

    print(max_seq_id + "\n" + max_seq)

# executing code
# input_file = "C:\\Users\\irem3\\Downloads\\rosalind_gc_1049_1_dataset.txt"
# read_fasta(input_file)
