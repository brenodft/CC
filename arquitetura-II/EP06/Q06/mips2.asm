.text
.globl main

main:
ori $s0,$zero,0x7FFF # maior numero inteiro possivel em 16bits (x)
ori $t0,$zero,0x493E 
sll $s1,$t0,4 # y
add $t0,$s1,$s1 # 2y
add $t0,$t0, $t0 # 4y
sub $s1,$s0,$t0 # z = x-4y
