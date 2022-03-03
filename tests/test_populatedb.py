import sqlite3
from project0.project0 import populatedb

def test_populatedb():
    table_data = [['2/2/2022 0:03', '2022-00005882', 'ALAMEDA ST / VICKSBURG AVE', 'MVA Non Injury', 'OK0140200'],
                            ['2/2/2022 0:15', '2022-00005884', '1525 E LINDSEY ST', 'Disturbance/Domestic', 'OK0140200']]
    conn = sqlite3.connect('./normanpd.db')
    populatedb(conn,table_data)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) from incidents")
    query_result = cursor.fetchall()
    assert query_result[0] == (2,)
