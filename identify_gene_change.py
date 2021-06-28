import pandas as pd
import sys

def read_in_data(df_name):

    df = pd.read_csv(df_name)

    return df

def extract_gene_families(df):

    gene_families = []
    gene_families_long = list(df.Gene_family)
    for gf in gene_families_long:
        gf = gf.split(".")[0]
        gene_families.append(gf)

    return gene_families

def find_intersection(list1, list2):

    return set(list1).intersection(list2)

def find_difference(list1,list2):

    intersection = find_intersection(list1,list2)
    lost = set(list1).difference(list2)
    gained = set(list2).difference(list1)

    return lost, gained

def write_results(results, name):

    file = open(name + ".txt", "w")
    for l in results:
        line = l + "\n"
        file.write(line)
    file.close()

def make_df_of_lost(lost_genes,df1,df2):

    print(df1)
    lost_genes = list(lost_genes)
    lost_genes_d = {"Gene_family":lost_genes}
    df_lost = pd.DataFrame.from_dict(lost_genes_d)
    df_lost = df_lost["Gene_family"] + ".bmge.ufboot.ale.ml_rec"
    df_merge = pd.merge(df_lost,df1, on = "Gene_family", how = "left")
    df_lost_at_node = df_merge[["Gene_family","Node","Copies"]]
    df_lost_at_node["Lost_at"] =  df2["Node"]
    df_name = "Gene_lost_between_nodes.csv"
    df_lost_at_node.to_csv(df_name)

    print(len(lost_genes))
    print(len(df_lost_at_node))

def main():
    df1 = read_in_data(df1_name)
    df2 = read_in_data(df2_name)
    df1_gf = extract_gene_families(df1)
    df2_gf = extract_gene_families(df2)
    lost, gained = find_difference(df1_gf,df2_gf)
    write_results(lost,"Lost_genes")
    write_results(gained,"Gained_gened")
    make_df_of_lost(lost, df1, df2)


if __name__ == "__main__":
    df1_name = sys.argv[1]
    df2_name = sys.argv[2]
    main()
