# Largely based on
# https://github.com/grpc/grpc/blob/v1.2.0/examples/python/route_guide/route_guide_client.py
import grpc
from datetime import date
import calendar


from generated import housing_pb2
from generated import housing_pb2_grpc


def fetch_estimate(stub, from_date, to_date, borough, price):
    # TODO(riley): double-check timezones are doing the right thing
    if from_date:
        from_timestamp = calendar.timegm(from_date.timetuple())
    else:
        from_timestamp = None
    if to_date:
        to_timestamp = calendar.timegm(to_date.timetuple())
    else:
        to_timestamp = None
    request = housing_pb2.EstimatePriceRequest(
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        borough=borough,
        price_in_pounds=price)
    estimate_response = stub.EstimatePrice(request)
    print estimate_response


def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = housing_pb2_grpc.HousingStub(channel)
    print "Expecting: 366,700 (PDF states 366,726 but missing precision)"
    fetch_estimate(stub, date(2000, 1, 1), date(2016, 1, 1), 'Islington',
                   100000)
    print "Expecting: MISSING_FROM_TIMESTAMP"
    fetch_estimate(stub, None, date(2016, 1, 1), 'Islington',
                   100000)
    print "Expecting: MISSING_TO_TIMESTAMP"
    fetch_estimate(stub, date(2000, 1, 1), None, 'Islington',
                   100000)
    print "Expecting: MISSING_PRICE_IN_POUNDS"
    fetch_estimate(stub, date(2000, 1, 1), date(2016, 1, 1), 'Islington', 0)
    print "Expecting: TIMESTAMPS_OUT_OF_ORDER"
    fetch_estimate(stub, date(2016, 1, 1), date(2000, 1, 1), 'Islington',
                   100000)
    print "Expecting: BOROUGH_NOT_FOUND"
    fetch_estimate(stub, date(2000, 1, 1), date(2016, 1, 1), 'Not Real',
                   100000)


if __name__ == '__main__':
    main()
