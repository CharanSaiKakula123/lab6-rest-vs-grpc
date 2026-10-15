#!/usr/bin/env python3

from concurrent import futures
import argparse
import base64
import io

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Servicer(lab6_pb2_grpc.Lab6Servicer):

    def add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def rawimage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )
        except Exception:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid image data")
            return lab6_pb2.imageReply()

    def dotproduct(self, request, context):
        if len(request.a) != len(request.b):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Vectors must have the same length")
            return lab6_pb2.dotProductReply()

        result = sum(a * b for a, b in zip(request.a, request.b))
        return lab6_pb2.dotProductReply(dotproduct=result)

    def jsonimage(self, request, context):
        try:
            image_data = base64.b64decode(request.img, validate=True)
            img = Image.open(io.BytesIO(image_data))
            return lab6_pb2.imageReply(
                width=img.size[0],
                height=img.size[1]
            )
        except Exception:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid image data")
            return lab6_pb2.imageReply()


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Servicer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gRPC server for Lab 6")
    parser.add_argument("-p", "--port", type=int, default=50051)
    args = parser.parse_args()
    serve(args.port)
