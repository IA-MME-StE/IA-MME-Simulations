#=============================================================#
# Written by  : Ee Yen Ling Eileen                            #
# Last updated: 01/12/2022                                    #
# Purpose     : To web scrape Cryptology ePrint Archive for   #
#               PDF papers and extract information about them #
#=============================================================#

from bs4 import BeautifulSoup
import requests
import re
import os
import wget
import pandas as pd
import math
import string
from pathlib import Path
from urllib.request import urlopen
from urllib.request import Request
from PyPDF2 import PdfFileReader
    
#url = input(“Enter a website to extract the links from: “)

URL = "https://eprint.iacr.org"
year = '2021'

DIR_DOWNLOAD = "pdfs-"+year
page = requests.get(URL+"/"+year+"/")

try:
    os.mkdir(DIR_DOWNLOAD)
except OSError:
    pass

data = {
    'NAME': [],
    'YEAR': [],
    'INDEX': [],
    'AUTHOR(S)': [],
    'CATEGORY': [],
    'KEYWORD(S)': [],
    'PUBLICATION': [],
    'LENGTH': [],
    'SIZE(KB)' : [],
    'SIZE(blocks of 128 bits)' : [],
}

def data_extraction(URL_NAME):
    NAME = URL_NAME[1:].split('/')
    PDF_PATH = Path(DIR_DOWNLOAD+"/"+NAME[0]+"-"+NAME[1])
            
    ## Downloads the pdf if it is not already downloaded
    if PDF_PATH.is_file():
        pass
    else:
        FULLURL = URL + URL_NAME
        wget.download(FULLURL,out = DIR_DOWNLOAD)
        
    pdf_file = open(PDF_PATH, "rb")
    pdf_reader = PdfFileReader(pdf_file, strict=False)
    pdf_pages = pdf_reader.numPages
    file_stats = os.stat(PDF_PATH)
           
    name = NAME[0]+'-'+NAME[1][:-4]
    data['YEAR'].append(NAME[0])
    data['INDEX'].append(NAME[1][:-4])
    data['NAME'].append(name)
    data['LENGTH'].append(pdf_pages)
    data['SIZE(KB)'].append(math.ceil(file_stats.st_size/1024))
    data['SIZE(blocks of 128 bits)'].append(math.ceil(file_stats.st_size/16))
        
    ## Goes to the individual page to extract more info
    page2 = requests.get(URL+URL_NAME[:-4])
    soup2 = BeautifulSoup(page2.text, features="html5lib")
            
    AUTHORS = []
    KEYWORDS = []

    ## Data extraction

    print("\nScraping",data['NAME'][-1], "...")
    
    for tag in soup2.find_all("meta"):
        if tag.get("name", None) == "citation_author":
            AUTHORS.append(tag.get("content", None))
    data['AUTHOR(S)'].append(AUTHORS)
        
    for item in soup2.find_all("div", id="metadata"):
        search_cat = item.find('dt',text=re.compile("Category"))
        if search_cat == None:
            data['CATEGORY'].append('Uncategorized')
        else:
            data['CATEGORY'].append(search_cat.find_next('dd').text.strip())
            
    for item in soup2.find_all("div", id="metadata"):
        search_kw = item.find('dt',text=re.compile("Keywords"))
        if search_kw == None:
            # To change all letters to CAPs, remove spaces and punctuations
            data['KEYWORD(S)'].append(data['CATEGORY'][-1].translate(str.maketrans('', '', string.punctuation)).replace(' ', '').upper())
        else:
            next_dd = search_kw.find_next('dd')
            a_tags = next_dd.find_all('a')
            for tag in a_tags:
                # To change all letters to CAPs, remove spaces and punctuations
                KEYWORDS.append(tag.text.strip().translate(str.maketrans('', '', string.punctuation)).replace(' ', '').upper())
                KEYWORDS = list(dict.fromkeys(KEYWORDS))
            data['KEYWORD(S)'].append(KEYWORDS)
            
    for item in soup2.find_all("div", id="metadata"):
        search_pub = item.find('dt',text=re.compile("Publication info"))
        if search_pub == None:
            break
        data['PUBLICATION'].append(search_pub.find_next('dd').text.strip())
        

def parse_page(page):
    soup = BeautifulSoup(page.text, features="html5lib")
    
    flag = 1
    
    while (flag):
        for i, link in enumerate(soup.find_all('a')):
            URL_NAME = link.get('href')
            if URL_NAME == None:
                continue
            elif URL_NAME.endswith('.pdf'):
                data_extraction(URL_NAME)
            elif link.text.strip() == 'Next »':
                next_page = requests.get(URL+URL_NAME)
                parse_page(next_page)    
            else:
                flag = 0


parse_page(page)

filename = "eprint_"+year+".csv"
df = pd.DataFrame(data)
df.to_csv(filename, encoding = 'utf-8')
