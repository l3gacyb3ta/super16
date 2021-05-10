# setup r2 and r2
load r2 0x0005
load r1 0x0001
# setup h
load p1 0x0068
.top
# Print h
prt 0x0000 0x0000
# Increment r1
add r1 0x0001
# compare and branch
cmp r1 r2
nbranch 0x0001 top
#
# if it's done, write an g
load p1 0x0067
prt 0x0000 0x0000