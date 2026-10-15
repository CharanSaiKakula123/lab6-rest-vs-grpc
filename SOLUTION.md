# Lab 6: REST vs. gRPC Benchmark Results

| Method | Local (ms/op) | Same-Zone (ms/op) | Different Region (ms/op) |
|---|---:|---:|---:|
| REST add | 2.097 | 2.911 | 351.544 |
| gRPC add | 0.376 | 1.177 | 164.988 |
| REST rawImage | 4.107 | 8.911 | 1280.402 |
| gRPC rawImage | 3.797 | 11.877 | 195.892 |
| REST dotProduct | 2.401 | 4.028 | 316.741 |
| gRPC dotProduct | 0.369 | 1.223 | 161.236 |
| REST jsonImage | 24.200 | 41.928 | 1432.898 |
| gRPC jsonImage | 17.103 | 36.310 | 235.342 |
| PING | 0.035 | 0.434 | 158.791 |

## Observations

On localhost, gRPC was faster than REST for all four operations, although the difference was relatively small for rawImage. In the same zone, gRPC was faster for add, dotProduct, and jsonImage but not for rawImage. These results show that gRPC is not necessarily faster for every operation.

Network latency has a substantial effect when the client and server are in different regions. The average ping RTT increased from 0.434 ms in the same zone to 158.791 ms between Oregon and Frankfurt. The cross region gRPC add and dotProduct results were close to the ping RTT, while REST took longer. The image operations took much longer with cross-region REST than with gRPC, likely due to a combination of connection overhead, payload transfer, serialization, and processing. These results should be interpreted with care because the repetition counts differed across some crossregion tests and the image operation latencies were notably high.