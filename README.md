@@ -1 +1,20 @@
# IA-MME-Simulations
# IA-MME-Simulations

This repository contains all the code, data and results used in our simulations for supporting SSE and SQL data types using IA-MME primitives. Simulation results are reported in our paper. 

## Simulating SE1 and SE2 on ePrint Datasets 

- ePrint datasets can be scraped using "ePrint_scrape.py" (change the year in line 24 accordingly)
- Type the command "python ePrint_scrape.py" to run the script. 
- A folder pdfs-<year> will be generated with all the ePrint PDFs downloaded in it. 
- An eprint_<year>.csv file with all necessary information extracted will also be generated.
- If the script hangs after a while, you can check which page on ePrint it hangs on, and change line 27 of ePrint_scrape.py to start from that page. 
- Do note that the eprint_<year>.csv file generated in this case would not be complete. 
- After all PDFs are downloaded, change line 27 back to the original command and run again to get the complete eprint_<year>.csv.
- Copies of the 2020 and 2021 CSV files are in "Data" (with additional information about PDF lengths) for reference. 
- Simulations can be run using "ePrint_LMM.py" using the command "python ePrint_LMM.py <filename>", where <filename> is the name of the .csv file.

## Simulating FP2, PP2 and PP3 on TPC-H Datasets

- TPC-H datasets are generated using the tpc-h-tool dbgen downloaded from https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp, with scale factors 1 and 0.01. 
- Add the conversion program "tpch_converter.py" to the dbgen folder and use the command "python tpch_converter.py <DIR>", where <DIR> is the name of the directory/folder containing the database, to convert the datasets to CSV.
- Schema determining the relations and allowed joins can be found in https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.1.pdf. 
- Add the classification program "classifying_joins.py" to the dbgen folder and use the command “python classifying_joins.py <DIR>”, where DIR is the name of the directory/folder containing the database, to classify the join output.
- Our datasets can be found in "Data"
- Some summary information on the datasets can be found in "Results_for_TPC-H.xlsx"
- Simulations can be run using "TPCH_LMM.py" by the command "python TPCH_LMM.py <DIR>", where <DIR> is the name of the directory/folder containing the CSV