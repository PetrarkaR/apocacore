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

So after a long night of thinking and failing to implement V type instructions for vectors, Ive wanted to re-do my approach to them and I decided I will need a bit more studying, I was thinking to do something like this -> implement the Vector store first, but im not really sure if vector should be the Opcode or what, I gotta think about that still. This is gonna be the hardest part I assume, just thinking about the architecture of the vector instructions. but ill get it down



Vector ops have been implemented as

Instruction Format (32-bit):
+----------+---------+---------+--------+---------+-----------------+
| funct6   | vm      | rs2     | rs1    | funct3  | rd     | opcode |
| [31:26]  | [25]    | [24:20] | [19:15]| [14:12] | [11:7] | [6:0]  |
+----------+---------+---------+--------+---------+-----------------+
