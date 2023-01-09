import sys
import os
import pandas as pd

argv = sys.argv

if len(argv) != 2:
    print("Use 'python ePrint_LMM.py <filename>', where <filename> is the name of the .csv file.")
    exit()

filename = os.fsdecode(argv[1])

# Reading csv into dataframe
eprint = pd.read_csv(filename)

data = eprint[['NAME', 'KEYWORD(S)', 'SIZE(blocks of 128 bits)']].copy()

all_keywords = []
number = []
for string in data['KEYWORD(S)']:
    if string[0] == '[':
        new_string = string[2:-2]
        keywords = list(new_string.split("', '"))
        number.append(len(keywords))
        for item in keywords:
            all_keywords.append(item)
    else:
        all_keywords.append(string)
        number.append(1)

# To remove duplicated keywords
collated_keywords = list(set(all_keywords))

data['NUM OF KEYWORDS'] = number
data['TOTAL SIZE OF DOCS STORED'] = data['SIZE(blocks of 128 bits)']*data['NUM OF KEYWORDS']

print("\nComputing the sizes of the 2-layer LMM indexes for "+filename+":\n")
print("LMM Level 1: \n")
print("Total number of labels:", len(data))
print("Total size of documents (in blocks of 128 bits):", sum(data['SIZE(blocks of 128 bits)']))
print("\nLMM Level 2: \n")
print("Total number of keywords:", len(collated_keywords))
print("Total number of doc_id tokens (in blocks of 128 bits):", len(all_keywords))
print("\n\nComputing the size of the 1-layer LMM index for "+filename+":\n")
print("Total number of keywords:", len(collated_keywords))
print("Total size of documents stored (in blocks of 128 bits):", sum(data['TOTAL SIZE OF DOCS STORED']))