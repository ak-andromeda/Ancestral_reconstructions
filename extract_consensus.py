import pandas as pd
import sys
import Bio
from Bio import SeqIO

def read_in_data(result):

    result = open(result, "r")
    result_list = []
    for l in result:
        l = l.strip()
        result_list.append(l)

    return result_list

def get_consensus_seqs(result_list,name):

    con_seq_dictionary = {}
    data_base = SeqIO.parse("Viridi_30_consensus_sequences.fasta", "fasta")
    for record in data_base:
        con_seq_dictionary[record.description] = str(record.seq)

    result_seq_dict = {}
    for result in result_list:
        seq_desc = result + "-sample1"
        con_seq = con_seq_dictionary[seq_desc]
        result_seq_dict[seq_desc] = con_seq

    file_name = name + "_con_seqs.fasta"
    file = open(file_name, "w")

    for desc, seq in result_seq_dict.items():
        line = ">" + desc + "\n" + seq + "\n"
        file.write(line)
    file.close


def main():
    result_list = read_in_data(result)
    get_consensus_seqs(result_list,name)



if __name__ == "__main__":
    result = sys.argv[1]
    name = sys.argv[2]
    main()
