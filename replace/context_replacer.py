import sys
from tempfile import mkstemp
from shutil import move
from os import remove

"""
    Replace text in file with context.
    Usage: for i in $(ls -1 *.txt); do python context_replacer.py "$i"; done

    begin: start looking for in context
    orig: want to replace
    dest: replacement
    context: number of lines of context
    pattern: pattern in context that triggers the replacement
"""


def main():
    print("Replacing patterns in file " + str(sys.argv[1]))
    newline_win = '\r\n'
    newline_unix = '\n'
    newline = None

    # discover the newline type of the file (open in binary mode)
    with open(sys.argv[1], 'rb') as f:
        for index, line in enumerate(f.readlines()):
            if line[-2:] != b'\r\n':
                print("es unix")
                newline = newline_unix
            else:
                print("es win")
                newline = newline_win
            break

    fh, abs_path = mkstemp()
    with open(fh, 'w', newline=newline) as nf:
        with open(sys.argv[1]) as f:
            line = "fake"
            found = False
            context = 3
            context_count = 0
            begin = "mainForm.firstDisclaimer"
            orig = "<visible>true"
            dest = "<visible>false"
            pattern = "<visible>true"
            while line:
                line = f.readline()
                if begin in line:
                    found = True
                    nf.write(line)
                    continue
                if found:
                    context_count += 1
                    if pattern in line:
                        l = line.replace(orig, dest)
                        nf.write(l)
                    else:
                        nf.write(line)
                else:
                    nf.write(line)
                if context_count >= context:
                    context_count = 0
                    found = False
                    # print("position: " + str(position) + " : " + line)
    # Remove original file
    remove(sys.argv[1])
    # Move new file
    move(abs_path, sys.argv[1])


if __name__ == "__main__":
    main()
