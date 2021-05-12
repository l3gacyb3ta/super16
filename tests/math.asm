# Do some math:
#
load r1 0x0002
load r2 0x0002
mulr r1 r2
#
add r1 0x0030
#
store p1 r1
prt 0x0000 0x0000