import unittest

import responses

from csv_downloader import CSVDownloader
from csv_downloader import REPORTS_URL

with open('fixtures/reports_good.html', 'r') as f:
    reports_good_body = f.read()

with open('fixtures/downloads_good.html', 'r') as f:
    downloads_good_body = f.read()

GOOD_DOWNLOADS_URL = 'https://www.gov.uk/government/statistical-data-sets/uk-house-price-index-data-downloads-february-2017'


GOOD_CSV_URL = 'http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/UK-HPI-full-file-2017-02.csv?utm_medium=GOV.UK&utm_source=datadownload&utm_campaign=full_fil&utm_term=9.30_11_04_17'
GOOD_CSV_URL = 'http://publicdata.landregistry.gov.uk/market-trend-data/house-price-index-data/UK-HPI-full-file-2017-02.csv'

class CSVDownloaderTestCase(unittest.TestCase):
    @responses.activate
    def test_happy_path(self):
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.GET, REPORTS_URL, body=reports_good_body)
            rsps.add(responses.GET, GOOD_DOWNLOADS_URL, body=downloads_good_body)
            rsps.add(responses.GET, GOOD_CSV_URL, body='yay')
            c = CSVDownloader()
            c.run()

    @responses.activate
    def test_downloads_bad(self):
        pass

    @responses.activate
    def test_reports_bad(self):
        pass

    @responses.activate
    def test_timeouts(self):
        pass

    @responses.activate
    def test_404(self):
        pass



if __name__ == '__main__':
    unittest.main()
