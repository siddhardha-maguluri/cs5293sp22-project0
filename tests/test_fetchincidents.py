from project0.project0 import fetchincidents

def test_fetchincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-01_daily_incident_summary.pdf"
    with open('./docs/2022-02-01_daily_incident_summary.pdf','rb') as pdf:
        expected_pdf_data  = pdf.read()
    assert fetchincidents(url) == expected_pdf_data