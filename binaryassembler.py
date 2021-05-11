import sys
import re

labels = {}

def parselabels(fn):
    linenum = 0
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.replace('\n', '').replace('\r', '')
            if len(line) == 0:
                continue
            if line[0] == '#':
                # Note that linenum won't be increased, so the address
                # remains correct
                continue

            if line[0] == '.':
                labels[line[1:]] = linenum * 4
                print("Label: " + line[1:] + " @ " +
                      format(linenum * 4, '#04x'))

            else:
                linenum = linenum + 1

def zerobin(fn):
    with open("rom.bin", "wb") as binary_file:
        binary_file.close()


def writebin(fn, b):
    with open("rom.bin", "ab") as binary_file:
        binary_file.write(bytearray(b))


if len(sys.argv) != 2:
    print("Usage: vASM file.asm")

    sys.exit()

zerobin("rom.bin")

parselabels(sys.argv[1])

with open(sys.argv[1]) as f:
    for line in f:

        # Ignore labels
        if line[0] == '.':
            continue

        # Ignore comments
        if line[0] == '#':
            continue

        line = line.replace('\n', '').replace('\r', '')

        if len(line) == 0:
                continue

        tok = re.split(r'[, ]', line)

        if '' in tok:
            tok.remove('')

        print(str(tok))

        if tok[0].lower() == "load":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                if a1[0] == '$':
                    # Address
                    addr = int(a1[1:], 0)

                    b = [0x20, r, addr >> 8, addr & 0xFF]
                    writebin("rom.bin", b)

                elif a1[0] == 'r':
                    # register
                    r2 = int(a1[1:], 0)

                    b = [0x20, r, 0, r2]
                    writebin("rom.bin", b)

                else:
                    # Value
                    v = int(a1, 0)

                    b = [0x20, r, v >> 8, v & 0xFF]
                    writebin("rom.bin", b)

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "store":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                if a1[0] == '$':
                    # Address
                    addr = int(a1[1:], 0)

                    b = [0x10, r, addr >> 8, addr & 0xFF]
                    writebin("rom.bin", b)

                elif a1[0] == 'r':
                    # Address in register
                    r2 = int(a1[1:], 0)

                    b = [0x11, r, 0, r2]
                    writebin("rom.bin", b)

                else:
                    print("Invalid mode")

                    print(line)

                    sys.exit()

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        
        elif tok[0].lower() == "cmp":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                if a1[0] == 'r':
                    # register
                    r2 = int(a1[1:], 0)

                    b = [0xf0, r, 0, r2]
                    writebin("rom.bin", b)

                else:
                    # Value
                    v = int(a1, 0)

                    b = [0xf1, r, v >> 8, v & 0xFF]
                    writebin("rom.bin", b)

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "branch":
            if tok[1] in labels:
                addr = labels[tok[1]]
                v = addr
                b = [0xb0, 0, v >> 8, v & 0xFF]
                writebin("rom.bin", b)

            else:
                print("Unknown label")

                print(tok[1])

                sys.exit()

              
        elif tok[0].lower() == "nbranch":
            if tok[1] in labels:
                addr = labels[tok[1]]
                v = addr
                b = [0xb1, 0, v >> 8, v & 0xFF]
                writebin("rom.bin", b)

            else:
                print("Unknown label")

                print(tok[1])

                sys.exit()

        elif tok[0].lower() == "add":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # Value
                v = int(a1, 0)

                b = [0x30, r, v >> 8, v & 0xFF]
                writebin("rom.bin", b)

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "addr":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # register
                r2 = int(a1[1:], 0)

                b = [0x31, r, 0, r2]
                writebin("rom.bin", b)


            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "sub":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # Value
                v = int(a1, 0)

                b = [0x30, r, v >> 8, v & 0xFF]
                writebin("rom.bin", b)

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "subr":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # register
                r2 = int(a1[1:], 0)

                b = [0x31, r, 0, r2]
                writebin("rom.bin", b)


            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()
                
        elif tok[0].lower() == "addr":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # register
                r2 = int(a1[1:], 0)

                b = [0x31, r, 0, r2]
                writebin("rom.bin", b)


            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "mul":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # Value
                v = int(a1, 0)

                b = [0x50, r, v >> 8, v & 0xFF]
                writebin("rom.bin", b)

            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "mulr":
            r = int(tok[1].lower()[1])

            if r >= 0 and r <= 7:
                a1 = tok[2]
                # register
                r2 = int(a1[1:], 0)

                b = [0x51, r, 0, r2]
                writebin("rom.bin", b)


            else:
                print("Invalid register name")

                print(tok[1].lower())

                sys.exit()

        elif tok[0].lower() == "halt":
            b = [0xFE, 0x00, 0x00, 0x00]
            writebin("rom.bin", b)

        elif tok[0].lower() == "noop":
            b = [0x00, 0x00, 0x00, 0x00]
            writebin("rom.bin", b)

        elif tok[0].lower() == "drw":
            b = [0xdd, 0x00, 0xdd, 0x00]
            writebin("rom.bin", b)
        
        elif tok[0].lower() == "prt":
            b = [0x99, 0x00, 0x99, 0x00]
            writebin("rom.bin", b)

        else:
            print("Unknown operand")

            print(tok[0])

            sys.exit()

