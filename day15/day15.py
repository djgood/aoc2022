from io import TextIOWrapper
import re
from typing import Iterator

from runner import Result
from util import Point2D

def parse_sensor_beacon(input_file: TextIOWrapper) -> dict[Point2D, Point2D]:
    sensor_parser = re.compile("Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)")
    sensors_to_beacons = dict()
    for line in input_file:
        m = sensor_parser.match(line.strip())
        if not m:
            raise RuntimeError("Could not parse input")

        sensor = Point2D(int(m[1]), int(m[2]))
        beacon = Point2D(int(m[3]), int(m[4]))
        sensors_to_beacons[sensor] = beacon

    return sensors_to_beacons

def main(input_file: TextIOWrapper) -> Result:
    row = 2000000
    sensor_range: dict[Point2D, int] = dict()
    sensors_to_beacons = parse_sensor_beacon(input_file)
    for sensor, beacon in sensors_to_beacons.items():
        sensor_range[sensor] = sensor.manhattan(beacon)

    rows: list[list[int]] = []
    for sensor in sensors_to_beacons:
        if (sensor.y + sensor_range[sensor] < row and
            sensor.y - sensor_range[sensor] > row):
            # sensor is not relevant
            break

        # sensor diamond is within the row
        y_diff = abs(sensor.y - row)
        remaining_distance = (sensor_range[sensor] - y_diff)
        row_left = sensor.x - remaining_distance
        row_right = sensor.x + remaining_distance
        rows.append([row_left, row_right])

    # compress rows
    rows.sort()
    compressed = [rows[0]]
    for interval in rows[1:]:
        if compressed[-1][0] <= interval[0] <= compressed[-1][1]:
            # merge
            compressed[-1][1] = max(compressed[-1][1], interval[1])
        else:
            compressed.append(interval)

    spots = sum([interval[1] - interval[0] + 1 for interval in compressed])
    # find beacons on row in interval
    beacons = 0
    for beacon in set(sensors_to_beacons.values()):
        if beacon.y == row:
            for interval in compressed:
                if beacon.x >= interval[0] and beacon.x <= interval[1]:
                    beacons += 1
                    break

    print(spots - beacons)

    return Result(None, None)
