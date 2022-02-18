import csv
import tempfile
from urllib.request import urlopen
import PyPDF2
import sqlite3
from sqlite3 import Error

def fetchincidents(url):
    """
    Takes a URL string and reads the data from the url.
    """
    raw_data = urlopen(url).read()
    # print(raw_data)
    return raw_data
    # file = open('/tmp/incident_summary'+'.pdf', 'wb')
    # file.write(raw_data)
    # file.close()
    # # pdf_data = open(raw_pdf_data, 'rb')

def extractincidents(incidents_data):
    """
    Takes the incident data as input and creates a temporary pdf file and extract the contents of pdf file.
    """
    fp = tempfile.TemporaryFile()
    fp.write(incidents_data)

    pdfreader = PyPDF2.PdfFileReader(fp)
    totalnoofpages = pdfreader.getNumPages()

    contents = pdfreader.getPage(0).extractText().split("\n")
    print(contents)


    # # pdf_data is a list which contains individual list for each page.
    # pdf_data = []
    #
    # # pdf_data_page0 is list of strings extracted from a pdf page 0.
    # # first page in a pdf file is a special one, The first 5 values are headers
    # # and last 3 values in this list not required.
    # # hence, we need to remove them from list
    # pdf_data_page1 = pdfreader.getPage(0).extractText().split("\n")
    # pdf_data_page1_cleaned = []
    # for i in range(5, len(pdf_data_page1)-3):
    #     pdf_data_page1_cleaned.append(pdf_data_page1[i])
    #
    # pdf_data.append(pdf_data_page1_cleaned)
    #
    # # for remaining pages the last value in the list is empty string. so, we need to remove it.
    # for pagenum in range(1, totalnoofpages):
    #     temp_page_data = pdfreader.getPage(pagenum).extractText().split("\n")
    #     cleaned_data = []
    #     for i in range(0, len(temp_page_data)-1):
    #         cleaned_data.append(temp_page_data[i])
    #     pdf_data.append(cleaned_data)
    #
    # rows = []

    return ''
