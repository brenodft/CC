.text
.globl main

main:
ori $8,$0,0x01
ori $8,$8, 0xFFFF
sll $8,$8,16
ori $8,$8, 0xFFFF