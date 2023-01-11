import sys
import os
import pandas as pd

argv = sys.argv

if len(argv) != 2:
    print("Use 'python classifying_joins.py <DIR>', where DIR is the name of the directory containing the database.")
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


# To check the relationship of the join
def get_relation(df1, df2, column):        
    max1 = df1[column].value_counts().max()
    max2 = df2[column].value_counts().max()

    if max1 == 1:
        if max2 == 1:
            return 'one-to-one'
        else:
            return 'one-to-many'
    else:
        if max2 == 1:
            return 'one-to-many'
        else:
            return 'many-to-many'


# To check the completeness of the join
def completeness(df1, df2, column): 
    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())

    if key1 == key2:
        return 'complete'
    elif(key1.issubset(key2)):
        return 'partially complete in Table 1'
    elif(key2.issubset(key1)):
        return 'partially complete in Table 2'
    else:
        return 'incomplete'


# To compute # rows in input tables
def num_rows(df, column): 

    sum = df[column].value_counts().sum()
    
    return sum


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


# To compute % of rows from input tables to join output
def percent_rows(df1, df2, column): 
    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())
    
    overlap = key1.intersection(key2)
    table1 = 0
    table2 = 0
    for i in overlap:
        table1 = table1 + dict1[i]
        table2 = table2 + dict2[i]
    
    percentage1 = table1 / df1[column].value_counts().sum() *100
    percentage2 = table2 / df2[column].value_counts().sum() * 100

    return percentage1, percentage2


# To compute % of distinct values from input tables to join output
def percent_distinct(df1, df2, column): 
    dict1 = dict(df1[column].value_counts())
    dict2 = dict(df2[column].value_counts())

    key1 = set(dict1.keys())
    key2 = set(dict2.keys())
    
    overlap = key1.intersection(key2)
        
    percentage1 = len(overlap) / len(key1) *100
    percentage2 = len(overlap) / len(key2) *100

    return percentage1, percentage2


# Printing of results for Relation and Completeness
print("\nResults for Relation and Completeness:")

print("\nNo. Table1 \tTable2 \t\tJoin \t\t Relation \t Completeness \n")

print(" 1) nation \tregion \t\tREGIONKEY \t", get_relation(nation, region, 'REGIONKEY')," \t", completeness(nation, region, 'REGIONKEY'))

print(" 2) supplier \tnation \t\tNATIONKEY \t", get_relation(supplier, nation, 'NATIONKEY')," \t", completeness(supplier, nation, 'NATIONKEY'))

print(" 3) customer \tnation \t\tNATIONKEY \t", get_relation(customer,  nation, 'NATIONKEY')," \t", completeness(customer,  nation, 'NATIONKEY'))

print(" 4) customer \tsupplier \tNATIONKEY \t", get_relation(customer, supplier, 'NATIONKEY')," \t", completeness(customer, supplier, 'NATIONKEY'))

print(" 5) partsupp \tsupplier \tSUPPKEY \t", get_relation(partsupp, supplier, 'SUPPKEY')," \t", completeness(partsupp, supplier, 'SUPPKEY'))

print(" 6) partsupp \tpart \t\tPARTKEY \t", get_relation(partsupp, part, 'PARTKEY')," \t", completeness(partsupp, part, 'PARTKEY'))

print(" 7) lineitem \tpartsupp \tPARTKEY \t", get_relation(lineitem, partsupp, 'PARTKEY')," \t", completeness(lineitem, partsupp, 'PARTKEY'))

print(" 8) lineitem \tpartsupp \tSUPPKEY \t", get_relation(lineitem, partsupp, 'SUPPKEY')," \t", completeness(lineitem, partsupp, 'SUPPKEY'))

print(" 9) lineitem \torders \t\tORDERKEY \t", get_relation(lineitem, orders, 'ORDERKEY')," \t", completeness(lineitem, orders, 'ORDERKEY'))

print("10) orders \tcustomer \tCUSTKEY \t", get_relation(orders, customer, 'CUSTKEY')," \t", completeness(orders, customer, 'CUSTKEY'),"\n")


# Printing of results for Number of Rows
print("\nResults for Number of Rows:")

print("\nNo. Table1 \t(# rows) \tTable2 \t\t(# rows) \tJoin \t\t(# rows) \n")

print(" 1) nation \t",num_rows(nation,'REGIONKEY'), "\t\tregion \t\t",num_rows(region,'REGIONKEY'), "\t\tREGIONKEY \t", num_join_rows(nation, region, 'REGIONKEY'))

print(" 2) supplier \t",num_rows(supplier,'NATIONKEY'), "\t\tnation \t\t",num_rows(nation,'NATIONKEY'), "\t\tNATIONKEY \t", num_join_rows(supplier, nation, 'NATIONKEY'))

print(" 3) customer \t",num_rows(customer,'NATIONKEY'), "\tnation \t\t",num_rows(nation,'NATIONKEY'), "\t\tNATIONKEY \t", num_join_rows(customer, nation, 'NATIONKEY'))

print(" 4) customer \t",num_rows(customer,'NATIONKEY'), "\tsupplier \t",num_rows(supplier,'NATIONKEY'), "\t\tNATIONKEY \t", num_join_rows(customer, supplier, 'NATIONKEY'))

print(" 5) partsupp \t",num_rows(partsupp,'SUPPKEY'), "\tsupplier \t",num_rows(supplier,'SUPPKEY'), "\t\tSUPPKEY \t", num_join_rows(partsupp, supplier, 'SUPPKEY'))

print(" 6) partsupp \t",num_rows(partsupp,'PARTKEY'), "\tpart \t\t",num_rows(part,'PARTKEY'), "\tPARTKEY \t", num_join_rows(partsupp, part, 'PARTKEY'))

print(" 7) lineitem \t",num_rows(lineitem,'PARTKEY'), "\tpartsupp \t",num_rows(partsupp,'PARTKEY'), "\tPARTKEY \t", num_join_rows(lineitem, partsupp, 'PARTKEY'))

print(" 8) lineitem \t",num_rows(lineitem,'SUPPKEY'), "\tpartsupp \t",num_rows(partsupp,'SUPPKEY'), "\tSUPPKEY \t", num_join_rows(lineitem, partsupp, 'SUPPKEY'))

print(" 9) lineitem \t",num_rows(lineitem,'ORDERKEY'), "\torders \t\t",num_rows(orders,'ORDERKEY'), "\tORDERKEY \t", num_join_rows(lineitem, orders, 'ORDERKEY'))

print("10) orders \t",num_rows(orders,'CUSTKEY'), "\tcustomer \t",num_rows(customer,'CUSTKEY'), "\tCUSTKEY \t", num_join_rows(orders, customer, 'CUSTKEY'), "\n")


# Printing of results for Percentages of Rows
print("\nResults for Percentages of Rows:")

print("\nNo. Table1 \tTable2 \t\tJoin \t\t % of Rows for Tables 1 and 2 \n")

print(" 1) nation \tregion \t\tREGIONKEY \t", percent_rows(nation, region, 'REGIONKEY'))

print(" 2) supplier \tnation \t\tNATIONKEY \t", percent_rows(supplier, nation, 'NATIONKEY'))

print(" 3) customer \tnation \t\tNATIONKEY \t", percent_rows(customer,  nation, 'NATIONKEY'))

print(" 4) customer \tsupplier \tNATIONKEY \t", percent_rows(customer, supplier, 'NATIONKEY'))

print(" 5) partsupp \tsupplier \tSUPPKEY \t", percent_rows(partsupp, supplier, 'SUPPKEY'))

print(" 6) partsupp \tpart \t\tPARTKEY \t", percent_rows(partsupp, part, 'PARTKEY'))

print(" 7) lineitem \tpartsupp \tPARTKEY \t", percent_rows(lineitem, partsupp, 'PARTKEY'))

print(" 8) lineitem \tpartsupp \tSUPPKEY \t", percent_rows(lineitem, partsupp, 'SUPPKEY'))

print(" 9) lineitem \torders \t\tORDERKEY \t", percent_rows(lineitem, orders, 'ORDERKEY'))

print("10) orders \tcustomer \tCUSTKEY \t", percent_rows(orders, customer, 'CUSTKEY'),"\n")


# Printing of results for Percentages of Distinct Values
print("\nResults for Percentages of Distinct Values:")

print("\nNo. Table1 \tTable2 \t\tJoin \t\t % of Distinct Values for Tables 1 and 2 \n")

print(" 1) nation \tregion \t\tREGIONKEY \t", percent_distinct(nation, region, 'REGIONKEY'))

print(" 2) supplier \tnation \t\tNATIONKEY \t", percent_distinct(supplier, nation, 'NATIONKEY'))

print(" 3) customer \tnation \t\tNATIONKEY \t", percent_distinct(customer,  nation, 'NATIONKEY'))

print(" 4) customer \tsupplier \tNATIONKEY \t", percent_distinct(customer, supplier, 'NATIONKEY'))

print(" 5) partsupp \tsupplier \tSUPPKEY \t", percent_distinct(partsupp, supplier, 'SUPPKEY'))

print(" 6) partsupp \tpart \t\tPARTKEY \t", percent_distinct(partsupp, part, 'PARTKEY'))

print(" 7) lineitem \tpartsupp \tPARTKEY \t", percent_distinct(lineitem, partsupp, 'PARTKEY'))

print(" 8) lineitem \tpartsupp \tSUPPKEY \t", percent_distinct(lineitem, partsupp, 'SUPPKEY'))

print(" 9) lineitem \torders \t\tORDERKEY \t", percent_distinct(lineitem, orders, 'ORDERKEY'))

print("10) orders \tcustomer \tCUSTKEY \t", percent_distinct(orders, customer, 'CUSTKEY'),"\n")
