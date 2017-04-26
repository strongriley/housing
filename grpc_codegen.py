#!/usr/bin/env python
"""
Inspiration:
https://github.com/grpc/grpc/blob/v1.2.0/examples/python/route_guide/run_codegen.py
"""

from grpc_tools import protoc

protoc.main(
    (
        '',
        '-I./protos',
        '--python_out=./generated',
        '--grpc_python_out=./generated',
        './protos/housing.proto',
    )
)
