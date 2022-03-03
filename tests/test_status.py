import sqlite3
from project0.project0 import status

def test_status(capsys):
    conn = sqlite3.connect('./normanpd.db')
    status(conn)
    actual_output = capsys.readouterr()
    expected_output = "Disturbance/Domestic|1\nMVA Non Injury|1\n"
    assert actual_output[0] == expected_output
