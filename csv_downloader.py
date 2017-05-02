from urlparse import urlparse
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup


REPORTS_URL = 'https://www.gov.uk/government/collections/uk-house-price-index-reports'
DOWNLOADS_MATCH_STRING = 'data downloads'
CSV_MATCH_STRING = 'uk hpi full file'


class CSVDownloader(object):
    def run(self):
        resp = requests.get(REPORTS_URL)
        html = BeautifulSoup(resp.text, 'html.parser')
        # TODO(riley): deal with failures
        downloads_page_href = self._get_most_recent_match(
            html.find_all('a'), DOWNLOADS_MATCH_STRING)

        resp = requests.get(downloads_page_href)
        html = BeautifulSoup(resp.text, 'html.parser')
        # TODO(riley): deal with failures
        csv_href = self._get_most_recent_match(
            html.find_all('a'), CSV_MATCH_STRING)
        filename = urlparse(csv_href).path.split('/')[-1]

        print "Downloading file. This may take a while"
        print csv_href
        csv = requests.get(csv_href)
        with open(filename, "wb") as f:
            f.write(csv.content)


    def _get_most_recent_match(self, links, match_substring):
        for l in links:
            if match_substring in l.text.lower():
                return urljoin(REPORTS_URL, l.get('href'))


if __name__ == '__main__':
    c = CSVDownloader()
    c.run()
