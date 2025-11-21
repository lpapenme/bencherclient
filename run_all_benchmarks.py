import math
import random

import requests
from bencherscaffold.client import BencherClient
from bencherscaffold.protoclasses.bencher_pb2 import Value, ValueType

if __name__ == '__main__':

    client = BencherClient()


    response = requests.get(
        'https://raw.githubusercontent.com/lpapenme/bencher/refs/heads/main/BencherServer/benchmark-registry.json',
    )

    registry = response.json()

    for benchmarkname, properties in registry.items():
        dimensions = properties['dimensions']
        benchmark_type = properties['type']
        # types can be PURELY_CONTINUOUS, PURELY_BINARY,PURELY_CATEGORICAL,PURELY_ORDINAL_REAL,PURELY_ORDINAL_INT, MIXED (lower case)
        # but we only support PURELY_CONTINUOUS, PURELY_BINARY,PURELY_CATEGORICAL,PURELY_ORDINAL_INT
        # create point type

        # if dimension is None, sample one between 1 and 10
        if dimensions is None:
            dimensions = random.randint(1, 10)
            # resample until not perfect square
            while math.sqrt(dimensions) % 1 == 0:
                dimensions = random.randint(1, 10)
        if benchmarkname in ['pbo-isingtriangular', 'pbo-nqueens']:
            # needs to be perfect square
            dimensions = dimensions ** 2

        match benchmark_type:
            case 'purely_continuous':
                values = [Value(type=ValueType.CONTINUOUS, value=0.5) for _ in range(dimensions)]
            case 'purely_binary':
                values = [Value(type=ValueType.BINARY, value=0) for _ in range(dimensions)]
            case 'purely_categorical':
                values = [Value(type=ValueType.CATEGORICAL, value=0) for _ in range(dimensions)]
            case 'purely_ordinal_int':
                values = [Value(type=ValueType.INTEGER, value=0) for _ in range(dimensions)]
            case 'mixed':
                if benchmarkname == 'svmmixed':
                    values = [Value(type=ValueType.BINARY, value=0) for _ in range(50)]
                    values += [Value(type=ValueType.CONTINUOUS, value=0.5) for _ in range(3)]
                else:
                    raise ValueError(f"Unsupported benchmark type: {benchmark_type}")
            case _:
                raise ValueError(f"Unsupported benchmark type: {benchmark_type}")
        client.evaluate_point(
            benchmark_name=benchmarkname,
            point=values
        )
        print(f"Evaluated {benchmarkname} with dimensions {dimensions} and type {benchmark_type}")
