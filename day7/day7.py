from __future__ import annotations
from typing import List, Optional, Union

def read_input(path: str):
    with open(path) as file:
        for line in file:
            yield line.strip()

class File:

    def __init__(self, name: str, size: str) -> None:
        self.name = name
        self.size = int(size)

    def to_string(self, current_indent=0) -> str:
        return " " * current_indent + f" - {self.size} {self.name}\n"

class Directory:

    def __init__(self, name: str, parent: Optional[Directory]) -> None:
        self.name = name
        self.parent = parent
        self.children = []

    def discover_file(self, file: Union[Directory, File]):
        self.children.append(file)

    def to_string(self, current_indent=0) -> str:
        indent = " " * current_indent
        s = indent + f" - dir {self.name}\n"
        for child in self.children:
            s += child.to_string(current_indent=current_indent + 2)
        return s

    def calc_size(self):
        size = 0
        for child in self.children:
            if isinstance(child, Directory):
                size += child.calc_size()
            else:
                size += child.size

        self.size = size
        return size

    def all_sizes(self, lt: Optional[int] = None) -> List[int]:
        sl = []

        if lt is None or self.size <= lt:
            sl.append(self.size)

        for child in self.children:
            if isinstance(child, Directory):
                sl += child.all_sizes(lt)

        return sl

def main():
    terminal = read_input("input.txt")
    next(terminal)
    # Parse input
    root = Directory("/", parent=None)
    cur_dir = root
    for input_line in terminal:
        assert cur_dir is not None
        if input_line.startswith("$"):
            cmd = input_line[2:].split(" ")
            if cmd[0] == "ls":
                pass
            else: # cmd[0] == "cd"
                arg = cmd[1]
                if arg == "..":
                    cur_dir = cur_dir.parent
                else:
                    new_dir = Directory(arg, parent=cur_dir)
                    cur_dir.children.append(new_dir)
                    cur_dir = new_dir
        else:
            output = input_line.split(" ")
            if output[0] == "dir":
                # Build dir when changing the directory
                pass
            else:
                file = File(output[1], output[0])
                cur_dir.discover_file(file)

    root.calc_size()
    print("== Part 1 ==")
    print(sum(root.all_sizes(100000)))
    unused = 70000000 - root.size
    space_needed = 30000000 - unused
    print("== Part 2 ==")
    # Could probably have written the earlier function as something similar to
    # this but oh well!
    print(min(s for s in root.all_sizes() if s > space_needed))

if __name__ == "__main__":
    main()
