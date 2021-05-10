import pickle
from tabulate import tabulate

with open('rom.pic', 'rb') as f:
    data = pickle.load(f)
    instructions = data[0]
    labels = data[1]

registers = {
    'r1': '0x0000',
    'r2': '0x0000',
    'r3': '0x0000',
    'r4': '0x0000',
    'r5': '0x0000',
    'r6': '0x0000',
    'r7': '0x0000',
    'p1': '0x0000',
    'x1': '0x0000',
    'y1': '0x0000',
    'cm': '0x0000',
}

# init disp
disp = []

for i in range(0, 4):
    disp.append([])
    for x in range(0, 4):
        disp[i].append(' ')


# print display
def printdisp(disp):
    print(tabulate(disp))


def addhex(hexdat, value):
    intdat = int(hexdat, 16)
    intdat = intdat + int(value, 16)
    return hex(intdat)


def toint(hexdat):
    return int(hexdat, 16)


def printreg():
    if toint(registers['p1']) != 0:
        print(chr(toint(registers['p1'])), end='')
    else:
        print()


def subhex(hexdat, value):
    intdat = int(hexdat, 16)
    intdat = intdat - int(value, 16)
    return hex(intdat)


cmpstore = False


def runtok(tok):
    com = tok[0]
    reg = tok[1]
    dat = tok[2]

    if com == 'store':
        registers[reg] = registers[dat]

    if com == 'load':
        registers[reg] = dat

    if com == 'add':
        registers[reg] = addhex(registers[reg], dat)

    if com == 'sub':
        registers[reg] = subhex(registers[reg], dat)

    if com == 'prt':
        printreg()

    if com == 'scrn':
        y = int(toint(registers['x1']))
        x = int(toint(registers['y1']))

        disp[x][y] = 'X' if dat == "0xffff" else " "

    if com == 'drw':
        printdisp(disp)

    if com == 'branch':
        pointer = 0
        if registers['cm'] == reg:
            pointer = labels[dat]
            return pointer
        else:
          pass

    if com == 'nbranch':
        pointer = 0
        if not registers['cm'] == reg:
            pointer = labels[dat]
            return pointer
        else:
          pass

    if com == 'cmp':
      val1 = int(toint(registers[reg]))
      val2 = int(toint(registers[dat]))
      if val1 > val2:
        registers['cm'] = '0x0001'
      elif val1 < val2:
        registers['cm'] = '0x0000'
      else:
        registers['cm'] = '0xffff'

global pointer
pointer = 0
while pointer != len(instructions):
    lpoint = pointer
    val = runtok(instructions[lpoint])
    if val == None:
      pointer += 1
    else:
      pointer = val
    
    #print(pointer)
    
print(tabulate(zip(registers.keys(), registers.values())))
