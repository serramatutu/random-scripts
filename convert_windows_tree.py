"""Convert windows `tree` output into a flat list of file names."""

import sys

from collections import deque

INDENT_MARKER = "---"
DEDENT_MARKER = " "

def main(infile: str, outfile: str):
    curr_path = deque()

    with open(infile, "rb") as file:
        lines = file.read().decode("utf-16").split("\r\n")

    files = []
    for line in lines:
        if INDENT_MARKER in line:
            indent_idx = line.find(INDENT_MARKER)
            curr_path.append(line[indent_idx + len(INDENT_MARKER):])
        elif line.endswith(DEDENT_MARKER): 
            pipe_count = line.count("|") 
            while pipe_count <= len(curr_path) and len(curr_path) > 0:
                curr_path.pop()
        else:
            file_name = line.replace("|", "").replace(" ", "")
            files.append("/".join(curr_path) + "/" + file_name)
    
    with open(outfile, "w") as file:
        file.write("\n".join(files))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])