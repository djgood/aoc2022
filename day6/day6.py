def read_input(filename: str):
    with open(filename) as file:
        for line in file:
            yield line

def start_packet(line: str) -> int:
    for cursor in range(len(line)):
        if len(set(line[cursor:cursor+4])) == 4:
            return cursor + 4

    return -1

def start_message(line: str) -> int:
    for cursor in range(len(line)):
        if len(set(line[cursor:cursor+14])) == 14:
            return cursor + 14

    return -1

def main():
    print("== Part 1 ==")
    print("== Sample ==")
    for line in read_input("sample_input.txt"):
        print(start_packet(line))

    print("== Real ==")
    for line in read_input("input.txt"):
        print(start_packet(line))

    print("== Part 2 ==")
    print("== Sample ==")
    for line in read_input("sample_input.txt"):
        print(start_message(line))
    print("== Real ==")
    for line in read_input("input.txt"):
        print(start_message(line))

if __name__ == "__main__":
    main()
