from project0.project0 import createdb
import sqlite3
import os

def test_createdb():
    conn = isinstance(createdb(), (sqlite3.Connection))
    assert True == conn
    assert True == os.path.exists('normanpd.db')