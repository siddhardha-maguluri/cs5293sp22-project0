import tempfile
from urllib.request import urlopen
import PyPDF2
import sqlite3
import os
import re
from sqlite3 import Error

# get the index of date time column in a page, as we know every row in page start with date and time.
def getindexesofdatecolumn(page):
    date_time_column_indexes = []
    for column_index in range(0,len(page)):
        if re.match('[0-9]+\/[0-9]+\/[0-9]{4} [0-9]+:[0-9]+', page[column_index]):
            date_time_column_indexes.append(column_index)
    
    return date_time_column_indexes

def fetchincidents(url):
    """
    Takes a URL string, reads the incidents data from the url and return raw data(i.e; data in bytes format)
    """
    raw_data = urlopen(url).read()
    return raw_data

def extractincidents(incidents_data):
    """
    Takes the incident data as input and creates a temporary file and extract the contents of file as rows.
    """
    fp = tempfile.TemporaryFile()
    fp.write(incidents_data)

    pdfreader = PyPDF2.PdfFileReader(fp)
    totalnoofpages = pdfreader.getNumPages()

    pdf_data = []

    for page_number in range(0,totalnoofpages):
        cleaned_page_data = []
        if page_number == 0:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(5, len(page_data)-3):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)
        elif page_number == totalnoofpages -1:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(5, len(page_data)-2):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)
        else:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(0,len(page_data)-1):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)
    
    cleaned_pdf_data = []

    for index, page in enumerate(pdf_data):
        date_time_indexes = getindexesofdatecolumn(page)
        cleaned_data_for_each_page = []
        for i in range(0,len(date_time_indexes)):
            # record = ''
            start = date_time_indexes[i]
            if i == len(date_time_indexes)-1:
                end = len(page)
                if end - start < 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start+1)])
                    cleaned_data_for_each_page.append('')
                    cleaned_data_for_each_page.append('')
                    cleaned_data_for_each_page.append(page[(start+2)])
                else:
                    for j in range(start,len(page)):
                        cleaned_data_for_each_page.append(page[j])
            else:
                end = date_time_indexes[i+1]
                if end - start < 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start+1)])
                    cleaned_data_for_each_page.append('')
                    cleaned_data_for_each_page.append('')
                    cleaned_data_for_each_page.append(page[(start+2)])
                    # record = page[start] + ' ' +page[(start+1)] + ' ' + 'null' + ' '+ 'null' + ' ' +  page[(start+2)]
                elif end - start > 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start+1)])
                    clean_address = page[(start+2)] + page[(start+3)]
                    cleaned_data_for_each_page.append(clean_address)
                    cleaned_data_for_each_page.append(page[(start+4)])
                    cleaned_data_for_each_page.append(page[(start+5)])
                    # record = page[start] + ' ' + page[(start+1)] + ' '+ page[(start+2)]
                else: 
                    for j in range(start,end):
                        cleaned_data_for_each_page.append(page[j])
        cleaned_pdf_data.append(cleaned_data_for_each_page)
    
    all_rows = []

    # creating a row and adding it to list
    for page_number in range(0,totalnoofpages):
        for i in range(0, len(cleaned_pdf_data[page_number]),5):
            row = []
            colum1 = cleaned_pdf_data[page_number][i]
            column2 = cleaned_pdf_data[page_number][i+1]
            column3 = cleaned_pdf_data[page_number][i+2]
            column4 = cleaned_pdf_data[page_number][i+3]
            column5 = cleaned_pdf_data[page_number][i+4]
            row.append(colum1)
            row.append(column2)
            row.append(column3)
            row.append(column4) 
            row.append(column5)
            all_rows.append(row)

    # print(all_rows)

    return all_rows
    
def createdb():
    try:
        if os.path.exists('normanpd.db'):
            os.remove('normanpd.db')
        fp = open('normanpd.db','x')
        fp.close()
        connnection = sqlite3.connect('normanpd.db')
        # print("---database created successfully---", connnection)
        return connnection
    except Error as e:
        print(e)      

def populatedb(db, incidents):
    cursor = db.cursor()
    create_incidents_table = ''' CREATE TABLE incidents (
                                incident_time TEXT,
                                incident_number TEXT,
                                incident_location TEXT,
                                nature TEXT,
                                incident_ori TEXT
                                );
                            '''
    cursor.execute(create_incidents_table)

    insert_query = """ INSERT INTO incidents VALUES (?, ?, ?, ?, ?);"""
    
    for row in incidents:
        cursor.execute(insert_query, (row[0],row[1],row[2],row[3],row[4]))
    
    # print('inserted all pdf data into database')
    db.commit()

def status(db):
    cursor = db.cursor()

    # SQL query to retrieve names of unique incidents and their count
    select_unique_incident_natures = "SELECT nature, count(nature) as no_of_times from incidents where nature not like '' group by nature"
    query_result = cursor.execute(select_unique_incident_natures)

    # Output the query result
    for row in query_result:
        print(f'{row[0]}|{row[1]}')
    
    db.close()
