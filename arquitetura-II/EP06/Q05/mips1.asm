.text
.globl main

main:
ori $t0,$zero,0x186A # x = 100000
sll $s0,$t0,4
ori $t1,$zero,0x30D4 # y = 200000
sll $s1,$t1,4
add $s2,$s0,$s1 # z = x+y
