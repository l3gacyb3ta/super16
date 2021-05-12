from tabulate import tabulate
import pickle

with open('rom.pic', 'rb') as f:
    data = pickle.load(f)
    instructions = data[0]
    labels = data[1]


def cleanregs(registers):
    for reg in registers.keys():
        dat = registers[reg]
        if len(dat) > 5:
            dat = dat[:6]

        if len(dat) < 6:
            dat = dat.replace('0x', '')
            datlen = len(dat)
            dat = '0x' + '0' * (4 - datlen) + str(dat)

        registers[reg] = dat

    return registers


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


def subhex(hexdat, value):
    intdat = int(hexdat, 16)
    intdat = intdat - int(value, 16)
    return hex(intdat)


def mulhex(hexdat, value):
    intdat = int(hexdat, 16)
    intdat = intdat * int(value, 16)
    return hex(intdat)


def toint(hexdat):
    return int(hexdat, 16)


def printreg():
    if toint(registers['p1']) != 0:
        print(chr(toint(registers['p1'])), end='')
    else:
        print()


cmpstore = False


def runtok(tok):
    try:
        len(tok[0])

    except:
        return None

    com = tok[0]
    reg = tok[1]
    dat = tok[2]

    if com == 'store':
        registers[reg] = registers[dat]

    if com == 'load':
        registers[reg] = dat

    if com == 'add':
        registers[reg] = addhex(registers[reg], dat)

    if com == 'addr':
        first = int(toint(registers[reg]))
        second = int(toint(registers[dat]))

        registers[reg] = hex(first + second)

    if com == 'sub':
        registers[reg] = subhex(registers[reg], dat)

    if com == 'subr':
        first = int(toint(registers[reg]))
        second = int(toint(registers[dat]))

        registers[reg] = hex(first - second)

    if com == 'mul':
        registers[reg] = subhex(registers[reg], dat)

    if com == 'mulr':
        first = int(toint(registers[reg]))
        second = int(toint(registers[dat]))

        registers[reg] = hex(first * second)

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

    if com == 'log':
        print(registers[reg])

    if com == 'noop':
        pass

    if com == 'jump':
        return labels[reg]

    if com == 'halt':
        exit()


global pointer
pointer = 0

while pointer != len(instructions):
    lpoint = pointer
    val = runtok(instructions[lpoint])

    if val == None:
        pointer += 1

    else:
        pointer = val

    registers = cleanregs(registers)
    print(tabulate(zip(registers.keys(), registers.values())))
    input()

    # print(pointer)


