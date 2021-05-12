from tabulate import tabulate
from typing import Union
import pickle
import time

tt0 = time.time()
t0 = time.time()

with open('rom.pic', 'rb') as f:
    data = pickle.load(f)
    instructions = data[0]
    labels = data[1]


def cleanregs(registers):
    '''Cleans up the registers'''
    for reg in registers.keys():
        dat = registers[reg]

        # if the data is to long
        if len(dat) > 5:
            dat = dat[:6]

        # if it is to short
        if len(dat) < 6:
            #remove 0x
            dat = dat.replace('0x', '')
            datlen = len(dat)
            #                   add the right number of zeros
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
    'p0': '0x0000',
    'x8': '0x0000',
    'y9': '0x0000',
    'cm': '0x0000',
}

disp = []

X_VALUE = 5
Y_VALUE = 4

for y in range(0, Y_VALUE):
    disp.append([])
    for x in range(0, X_VALUE):
        disp[y].append(' ')

# print display
def printdisp(disp: list):
    '''Prints out display using tabulate'''
    print(tabulate(disp))


def addhex(hexdat: str, value: str) -> str:
    '''adds a hex to a hex'''
    intdat = int(hexdat, 16)
    intdat = intdat + int(value, 16)
    return hex(intdat)


def subhex(hexdat: str, value: str) -> str:
    '''Subtracts a hex from a hex'''
    intdat = int(hexdat, 16)
    intdat = intdat - int(value, 16)
    return hex(intdat)


def mulhex(hexdat: str, value: str) -> str:
    '''Multiplies a hex by a hex'''
    intdat = int(hexdat, 16)
    intdat = intdat * int(value, 16)
    return hex(intdat)

def divhex(hexdat: str, value: str) -> str:
    '''Divides a hex by a hex'''
    intdat = int(hexdat, 16)
    intdat = intdat // int(value, 16)
    return hex(intdat)

def toint(hexdat: str) -> int:
    '''Converts a hex to an int'''
    return int(hexdat, 16)


def printreg():
    if toint(registers['p0']) != 0:
        print(chr(toint(registers['p0'])), end='')
    else:
        print()


cmpstore = False


def runtok(tok: list) -> Union[None, int]:
    '''Interpret 1 token from a list'''
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
    
    if com == 'div':
        registers[reg] = subhex(registers[reg], dat)

    if com == 'divr':
        first = int(toint(registers[reg]))
        second = int(toint(registers[dat]))

        registers[reg] = hex(first // second)

    if com == 'prt':
        printreg()

    if com == 'scrn':
        y = toint(registers['x8'])
        x = int(toint(registers['y9']))

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

t1 = time.time()

total = t1-t0
# Timestamping
# print("Init: " + str(total))

global pointer
pointer = 0

while pointer != len(instructions):

    t0 = time.time()
    lpoint = pointer
    val = runtok(instructions[lpoint])

    if val == None:
        pointer += 1

    else:
        pointer = val

    registers = cleanregs(registers)

    t1 = time.time()

    total = t1-t0

    # time stamping
    # print("Instruction " + str(lpoint) + ': ' + str(total))

    # print(pointer)

# print out registers
print(tabulate(zip(registers.keys(), registers.values())))

tt1 = time.time()

total = tt1-tt0
print("Total time: " + str(total))