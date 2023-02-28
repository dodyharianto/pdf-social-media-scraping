import pandas as pd
import numpy as np
import os
from PyPDF2 import PdfReader, PdfFileReader

def scrape_pdf(filename):
    reader = PdfReader(filename) 
    number_of_pages = len(reader.pages)

    # list of all text from all pages
    text_list = []
    for i in range(number_of_pages):
        page = reader.pages[i]

        # all text from one page
        text = page.extract_text()
        # print(text)

        text_list.append(text)
    return text_list

# main directory for all PDF files
pdf_files_directory = 'PDF Files'

# all scrapped journal names
journal_names = os.listdir(pdf_files_directory)

filenames_list = []
journal_names_list = []
text_lists = []

for journal_name in journal_names:
    filenames = os.listdir(os.path.join(pdf_files_directory, journal_name))
    for filename in filenames:
        journal_path = os.path.join(pdf_files_directory, journal_name)
        
        filenames_list.append(filename)
        journal_names_list.append(journal_name)
        
        text_list = scrape_pdf(os.path.join(journal_path, filename))
        text_lists.append(text_list)

# convert to dataframe
df = pd.DataFrame({'File Name': filenames_list,
                   'Journal Name': journal_names_list,
                   'Text List': text_lists})

print(df.head())
# df.to_csv('pdf-scraping.csv')