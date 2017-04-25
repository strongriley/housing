from os.path import isfile
import csv
from datetime import datetime

import requests

CSV_URL = ('http://publicdata.landregistry.gov.uk/market-trend-data/'
           'house-price-index-data/UK-HPI-full-file-2016-05.csv')
FILENAME = 'HPI.csv'


# TODO(riley): probably make singleton. Otherwise could waste lots of memory
class HousingData(object):
    _cache = None

    def __init__(self):
        self._cache = dict()
        if not isfile(FILENAME):
            self.download_csv()
        self.load_csv()

    def load_csv(self):
        with open(FILENAME, 'rb') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip headers
            for row in reader:
                name = row[1]
                date_obj = datetime.strptime(row[0], '%d/%m/%Y').date()
                idx = row[4]
                if name not in self._cache:
                    self.cache[name] = dict()
                self.cache[name][date_obj] = idx

    # TODO(riley): write tests for this. Too lazy to stub out
    def downlaod_csv(self):
        print 'downloading CSV (may take some time)'
        csv = requests.get(CSV_URL)
        with open(FILENAME, "wb") as f:
            f.write(csv.content)
