from runner import Result
from io import TextIOWrapper

from dataclasses import dataclass
from typing import List, Set, Tuple, Optional

@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int
    height: int

    @staticmethod
    def from_char(x: int, y:int, char: str):
        return Point(x, y, ord(char) - ord('a'))

class Map:
    def __init__(self, points: List[List[Point]], start_point: Point, end_point: Point) -> None:
        self.points: List[List[Point]] = points
        self.max_y = len(points)
        self.max_x = len(points[0])
        self.start_point: Point = start_point
        self.end_point: Point = end_point
        self.visited: Set[Tuple[int, int]] = set()

    def __str__(self) -> str:
        lines = []
        for y, row in enumerate(self.points):
            line = ""
            for x, col in enumerate(row):
                if (x, y) == (self.start_point.x, self.start_point.y):
                    line += "S"
                elif (x, y) == (self.end_point.x, self.end_point.y):
                    line += "E"
                else:
                    line += chr(ord('a') + col.height)

            lines.append(line)

        return "\n".join(lines)

    def discover_neighbours(self, x: int, y: int) -> List[Point]:
        neighbours = []
        adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in adjacent:
            if ((y + dy < self.max_y and y + dy >= 0) and
                (x + dx < self.max_x and x + dx >= 0)):

                if (x + dx, y + dy) in self.visited:
                    continue

                if self.points[y][x].height + 1 >= self.points[y + dy][x + dx].height:
                    neighbours.append(self.points[y + dy][x + dx])

        return neighbours

    def find_best_hiking_trail(self) -> int:
        """Returns the shortest path to a point with an elevation "a" on the map"""
        trails_len = []
        for x in range(0, self.max_x):
            for y in range(0, self.max_y):
                if self.points[y][x].height == 0:
                    d = self.find_peak(self.points[y][x])
                    if d > 0:
                        trails_len.append(d)

        return min(trails_len)

    def find_peak(self, start_point: Optional[Point] = None) -> int:
        """
        Starting from the start_point, find self.end_point using the part 1 rule:
        * Can only go to the next point if the next height <= current_height + 1

        Returns the number of steps
        """
        self.visited = set()
        current_cost = 1
        if not start_point:
            start_point = self.start_point

        open_set = [(current_cost, neighbour) for neighbour in self.discover_neighbours(start_point.x, start_point.y)]
        self.visited.add((start_point.x, start_point.y))
        while open_set:
            # remove element with lowest cost
            lowest_cost, lowest_node = open_set[0]
            for cost, node in open_set:
                if cost < lowest_cost:
                    lowest_cost = cost
                    lowest_node = node

            open_set.remove((lowest_cost, lowest_node))
            self.visited.add((lowest_node.x, lowest_node.y))
            # increment cost, add neighbours back to openset
            if (lowest_node.x, lowest_node.y) == (self.end_point.x, self.end_point.y):
                return lowest_cost
            else:
                neighbours = [(lowest_cost + 1, neighbour) for neighbour in self.discover_neighbours(lowest_node.x, lowest_node.y) if (lowest_cost + 1, neighbour) not in open_set]
                open_set += neighbours

        return -1

def parse_map(file: TextIOWrapper) -> Map:
    points = []
    start_point = None
    end_point = None

    for y, line in enumerate(file):
        x_points = []
        for x, char in enumerate(line.strip()):
            if char == "S":
                start_point = Point(x, y, 0)
                x_points.append(start_point)
            elif char == "E":
                end_point = Point(x, y, 26)
                x_points.append(end_point)
            else:
                x_points.append(Point.from_char(x, y, char))

        points.append(x_points)

    if not start_point or not end_point:
        raise Exception("Parser did not find start or end points")

    hill_map = Map(points, start_point, end_point)

    return hill_map

def main(input_file: TextIOWrapper) -> Result:
    hill_map = parse_map(input_file)
    return Result(hill_map.find_peak(), hill_map.find_best_hiking_trail())
