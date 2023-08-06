# Anko Investor Python SDK

This module provides a simple Anko Investor Forecasts gRPC Service client for python.

This module does little more wrap [grpc](https://pypi.org/project/grpcio/) with retry logic and authorization wrappers.

```
$ pip install anko-sdk
```

## Usage

Given a valid token from https://anko-investor.com (see: [Getting Started](https://github.com/anglo-korean/documentation#getting-started) for more information), the following example will start consuming Forecasts

```python
import os
import socket

from anko import Client

c = Client(os.environ.get('ANKO_TOKEN'), socket.gethostname())

for forecast in c:
    if forecast:
        print(forecast)

```

(Here we use the current machine's hostname as a client identifier- this can be anything, really; it's useful to set in case you need to open a support ticket to help debug connections. It can even be an empty string).
