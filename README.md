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
   usage        :  

   PdfFileReader() - to create an pdf reader object.  
   getNumPages()   - gives the count of total number of pages in a pdf.  
   getPage()       - to access a individual page. will send page number as a parameter.  
   extractText()   - to extract the content of a page.  
   

2. ```pytest``` - This package is used to unittest the code.  
   Installation : To install the package run ```pipenv install pytest```  
   
   Usage        :  
   
   assert - to assert the value that a function returns.

## Bugs


## Explanation of functions written in python 

1. ```fetchincidents()```     - Takes an incident page ```URL```, reads the incidents data from the url and return raw data(i.e; data in bytes format)  
2. ```extractincidents()```   - Takes the incident data( which is data in byte format) as input and creates a temporary pdf file and extract the contents of file as list of lists. Each item in the returned list is a list of strings of each individual row.  
3. ```createdb()```           - Creates an SQLite Database with a table named ```incidents```  
4. ```populatedb()```         - Populate the database with input values.  
5. ```Status()```            - Prints the query result in a formatted way to the std output.  
6. ```getindexesofdatecolumn()``` - Given a list of page contents as input parameter, returns a list with indexes of 'date time column'. this 
will helps us to form a row of data. 


## Approach of database development

```createdb()``` creates a database and also create a table named 'incidents' in the database. Before the creation of database i am checking whether the database file is there or not in project directory. if exists, i am deleting and creating a fresh database. This helps in storing the new data in database everytime we run the project. 

## Assumptions
I have made the following assumptions about data.  
1. For some of the rows in pdf, if there will be any missing values, those will be always 3rd and 4th columns.
2. For some of the rows in pdf, address column will always be 2 lines only.
