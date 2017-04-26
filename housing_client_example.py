# Largely based on https://github.com/grpc/grpc/blob/v1.2.0/examples/python/route_guide/route_guide_client.py
import grpc
from datetime import date
import calendar


from generated import housing_pb2
from generated import housing_pb2_grpc


def fetch_estimate(stub, from_date, to_date, borough, price):
    # TODO(riley): double-check timezones are doing the right thing
    from_timestamp = calendar.timegm(from_date.timetuple())
    to_timestamp = calendar.timegm(to_date.timetuple())
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
    print "Expecting: 366,726"
    fetch_estimate(stub, date(2000, 1, 1), date(2016, 1, 1), 'Islington',
                   100000)
    print "Expecting: MISSING_FROM_TIMESTAMP"
    fetch_estimate(stub, date(1970, 1, 1), date(2016, 1, 1), 'Islington',
                   100000)
    print "Expecting: MISSING_TO_TIMESTAMP"
    fetch_estimate(stub, date(2000, 1, 1), date(1970, 1, 1), 'Islington',
                   100000)
    print "Expecting: MISSING_PRICE_IN_POUNDS"
    fetch_estimate(stub, date(2000, 1, 1), date(2016, 1, 1), 'Islington', 0)
    print "Expecting: out of order"
    fetch_estimate(stub, date(2016, 1, 1), date(2000, 1, 1), 'Islington',
                   100000)



if __name__ == '__main__':
    main()
