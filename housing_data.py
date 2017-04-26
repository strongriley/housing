from os.path import isfile
import csv
from datetime import datetime
from decimal import Decimal

import requests

CSV_URL = ('http://publicdata.landregistry.gov.uk/market-trend-data/'
           'house-price-index-data/UK-HPI-full-file-2016-05.csv')
FILENAME = 'HPI.csv'


class BoroughNotFound(Exception):
    pass


class DateNotFound(Exception):
    pass


# TODO(riley): probably make singleton. Otherwise could waste lots of memory
class HousingData(object):
    _cache = None

    def __init__(self):
        self._cache = dict()
        if not isfile(FILENAME):
            self._download_csv()
        self._load_csv()

    def get_price_index(self, borough, idx_date):
        borough = borough.lower()
        if borough not in self._cache:
            raise BoroughNotFound("'%s' borough not found" % borough)
        if idx_date not in self._cache[borough]:
            raise DateNotFound("'%s' date not found" % idx_date)
        return self._cache[borough][idx_date]

    def _load_csv(self):
        print "Loading CSV"
        with open(FILENAME, 'rb') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip headers
            for row in reader:
                name = row[1].lower()
                date_obj = datetime.strptime(row[0], '%d/%m/%Y').date()
                idx = Decimal(row[4])
                if name not in self._cache:
                    self._cache[name] = dict()
                self._cache[name][date_obj] = idx

    # TODO(riley): write tests for this. Too lazy to stub out
    def _download_csv(self):
        print 'Downloading CSV (this may take some time)'
        csv = requests.get(CSV_URL)
        with open(FILENAME, "wb") as f:
            f.write(csv.content)
