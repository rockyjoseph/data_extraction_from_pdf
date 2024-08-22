# IMporting Libraries
import os
import PyPDF2
import re
import pandas as pd
import numpy as np

# REading the file
reader = PyPDF2.PdfReader("sample_problem.pdf")

# Getting the content in the text file
for pg in range(0, 1):
    page = reader.pages[pg]
    try:
        file = open('pdf_content.txt','a')
    except FileNotFoundError:
        file = open('pdf_content.txt','w')
        
    file.write(page.extract_text())
    file.close()
    
# Opening files for extracting the content and writing on it.
out_file = open('pdf_line_content.txt','w')
new_file = open('pdf_content.txt','rb')

s = new_file.read()
strn = re.split(' No', str(s))
out_file.write('\n'.join(strn))

new_file.close()
out_file.close()

# Reading the content
out_files = open('pdf_line_content.txt','r')

row = []

# Making a loop for getting the data from the pdf
for eachline in out_files.readlines():
    name = re.findall(r'.\dName\s:\s(.*?)\s', eachline)
    relative = re.findall(r'\sName\s:\s(.*?)\s\s\d\d', eachline)
    gender = re.findall(r'.Gender\s:\s(.*?)Age', eachline)
    age = re.findall(r'[A-Z]*\s\s(\d\d)\s.\w', eachline)
    h_no = re.findall(r'\s:\s(.*?)Gender', eachline)

    # Appending the details in a row.
    row.append((name, relative, gender, age, h_no))
    
# Closing the file
out_files.close()

# Removing the text files
os.remove('pdf_content.txt')
os.remove('pdf_line_content.txt')

# Creating a Dataframe to store it in excel.
df = pd.DataFrame(row, columns = ['Name', 'Relative Name','Gender','Age','House No.'])

for col in df.columns:
    df[col] = df[col].apply(lambda i: ''.join(i))
    
df.replace('', np.nan, inplace=True)
df.dropna(how='all', inplace=True)

writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer, 'Content')

writer.close()