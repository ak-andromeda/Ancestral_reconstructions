import pandas as pd
import sys
import Bio
from Bio import SeqIO

def read_in_data(file):

    df = pd.read_csv(file)
    print(df.head())
    return df

def get_genes_at_node(df):

    gf_at_node = list(df.Gene_family)
    gf_code_at_node = [gene.split(".")[0] for gene in gf_at_node]

    return(gf_code_at_node)

def copy_consenus_genes_of_node(gf_code_at_node,consensus_sequences):

    records_at_node = {}
    con_records = SeqIO.parse(consensus_sequences,"fasta")
    for record in con_records:
        code = (str(record.description)).split("-")[0]
        for gf_code in gf_code_at_node:
            if gf_code == code:
                records_at_node[str(record.description)] = str(record.seq)

    return records_at_node

def write_results(records_at_node, node):

    files_created = 0
    file_name = node + "_consensus_sequenes_present.fasta"
    file = open(file_name, "w")
    for seq, desc in records_at_node.items():
        seq = seq.split("-")[0]
        line = ">" + seq + "\n" + desc + "\n"
        file.write(line)
        files_created += 1
    file.close()

    print("Consensus sequences present at the node stated are in: \n",
           "node + _consensus_sequenes_present.fasta")
    print("files at node =", files_created)


def main():

    df = read_in_data(results_file)
    genes_at_node = get_genes_at_node(df)
    records_at_node = copy_consenus_genes_of_node(genes_at_node, consensus_sequences)
    write_results(records_at_node, node)


if __name__ == "__main__":
    results_file = sys.argv[1]
    consensus_sequences = sys.argv[2]
    node = sys.argv[3]
    main()
