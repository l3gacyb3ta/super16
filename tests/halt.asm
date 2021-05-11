# setup r2 and r2
load r2 0x0005
load r1 0x0001
load p1 0x0000
.top
# Increment r1
add r1 0x0001
halt 0x0000 0x0000
# compare and branch
cmp r1 r2
prt 0x0000 0x0000
nbranch 0x0001 top
#