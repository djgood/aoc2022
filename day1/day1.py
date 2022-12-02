import heapq

def run():
    with open("input.txt") as input:
        elves = []
        calories_buffer = 0
        for line in input:
            if line == "\n":
                heapq.heappush(elves, -calories_buffer)
                calories_buffer = 0
            else:
                calories_buffer += int(line)

        top3 = [-heapq.heappop(elves) for _ in range(3)]
        print(top3[0])
        print(sum(top3))

if __name__ == "__main__":
    run()
