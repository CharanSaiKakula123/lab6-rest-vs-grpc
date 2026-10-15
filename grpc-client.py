#!/usr/bin/env python3

import argparse
import base64
import random
import time

import grpc
import lab6_pb2
import lab6_pb2_grpc


def doAdd(stub, debug=False):
    response = stub.add(lab6_pb2.addMsg(a=5, b=10))
    if debug:
        print("Sum:", response.sum)


def doRawImage(stub, debug=False):
    with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
        image_data = f.read()

    response = stub.rawimage(lab6_pb2.rawImageMsg(img=image_data))
    if debug:
        print("Image dimensions:", response.width, response.height)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    response = stub.dotproduct(lab6_pb2.dotProductMsg(a=a, b=b))
    if debug:
        print("Dot product:", response.dotproduct)


def doJsonImage(stub, debug=False):
    with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = stub.jsonimage(lab6_pb2.jsonImageMsg(img=image_data))
    if debug:
        print("Image dimensions:", response.width, response.height)


parser = argparse.ArgumentParser(description="gRPC client for Lab 6")
parser.add_argument("host", help="IP address or hostname of the gRPC server")
parser.add_argument(
    "cmd",
    choices=["add", "rawImage", "dotProduct", "jsonImage"]
)
parser.add_argument("reps", type=int, help="Number of repetitions")
parser.add_argument("-p", "--port", type=int, default=50051)
parser.add_argument("-d", "--debug", action="store_true")
args = parser.parse_args()

if args.reps <= 0:
    parser.error("reps must be greater than zero")

address = f"{args.host}:{args.port}"
print(f"Running {args.reps} reps against {address}")

operations = {
    "add": doAdd,
    "rawImage": doRawImage,
    "dotProduct": doDotProduct,
    "jsonImage": doJsonImage,
}

with grpc.insecure_channel(address) as channel:
    stub = lab6_pb2_grpc.Lab6Stub(channel)

    # Warm up the connection before timing requests.
    operations[args.cmd](stub)

    start = time.perf_counter()
    for _ in range(args.reps):
        operations[args.cmd](stub, debug=args.debug)
    elapsed_ms = (time.perf_counter() - start) * 1000 / args.reps

print("Took", elapsed_ms, "ms per operation")
