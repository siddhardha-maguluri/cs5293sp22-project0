from project0.project0 import getindexesofdatecolumn

def test_datetimeindexes():
    rows = ['2/2/2022 0:03', '2022-00005882', 'ALAMEDA ST / VICKSBURG AVE', 'MVA Non Injury', 'OK0140200',
            '2/2/2022 0:15', '2022-00005884', '1525 E LINDSEY ST', 'Disturbance/Domestic', 'OK0140200']
    actual_data = getindexesofdatecolumn(rows)
    assert actual_data == [0,5]  