import pandas as pd
from collections import Counter
import sys


def make_GO_term_dict(GO_terms):

    ids = []
    functions = []

    go = open(GO_terms, "r")
    for line in go:
        line = line.strip()
        if line.startswith("id:"):
            GO_term = line[4:]
            ids.append(GO_term)
        if line.startswith("name:"):
            function = line[6:]
            functions.append(function)
        if line.startswith("alt_id:"):
            ids.append(line[8:])
            functions.append(function)

    GO_dict = {}
    file = open("GO_term_id_function.csv", "w")
    for key, val in zip(ids,functions):
        line = key + "," + val + "\n"
        file.write(line)
        GO_dict[key] = val
    file.close()

    return GO_dict

def read_in_data(data):

    df = pd.read_csv(data, sep='\t')
    print(df.head())
    return df

def isolate_go_terms(df):

    Gene_families = df["#query"].to_list()
    GO_list = df["GOs"].to_list()
    reformat_list = []
    gf_list = []
    for go, gf in zip(GO_list,Gene_families):
        go = str(go)
        sep_list =  go.split(",")
        for go_i in sep_list:
            reformat_list.append(go_i)
            gf_list.append(gf)

    data = {"Gene_family":gf_list,"GO_term":reformat_list}
    df = pd.DataFrame.from_dict(data)

    return df

def find_functions(GO_data,GO_dict,output_file):


    GO_terms = list(GO_data.GO_term)
    gene_families = list(GO_data.Gene_family)


    functions = []
    go_terms = []
    gfs = []

    zipped = zip(GO_terms,gene_families)
    for go_term, gf in zipped:

        if go_term == "nan":
            continue
        else:
            function = GO_dict[go_term]
            functions.append(function)
            go_terms.append(go_term)
            gfs.append(gf)


    data = {"Gene_family":gfs,"Go_term":go_terms,"Function":functions}
    df = pd.DataFrame.from_dict(data)
    file_name = output_file + "functions_raw.csv"
    df.to_csv(file_name)

    lost_function_freq = Counter(list(df.Function))
    return(lost_function_freq)

def write_results(dictionary, file_name):

    file = open(file_name + "summarised.csv", "w")
    file.write("Function,Frequency\n")
    for key, val in dictionary.items():
        key = key.replace(",","-")
        line = key + "," + str(val) + "\n"
        file.write(line)
    file.close()

def main():
    GO_dict = make_GO_term_dict(GO_terms)
    df = read_in_data(data)
    GO_data = isolate_go_terms(df)
    lost_function_freq = find_functions(GO_data,GO_dict,output_file)
    write_results(lost_function_freq, output_file)

if __name__ == "__main__":
    GO_terms = sys.argv[1]
    data = sys.argv[2]
    output_file = sys.argv[3]
    main()
