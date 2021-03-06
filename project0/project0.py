# Author: Siddhardha Maguluri <Siddhardha.Maguluri@ou.edu>.

"""This module provides the functions that we can use to extract 
the content from a incident PDF from Norman Police Department, 
create a database and the populate the database with the extracted query, 
and Show the output of database query.
"""
import os
import sqlite3
from  sqlite3 import Error
import re
import tempfile
from typing import List

import urllib.request
import PyPDF2


def getindexesofdatecolumn(page: List[str]) -> List[int]:
    """
    get the index of date time column in a page, as we know every row in page start with date and time.

    Parameters
    ----------
    page: List[str]
        Content of one pdf page as list of strings.
    
    Return
    ------
    date_time_columns_indexes: List[int]
        a list of indexes of date time column data in the given list of strings.
    
    """
    date_time_column_indexes = []
    for column_index in range(0, len(page)):
        if re.match("[0-9]+\/[0-9]+\/[0-9]{4} [0-9]+:[0-9]+", page[column_index]):
            date_time_column_indexes.append(column_index)

    return date_time_column_indexes


def fetchincidents(url: str) -> bytes:
    """
    Takes an incident page ```URL```, reads the incidents data from the url using urlib and return raw data(i.e; data in bytes format)

    Paramaters
    ----------
    url : str
        An url of the incidents page from Norman Police Department site.

    Returns
    -------
    data: bytes
        returns a data in bytes format
    """
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"

    raw_data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()

    return raw_data


def extractincidents(incidents_data: bytes) -> List[list[str]]:
    """
    Takes the incident data( which is data in byte format) as input and creates a temporary pdf file and extract the contents of file as list of lists. 

    Paramaters
    ----------
    incidents_data : bytes
        data of a pdf file in bytes format.

    Return
    ------
    rows: List(list)
        all rows in the pdf file as a list
 
    """
    fp = tempfile.TemporaryFile()
    fp.write(incidents_data)

    pdfreader = PyPDF2.PdfFileReader(fp)
    totalnoofpages = pdfreader.getNumPages()

    pdf_data = []  # list with pdf contents after removing unwanted content of each page.

    # extractText of PyPDF2 will returns the page content as one long string. using split with '\n' as delimiter gives
    # us a list of strings(page content). in this case page 0 has some extra values at the start and end, 
    # while last page will have an extra value at the end. all these extra values need to be removed. 
    # Hence, first page and last page is handled seperately.  
    for page_number in range(0, totalnoofpages):
        cleaned_page_data = []
        if page_number == 0:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(5, len(page_data) - 3):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)
        elif page_number == totalnoofpages - 1:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(0, len(page_data) - 2):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)
        else:
            page_data = pdfreader.getPage(page_number).extractText().split("\n")
            for i in range(0, len(page_data) - 1):
                cleaned_page_data.append(page_data[i])
            pdf_data.append(cleaned_page_data)

    cleaned_pdf_data = [] # list of page contents after handling the rows with missing values and rows with address column in 2 lines 

    for index, page in enumerate(pdf_data):
        date_time_indexes = getindexesofdatecolumn(page)
        cleaned_data_for_each_page = []
        for i in range(0, len(date_time_indexes)):
            start = date_time_indexes[i]
            if i == len(date_time_indexes) - 1:
                end = len(page)
                if end - start < 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start + 1)])
                    cleaned_data_for_each_page.append("")
                    cleaned_data_for_each_page.append("")
                    cleaned_data_for_each_page.append(page[(start + 2)])
                else:
                    for j in range(start, len(page)):
                        cleaned_data_for_each_page.append(page[j])
            else:
                end = date_time_indexes[i + 1]
                if end - start < 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start + 1)])
                    cleaned_data_for_each_page.append("")
                    cleaned_data_for_each_page.append("")
                    cleaned_data_for_each_page.append(page[(start + 2)])
                elif end - start > 5:
                    cleaned_data_for_each_page.append(page[start])
                    cleaned_data_for_each_page.append(page[(start + 1)])
                    clean_address = page[(start + 2)] + page[(start + 3)]
                    cleaned_data_for_each_page.append(clean_address)
                    cleaned_data_for_each_page.append(page[(start + 4)])
                    cleaned_data_for_each_page.append(page[(start + 5)])
                else:
                    for j in range(start, end):
                        cleaned_data_for_each_page.append(page[j])
        cleaned_pdf_data.append(cleaned_data_for_each_page)

    all_rows = []

    # As we know every row or record in a pdf should 5 column values, 
    # i am taking 5 elements from a list and creating a row and 
    # finally adding it to all_rows list. So, all_rows is list of lists, where each list contains column values of each row.
    for page_number in range(0, totalnoofpages):
        for i in range(0, len(cleaned_pdf_data[page_number]), 5):
            row = []
            colum1 = cleaned_pdf_data[page_number][i]
            column2 = cleaned_pdf_data[page_number][i + 1]
            column3 = cleaned_pdf_data[page_number][i + 2]
            column4 = cleaned_pdf_data[page_number][i + 3]
            column5 = cleaned_pdf_data[page_number][i + 4]
            row.append(colum1)
            row.append(column2)
            row.append(column3)
            row.append(column4)
            row.append(column5)
            all_rows.append(row)

    return all_rows


def createdb() -> sqlite3.Connection:
    """ 
    creates an SQLite Database with a table named ```incidents``` 
    
    Parameters
    ----------
    None

    Return
    ------
    a sqlite3 database connection object.
    
    """
    try:
        if os.path.exists("normanpd.db"):
            os.remove("normanpd.db")
        fp = open("normanpd.db", "x")
        fp.close()
        connnection = sqlite3.connect("normanpd.db")
        create_incidents_table = """ CREATE TABLE incidents (
                                incident_time TEXT,
                                incident_number TEXT,
                                incident_location TEXT,
                                nature TEXT,
                                incident_ori TEXT
                                );
                            """
        cursor = connnection.cursor()
        cursor.execute(create_incidents_table)
        return connnection
    except Error as e:
        print(e)


def populatedb(db: sqlite3.Connection, incidents: List[list[str]]) -> None :
    """
    Populates the database with the given incidents data

    Parameters
    ----------
    db: sqlite.Connection
        a sqlite3 database connection object

    incidents: List[list[str]]
        list of rows in a pdf file.

    Return
    ------
    None

    """
    
    cursor = db.cursor()
    insert_query = "INSERT INTO incidents VALUES (?, ?, ?, ?, ?)"

    for row in incidents:
        cursor.execute(insert_query, (row[0], row[1], row[2], row[3], row[4]))

    db.commit()


def status(db):
    """
    Prints the query result to the standard output.

    Parameters
    ----------
    db: sqlite.Connection
        a sqlite3 database connection object
    
    Return
    ------
    None
    """
    cursor = db.cursor()

    # SQL query to retrieve names of unique incidents and their count
    select_unique_incident_natures = "SELECT nature, count(nature) as no_of_times from incidents group by nature order by no_of_times desc, nature"
    query_result = cursor.execute(select_unique_incident_natures)

    # Output the query result
    for row in query_result:
        print(f"{row[0]}|{row[1]}")

    db.close()
