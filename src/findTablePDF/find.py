import camelot

import urllib
#from urllib.request import urlopen

#import fiona

#PDF file
file = "test.pdf"

#Read the pdf file using the camelot library
tables = camelot.read_pdf(file)

#Print statements
print("Total Tables Extracted:", tables.n)

print(tables[0].df)

#Convert the table to a csv file
tables[0].to_csv("test.csv")

#Convert the table to a excel file
tables[0].to_excel("test2.xlsx")