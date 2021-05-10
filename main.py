import sys
import re
import pickle
from tabulate import tabulate

labels = {}

args = sys.argv

def findnext(text='.'):
  with open(args[1]) as f:
    lines = f.readlines()

def parselabels(fn):
    linenum = 0

    # read the file
    with open(args[1]) as f:
        # parse labels for each line
        for line in f:
            #clean up lines
            line = line.replace('\n', '').replace('\r', '')
            if line[0] == '#':
                # Note that linenum won't be increased, so the address
                # remains correct
                continue

            if line[0] == '.':
                labels[line[1:]] = linenum
                
            else:
                linenum = linenum + 1


def zerobin(fn):
    with open("rom.bin", "wb") as binary_file:
        binary_file.close()


#write out the binary
def writebin(fn, b):
    with open("rom.bin", "ab") as binary_file:
        binary_file.write(bytearray(b))


# Error checking for args
if len(args) != 2:
    print("Usage: vASM file.asm")
    sys.exit()

parselabels(args[1])

tokens = []

with open(args[1]) as f:
    for line in f:
        if line == '':
            continue
        # Ignore labels
        if line[0] == '.':
            continue

        # Ignore comments
        if line[0] == '#':
            continue

        line = line.replace('\n', '').replace('\r', '')
        tok = re.split(r'[, ]', line)

        if '' in tok:
            tok.remove('')

        # print(str(tok))
        tokens.append(tok)

#print(tabulate(tokens, headers=['comm', 'reg', 'dat']))

parselabels(args[1])
print(labels)
with open("rom.pic", "wb") as f:
    pickle.dump([tokens, labels], f)


