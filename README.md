# cs5293sp22-project0
Contains code for the projects that are done as part of text analytics class.  

## Name: Siddhardha Maguluri  

## How to run the project  
1. Clone the code with following the command ```git clone https://github.com/siddhardha-maguluri/cs5293sp22-project0.git```  
2. Open terminal in project root directory. make sure you have ```pipenv``` installed in the system. Run the following command  
   ```pipenv install``` 
3. The above command creates a virtual environment in the project folder, install all the packages mentioned in ```requirements.txt```  
   and track the package version changes in a Pipfile. 
4. finally, run the code using following command  
   `pipenv run python project0/main.py --incidents <incidentpageurl>`

## External libraries used and their installation procedure and usage
1. ```PyPDF2``` - This package is used to extract the data from a PDF file.  
   Installation : To install the package run ```pipenv install PyPDF2```

   usage:  

   PdfFileReader() - to create an pdf reader object.  
   getNumPages()   - gives the count of total number of pages in a pdf.  
   getPage()       - to access a individual page. will send page number as a parameter.  
   extractText()   - to extract the content of a page.  
   
2. ```pytest``` - This package is used to unittest the code.
   Installation : To install the package run ```pipenv install PyPDF2```
   
   Usage:
   assert - to assert the value that a function returns.


3. ```black```  - A PEP 8 compliant Python code formatter
   Installation : To install the package run ```pipenv install black```

   Usage: ```black  filename or directoryname```

## Bugs
1. The code won't work as expected on empty pdfs.

## Explanation of functions written in python 

1. ```fetchincidents()```     - Takes an incident page ```URL```, reads the incidents data from the url and return raw data(i.e; data in bytes format)  
2. ```extractincidents()```   - Takes the incident data( which is data in byte format) as input and creates a temporary pdf file and extract the contents of file as list of lists. Each item in the returned list is a list of strings of each individual row.  
3. ```createdb()```           - Creates an SQLite Database with a table named ```incidents```  
4. ```populatedb()```         - Populate the database with input values.  
5. ````Status()```            - Prints the query result in a formatted way to the std output.  
6. ```getindexesofdatecolumn()``` - Given a list of page contents as input parameter, returns a list with indexes of 'date time column'. this will helps us to form a row of data. 


## Approach of database development

```createdb()``` creates a database and also create a table named 'incidents' in the database. Before the creation of database i am checking whether the database file is there or not in project directory. if exists, i am deleting and creating a fresh database. This helps in storing the new data in database everytime we run the project. 

## Assumptions
I have made the following assumptions about data.  
1. For some of the rows in pdf, if there will be any missing values, those will be always 3rd and 4th columns.
2. For some of the rows in pdf, address column will always be 2 lines only.
3. The url will always be a incident url.

## Explanations of unit tests:

For each function in the project i have written one unit testcase.

1. test_fetchincidents() - in this test function, i am calling my method as usual by sending url as parameter. this gives me data in bytes. Now i have the same file in docs folder. Open the file using Open() and reads data from file using read() method and comparing whether both data is same or not.

2. test_extractincidents() - in this test function, opens the file and reads data from it and call the function named extractincidents. i am checking the length of the list that is returned by that function. 

3. test_createdb() - in this test function, i am checking the return type of createdb(). it should be an object of Connection class from sqlite3 package. i am also checking whether normanpd.db database file is created or not.

4. test_populatedb() - in this test function, by calling populatedb() i am inserting 2 records into the database and then wrote a select query to get the records in the database.

5. test_status() - in this test function, i used builtin fixture capsys to verify the output printed is same as the one that will be by calling status().

6. test_datetimeindexes() - in this test function, i am checking whether i am getting a list of indexes of date_time string. 
