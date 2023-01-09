# Converts commas to ;, and | to commas.

import sys
import os

argv = sys.argv

if len(argv) != 2:
    print("Use 'python tpch_converter.py <DIR>', where DIR is the name of the directory containing the database.")
    exit()

directory = os.fsdecode(argv[1])

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    name = os.path.splitext(filename)[0]
    new_file = name+".csv"
    ou = open(directory+"/"+new_file, "w")

    openfile = open(directory+"/"+filename)

    # Prepending table labels
    if filename == "customer.tbl":
        ou.write("CUSTKEY,NAME,ADDRESS,NATIONKEY,PHONE,ACCTBAL,MKTSEGMENT,COMMENT,NA\n")
    elif filename == "lineitem.tbl":
        ou.write("ORDERKEY,PARTKEY,SUPPKEY,LINENUMBER,QUANTITY,EXTENDEDPRICE,DISCOUNT,TAX,RETURNFLAG,LINESTATUS,SHIPDATE,COMMITDATE,RECEIPTDATE,SHIPINSTRUCT,SHIPMODE,COMMENT,NA\n")
    elif filename == "nation.tbl":
        ou.write("NATIONKEY,NAME,REGIONKEY,COMMENT,NA\n")
    elif filename == "orders.tbl":
        ou.write("ORDERKEY,CUSTKEY,ORDERSTATUS,TOTALPRICE,ORDERDATE,ORDER-PRIORITY,CLERK,SHIP-PRIORITY,COMMENT,NA\n")
    elif filename == "part.tbl":
        ou.write("PARTKEY,NAME,MFGR,BRAND,TYPE,SIZE,CONTAINER,RETAILPRICE,COMMENT,NA\n")
    elif filename == "partsupp.tbl":
        ou.write("PARTKEY,SUPPKEY,AVAILQTY,SUPPLYCOST,COMMENT,NA\n")
    elif filename == "region.tbl":
        ou.write("REGIONKEY,NAME,COMMENT,NA\n")    
    elif filename == "supplier.tbl":
        ou.write("SUPPKEY,NAME,ADDRESS,NATIONKEY,PHONE,ACCTBAL,COMMENT,NA\n")
    else:
        pass

    for line in openfile:
        ou.write(line.replace(",", ";").replace("|", ","))
    print(openfile)
    openfile.close()

ou.close()


