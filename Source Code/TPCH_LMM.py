import sys
import os
import pandas as pd
import math

argv = sys.argv

if len(argv) != 2:
    print("Use 'python TPCH_LMM.py <DIR>', where DIR is the name of the directory containing the database.")
    exit()

directory = os.fsdecode(argv[1])

# Reading csv into dataframe
customer = pd.read_csv(directory+"/customer.csv")
lineitem = pd.read_csv(directory+"/lineitem.csv")
nation = pd.read_csv(directory+"/nation.csv")
orders = pd.read_csv(directory+"/orders.csv")
part = pd.read_csv(directory+"/part.csv")
partsupp = pd.read_csv(directory+"/partsupp.csv") 
region = pd.read_csv(directory+"/region.csv")
supplier = pd.read_csv(directory+"/supplier.csv")

# Initialising an empty temporary dataframe
temp_df = pd.DataFrame()

table = {
    'LABEL': [],
    'VALUE': [],
    'LENGTH': [],
}

L1 = {
    'LABEL': [],
    'LENGTH': [],
}

PPI_DL_L2 = {
    'LABEL': [],
    'VALUE': [],
    'LENGTH': [],
}

PPI_TL_L2 = {
    'LABEL': [],
    'VALUE': [],
    'LENGTH': [],
}

PPI_TL_L3 = {
    'LABEL': ['nation_region_REGIONKEY', 'supplier_nation_NATIONKEY', 'customer_nation_NATIONKEY', 'customer_supplier_NATIONKEY', 'partsupp_supplier_SUPPKEY', 'partsupp_part_PARTKEY', 'lineitem_partsupp_PARTKEY', 'lineitem_partsupp_SUPPKEY', 'lineitem_orders_ORDERKEY', 'orders_customer_CUSTKEY'],
    'VALUE': [['nation', 'region'], ['supplier', 'nation'], ['customer', 'nation'], ['customer', 'supplier'], ['partsupp', 'supplier'], ['partsupp', 'part'], ['lineitem', 'partsupp'], ['lineitem', 'partsupp'], ['lineitem', 'orders'], ['orders', 'CUSTKEY_customer']],
    'LENGTH': [],
}

FPI_L2 = {
    'LABEL': [],
    'VALUE': [],
    'LENGTH': [],
}


# To print the name of a variable
def print_var_name(variable):
    for name in globals():
        if eval(name) is variable:
            return name

# To change the index of the dataframe df
def change_index(df, temp_df, count):
    
    count_start = count
    count_end = count_start + len(df)
    set_range = pd.Series(range(count_start,count_end))
    temp_df = df.set_index([set_range])
    return temp_df, count_end

# To count the byte size of each row of the dataframes
def row_size(all_new_dfs, table):
    
    for key in all_new_dfs:
        for index in all_new_dfs[key].index:
            table['LABEL'].append(index)
        x = all_new_dfs[key].to_string(header=False, index=False, index_names=False).split('\n')
        vals = [','.join(ele.split()) for ele in x]
        for i in range(len(vals)):
            table['LENGTH'].append(math.ceil(len(vals[i])/16))  
    return table

# To tabulate results of table retrievals
def table_retrieval(all_new_dfs, table):
    
    for key in all_new_dfs:
        table['LABEL'].append(key[4:])
        table['VALUE'].append(list(all_new_dfs[key].index))
        table['LENGTH'].append(len(list(all_new_dfs[key].index)))
    return table

# To tabulate results of joins for Partially Precomputed Indexing (PPI) - Double Layer (DL) Scheme
def PPI_DL_join(df1, df2, column, table):

    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())
    
    overlap = key1.intersection(key2)
    
    index1 = []
    index2 = []
    
    for i in list(df1[column].index):
        if {df1[column][i]}.issubset(overlap):
            index1.append(i)
    print_var_name(df1)
    table['LABEL'].append(column+'_'+print_var_name(df1)[4:])
    table['VALUE'].append(index1)
    table['LENGTH'].append(len(index1))

    for i in list(df2[column].index):
        if {df2[column][i]}.issubset(overlap):
            index2.append(i)
    table['LABEL'].append(column+'_'+print_var_name(df2)[4:])
    table['VALUE'].append(index2)
    table['LENGTH'].append(len(index2))
    
    return table

# To tabulate results of joins for Partially Precomputed Indexing (PPI) - Triple Layer (TL) Scheme
def PPI_TL_join(df1, df2, column, table):

    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())
    
    overlap = key1.intersection(key2)
    
    index1 = []
    index2 = []

    for i in list(df2[column].index):
        if {df2[column][i]}.issubset(overlap):
            index2.append(i)
    table['LABEL'].append(column+'_'+print_var_name(df2)[4:])
    table['VALUE'].append(index2)
    table['LENGTH'].append(len(index2))
    
    return table

# To compute # rows in join output
def num_join_rows(df1, df2, column): 
    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())
    
    overlap = key1.intersection(key2)
    multiply = []
    for i in overlap:
        multiply.append(dict1[i] * dict2[i])

    return sum(multiply)


# Changing indexes of all dataframes    
new_customer = pd.DataFrame(customer)
new_lineitem, count = change_index(lineitem, temp_df, len(customer))
new_nation, count1 = change_index(nation, temp_df, count)
new_orders, count = change_index(orders, temp_df, count1)
new_part, count1 = change_index(part, temp_df, count)
new_partsupp, count = change_index(partsupp, temp_df, count1)
new_region, count1 = change_index(region, temp_df, count)
new_supplier, count = change_index(supplier, temp_df, count1)

# The csv files have a NA column at the end so it is removed
new_customer = new_customer.iloc[: , :-1]
new_lineitem = new_lineitem.iloc[: , :-1]
new_nation = new_nation.iloc[: , :-1]
new_orders = new_orders.iloc[: , :-1]
new_part = new_part.iloc[: , :-1]
new_partsupp = new_partsupp.iloc[: , :-1]
new_region = new_region.iloc[: , :-1]
new_supplier = new_supplier.iloc[: , :-1]

all_new_dfs = {key: value for key, value in locals().items() if (isinstance(value, pd.core.frame.DataFrame) and key[0:3] == 'new')}

newL1 = row_size(all_new_dfs, L1)
"""
print("--------------------------------------------------------------------------------------------------")
print("L1: \n")
df = pd.DataFrame(newL1)
print(df)
"""

# Setting up LMM for Partially Precomputed Indexing (PPI) - Double Layer (DL) Scheme
table1 = table_retrieval(all_new_dfs, table)
table = PPI_DL_join(new_nation, new_region, 'REGIONKEY', table1)
table1 = PPI_DL_join(new_supplier, new_nation, 'NATIONKEY', table)
table = PPI_DL_join(new_customer,  new_nation, 'NATIONKEY', table1)
table1 = PPI_DL_join(new_customer, new_supplier, 'NATIONKEY', table)
table = PPI_DL_join(new_partsupp, new_supplier, 'SUPPKEY', table1)
table1 = PPI_DL_join(new_partsupp, new_part, 'PARTKEY', table)
table = PPI_DL_join(new_lineitem, new_partsupp, 'PARTKEY', table1)
table1 = PPI_DL_join(new_lineitem, new_partsupp, 'SUPPKEY', table)
table = PPI_DL_join(new_lineitem, new_orders, 'ORDERKEY', table1)
PPI_DL_L2 = PPI_DL_join(new_orders, new_customer, 'CUSTKEY', table)
"""
print("--------------------------------------------------------------------------------------------------")
print("PPI_DL_L2: \n")
df = pd.DataFrame(PPI_DL_L2)
print(df)
"""
print("--------------------------------------------------------------------------------------------------")
print("\nComputing the sizes of PP2 indexes:\n")
print("\n(PP2 Level 1) \n")
print("Total number of labels:", len(newL1['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(newL1['LENGTH']))

print("\n(PP2 Level 2) \n")
print("Total number of labels:", len(PPI_DL_L2['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(PPI_DL_L2['LENGTH']))


# Setting up LMM for Partially Precomputed Indexing (PPI) - Triple Layer (TL) Scheme
table1 = table_retrieval(all_new_dfs, PPI_TL_L2)
PPI_TL_L2 = PPI_TL_join(new_orders, new_customer, 'CUSTKEY', table1)

for item in PPI_TL_L3['VALUE']:
    PPI_TL_L3['LENGTH'].append(len(item))
"""
print("--------------------------------------------------------------------------------------------------")
print("PPI_TL_L2: \n")
df = pd.DataFrame(PPI_TL_L2)
print(df)
"""
print("--------------------------------------------------------------------------------------------------")
print("\nComputing the sizes of PP3 indexes:\n")
print("\n(PP3 Level 1) \n")
print("Total number of labels:", len(newL1['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(newL1['LENGTH']))

print("\n(PP3 Level 2) \n")
print("Total number of labels:", len(PPI_TL_L2['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(PPI_TL_L2['LENGTH']))
"""
print("--------------------------------------------------------------------------------------------------")
print("PPI_TL_L3: \n")
df = pd.DataFrame(PPI_TL_L3)
print(df)
"""
print("\n(PP3 Level 3) \n")
print("Total number of labels:", len(PPI_TL_L3['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(PPI_TL_L3['LENGTH']))
print("\nRemark: 20 blocks of values in total since each label has 2 values and each value is at most 16 ASCII characters/bytes = 128 bits")


# Setting up LMM for Fully Precomputed Indexing (FPI) Scheme
table1 = table_retrieval(all_new_dfs, FPI_L2)
table1.pop('VALUE')
for item in PPI_TL_L3['LABEL']:
    table1['LABEL'].append(item)
table1['LENGTH'].append(2*num_join_rows(new_nation, new_region, 'REGIONKEY'))
table1['LENGTH'].append(2*num_join_rows(new_supplier, new_nation, 'NATIONKEY'))
table1['LENGTH'].append(2*num_join_rows(new_customer, new_nation, 'NATIONKEY'))
table1['LENGTH'].append(2*num_join_rows(new_customer, new_supplier, 'NATIONKEY'))
table1['LENGTH'].append(2*num_join_rows(new_partsupp, new_supplier, 'SUPPKEY'))
table1['LENGTH'].append(2*num_join_rows(new_partsupp, new_part, 'PARTKEY'))
table1['LENGTH'].append(2*num_join_rows(new_lineitem, new_partsupp, 'PARTKEY'))
table1['LENGTH'].append(2*num_join_rows(new_lineitem, new_partsupp, 'SUPPKEY'))
table1['LENGTH'].append(2*num_join_rows(new_lineitem, new_orders, 'ORDERKEY'))
table1['LENGTH'].append(2*num_join_rows(new_orders, new_customer, 'CUSTKEY'))   
FPI_L2 = table1
"""
print("--------------------------------------------------------------------------------------------------")
print("FPI_L2: \n")
df = pd.DataFrame(FPI_L2)
print(df)
"""
print("--------------------------------------------------------------------------------------------------")
print("\nComputing the sizes of FP2 indexes:\n")
print("\n(FP2 Level 1) \n")
print("Total number of labels:", len(newL1['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(newL1['LENGTH']))

print("\n(FP2 Level 2) \n")
print("Total number of labels:", len(FPI_L2['LABEL']))
print("Total size of values (in blocks of 128 bits):", sum(FPI_L2['LENGTH']))

