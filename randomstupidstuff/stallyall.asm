# setup r2 and r2
load r2 0xffff
load r1 0x0001
load p0 0x0000
.top
# Increment r1
add r1 0x0001
noop 0x0000 0x0000
# compare and branch
cmp r1 r2
nbranch 0xffff top
# Runs 0xffff times!