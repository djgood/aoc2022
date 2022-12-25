from __future__ import annotations

from io import TextIOWrapper
from typing import Optional
from runner import Result

from util import Point2D

class Map:
    lowest_y = 0
    walls = set()

    def draw_line(self, start: Point2D, end: Point2D):
        diff = end - start
        if diff.x == 0:
            if diff.y >= 0:
                range_iter = range(0, diff.y + 1)
            else:
                range_iter = range(diff.y, 1)

            for dy in range_iter:
                self.walls.add(Point2D(start.x, start.y + dy))

            self.lowest_y = max(end.y, self.lowest_y)

        elif diff.y == 0:
            if diff.x >= 0:
                range_iter = range(0, diff.x + 1)
            else:
                range_iter = range(diff.x, 1)

            for dx in range_iter:
                self.walls.add(Point2D(start.x + dx, start.y))
        else:
            raise RuntimeError("Diagonal lines not supported")

    def sand_sim(self, floor_y: Optional[int] = None):
        stopped_sand = set()
        blocking = set.union(stopped_sand, self.walls)
        while True:
            # add a new unit of sand
            cur_pos = Point2D(500, 0)
            if Point2D(500, 0) in stopped_sand:
                print("Maxmimum sand pile reached")
                break

            if floor_y is None:
                lowest_y = self.lowest_y
            else:
                lowest_y = floor_y

            while cur_pos.y < lowest_y:
                if floor_y:
                    if cur_pos.y + 1 == floor_y:
                        blocking.add(cur_pos)
                        stopped_sand.add(cur_pos)
                        break

                # calc blocking set
                # find a free spot
                if Point2D(cur_pos.x, cur_pos.y + 1) not in blocking:
                    # gravity
                    cur_pos = Point2D(cur_pos.x, cur_pos.y + 1)
                elif Point2D(cur_pos.x - 1, cur_pos.y + 1) not in blocking:
                    # left diag
                    cur_pos = Point2D(cur_pos.x - 1, cur_pos.y + 1)
                elif Point2D(cur_pos.x + 1, cur_pos.y + 1) not in blocking:
                    # right diag
                    cur_pos = Point2D(cur_pos.x + 1, cur_pos.y + 1)
                else:
                    # actually stopped
                    blocking.add(cur_pos)
                    stopped_sand.add(cur_pos)
                    break

            if floor_y is None:
                if cur_pos.y >= self.lowest_y:
                    break

        return len(stopped_sand)


def parse_map(input_file: TextIOWrapper) -> Map:
    map_2d = Map()
    for line in input_file:
        points = line.strip().split("->")
        last_point: Optional[Point2D] = None
        for point_str in points:
            x, y = point_str.split(",")
            point = Point2D(int(x), int(y))
            if not last_point:
                last_point = point

            map_2d.draw_line(last_point, point)
            last_point = point

    return map_2d

def main(input_file: TextIOWrapper) -> Result:
    map_2d = parse_map(input_file)
    return Result(map_2d.sand_sim(), map_2d.sand_sim(floor_y=map_2d.lowest_y + 2))
