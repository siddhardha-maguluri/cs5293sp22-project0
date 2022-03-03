from project0.project0 import extractincidents

def test_extraincidents():
    with open('./docs/2022-02-01_daily_incident_summary.pdf','rb') as pdf:
        test_data  = pdf.read()
    assert len(extractincidents(test_data)) == 392  