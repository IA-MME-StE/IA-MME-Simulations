# IA-MME-Simulations

This repository contains all the code, data and results used in our simulations for supporting SSE and SQL data types using IA-MME primitives. Simulation results are reported in our paper. 

## Simulating SE1 and SE2 on ePrint Datasets 

- ePrint datasets can be scraped using "ePrint_scrape.py" (change the year in line 24 accordingly)
- A folder pdfs-<year> will be generated with all the ePrint PDFs downloaded in it. 
- An eprint_<year>.csv file with all necessary information extracted will also be generated.
- Copies of the 2020 and 2021 CSV files are in "Data" (with additional information about PDF lengths) for reference. 
- Simulations can be run using "ePrint_LMM.py"

## Simulating FP2, PP2 and PP3 on TPC-H Datasets

- TPC-H datasets are generated using the tpc-h-tool dbgen downloaded from https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp, with scale factors 1 and 0.01. 
- Datasets are converted to CSV using "tpch_converter.py"
- Schema determining the relations and allowed joins can be found in https://www.tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.1.pdf. 
- Our datasets can be found in "Data"
- Some summary information on the datasets can be found in "Results_for_TPC-H.xlsx"
- Simulations can be run using "TPCH_LMM.py"