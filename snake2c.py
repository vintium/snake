import sys
from typing import TextIO

INDENTATION = "    "


def indent_of_line(l: str, indentation: str) -> int:
    indent: int = 0
    while l.removeprefix(indentation) != l:
        l = l.removeprefix(indentation)
        indent += 1 
    return indent

def snake2c(source: str, indentation: str, sink: TextIO = sys.stdout):
    indent: int = 0
    for line in source.splitlines():
        line_indent = indent_of_line(line, indentation)
        if line.startswith("import"):
            if line == "import":
                print(f"ERROR: empty import", file=sys.stderr)
                exit(1); 

            if line[6:8] == " \"" or line[6:8] == " '":
                print(f"#include {line[7:]}", file=sink)
            else:
                print(f"#include <{line[7:]}>", file=sink) 
        elif line.startswith("#"):
            print(f"{line}", file=sink) 
        elif line_indent > indent:
            for i in range(indent, line_indent):
                print(f"{indentation * i}{{", file=sink)
                indent += 1
            if line.strip() == '':
                print(f"{line}", file=sink)
            else:
                print(f"{line};", file=sink)
        elif line.endswith(':'):
            print(f"{line[:-1]} {{", file=sink)
            indent += 1
        elif line_indent == indent:
            if line.strip() == '':
                print(f"{line}", file=sink)
            else:
                print(f"{line};", file=sink)
 
        elif line_indent < indent:
            for d in reversed(range(line_indent, indent)):
                print(f"{indentation * d}}}")
                indent -= 1
            if line.strip() == '':
                print(f"{line}", file=sink)
            else:
                print(f"{line};", file=sink)
 
        else:
            print(f"ERROR: idk wtf to do with this line!!!", file=sys.stderr)
            print(f"NOTE: content of line: {repr(line)}", file=sys.stderr)
            exit(1);

def usage(program: str):
    """ prints the usage for the program """
    # TODO: Add usage
    pass


def main(args: list[str]) -> int:
    if len(args) < 2:
        usage()
        print("ERROR: no file provided",
              file=sys.stderr) 
        return 1;
    in_fn = args[1]
    # TODO: add support for providing an output file name.
    with open(in_fn, 'r') as in_f:
        snake_source = in_f.read()
        # TODO: detect indentation style in program.
        # for now, this only supports 4 spaces.
        snake2c(snake_source, INDENTATION) 
        

if __name__ == "__main__":
    exit(main(sys.argv))
