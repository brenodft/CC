# *x     = &p2;
# *p2    = &p1;
# *p1    = &valor;
# *valor = valor;

.data
	x: .word p1
	p1: .word p2
	p2: .word inteiro
	inteiro: .word 2

.text
main:

#carregando memoria
ori $s0,$zero,0x1001
sll $s0,$s0,16

lw $t0, 0($s0)
lw $t1, 4($s0)
lw $t2, 8($s0)
lw $t3, 12($s0)

add $t3,$t3,$t3 
sw $t3, 12($s0)