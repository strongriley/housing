from concurrent import futures
from datetime import datetime
import time

import grpc

from generated import housing_pb2
from generated import housing_pb2_grpc
from housing_data import HousingData
from housing_data import BoroughNotFound
from housing_data import DateNotFound


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class HousingServicer(housing_pb2_grpc.HousingServicer):
    data = None

    def __init__(self):
        self.data = HousingData()

    def EstimatePrice(self, request, context):
        response = housing_pb2.EstimatePriceResponse()
        error = None
        if request.from_timestamp == 0:
            response.error = housing_pb2.MISSING_FROM_TIMESTAMP
            return response
        if request.to_timestamp == 0:
            response.error = housing_pb2.MISSING_TO_TIMESTAMP
            return response
        if request.price_in_pounds == 0:
            response.error = housing_pb2.MISSING_PRICE_IN_POUNDS
            return response
        if not request.borough:
            response.error = housing_pb2.MISSING_BOROUGH
            return response

        from_date = datetime.utcfromtimestamp(
            request.from_timestamp).date()
        to_date = datetime.utcfromtimestamp(
            request.to_timestamp).date()
        # Always start on the first of the monthb
        from_date.replace(day=1)
        to_date.replace(day=1)
        if to_date < from_date:
            response.error = housing_pb2.TIMESTAMPS_OUT_OF_ORDER
            return response

        # TODO(riley): clean this up. Sad flow
        try:
            try:
                from_idx = self.data.get_price_index(
                    request.borough, from_date)
            except DateNotFound:
                response.error = housing_pb2.FROM_TIMESTAMP_NOT_FOUND
                return response
            try:
                to_idx = self.data.get_price_index(
                    request.borough, to_date)
            except DateNotFound:
                response.error = housing_pb2.TO_TIMESTAMP_NOT_FOUND
                return response
        except BoroughNotFound:
            response.error = housing_pb2.BOROUGH_NOT_FOUND
            return response
        print "from index: %s" % from_idx
        print "to index: %s" % to_idx
        estimated_price = int(to_idx / from_idx * request.price_in_pounds)
        response.estimated_price_in_pounds = estimated_price
        return response


# Largely based on:
# https://github.com/grpc/grpc/blob/v1.2.0/examples/python/route_guide/route_guide_server.py
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    housing_pb2_grpc.add_HousingServicer_to_server(HousingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print "Service started"
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print "Service stopping"
        server.stop(0)

if __name__ == '__main__':
    serve()
