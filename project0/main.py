import argparse
import project0


def main(url):

    # Download data
    incident_data = project0.fetchincidents(url)

    # Extract data
    incidents = project0.extractincidents(incident_data)

    # Create new database
    # db = project0.createdb()

    # with open('./incidents_data.csv', 'w',newline='') as csvfile:
    #     filewriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #     for i in range(5, len(pdf_data)-3, 5):
    #         filewriter.writerow([pdf_data[i], pdf_data[i+1], pdf_data[i+2], pdf_data[i+3], pdf_data[i+4]])
    #     csvfile.close()
    #
    # pdfFileObj.close()
    #
    # try:
    #     connnection = sqlite3.connect('./normanpd.db')
    #     print("database created successfully")
    #
    #     cursor = connnection.cursor()
    #
    #     create_incidents_table = ''' CREATE TABLE incidents (
    #                             incident_time TEXT,
    #                             incident_number TEXT,
    #                             incident_location TEXT,
    #                             nature TEXT,
    #                             incident_ori TEXT
    #                             );
    #                       '''
    #     cursor.execute(create_incidents_table)
    #
    #     incidents_csv_file = open('./incidents_data.csv')
    #     csv_file_contents = csv.reader(incidents_csv_file)
    #
    #     insert_records = '''INSERT INTO incidents (
    #                         incident_time,
    #                         incident_number,
    #                         incident_location,
    #                         nature,
    #                         incident_ori ) VALUES (?,?,?,?,? )'''
    #
    #     cursor.executemany(insert_records, csv_file_contents)
    #
    #     # SQL query to retrieve names of unique incidents and their count
    #     select_unique_incident_natures = "SELECT nature, count(nature) as no_of_times from incidents group by nature"
    #     query_result = cursor.execute(select_unique_incident_natures)
    #
    #     # Output the query result
    #     for row in query_result:
    #         print(row)
    #
    #     connnection.commit()
    # except Error as e:
    #     print(e)
    # finally:
    #     if connnection:
    #         connnection.close()
    # Download data
    # incident_data = project0.fetchincidents(url)



    # # Create new database
    # db = project0.createdb()

    # # Insert data
    # project0.populatedb(db, incidents)

    # Print incident counts
    # project0.status(db)
    # print("Given url is:")
    # print(url)
    # print('Sample incident data')
    # print(incident_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
