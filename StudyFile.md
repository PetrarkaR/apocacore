# RISC-V study file

This is a file intended for my documenting of all the various things in RISC, how they work, what I want to implement, all the good stuff.

## RISC-V architecture

It's important to understand there are 4 instruction types
R type for register based ops

31        25 24     20 19     15 14  12 11      7 6            0
+----------+---------+---------+------+---------+-------------+
| funct7   |   rs2   |   rs1   |funct3|   rd    |    opcode   |
+----------+---------+---------+------+---------+-------------+

Thank you claude for the visual.
I type, for ops with immediate values

31                  20 19     15 14  12 11      7 6            0
+---------------------+---------+------+---------+-------------+
| immediate[11:0]     |   rs1   |funct3|   rd    |    opcode   |
+---------------------+---------+------+---------+-------------+

S type for operations for storing

31        25 24     20 19     15 14  12 11      7 6            0
+----------+---------+---------+------+---------+-------------+
| imm[11:5]|   rs2   |   rs1   |funct3|imm[4:0] |    opcode   |
+----------+---------+---------+------+---------+-------------+

B type for branching

31        25 24     20 19     15 14  12 11      7 6            0
+----------+---------+---------+------+---------+-------------+
|imm[12|10:5]| rs2   |   rs1   |funct3|imm[4:1|11]|  opcode   |
+----------+---------+---------+------+---------+-------------+

U-type for upper immediates, not really sure what these are for yet

31                                  12 11      7 6            0
+-------------------------------------+---------+-------------+
| immediate[31:12]                    |   rd    |    opcode   |
+-------------------------------------+---------+-------------+

J-type for jumping 

31        30      21 20    19        12 11      7 6            0
+----------+----------+------+----------+---------+-------------+
|imm[20]   |imm[10:1] |imm[11]|imm[19:12]|   rd    |    opcode   |
+----------+----------+------+----------+---------+-------------+


I think we will mostly be working with the first 4 types. 
We should have 32 registers but I reduced it to 16 to make it easier to work with, X0 is always bound to be all 0s, with PC as its own special register as well. X1 is by standard used for holding the return address for a call with X5 being available as an alternate link register. X2 is the stack pointer.