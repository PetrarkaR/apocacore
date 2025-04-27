# apocacore
A RISC-V based processor simulator? I am not really sure what this is. I am not good at this stuff yet. Named after Epiphany, apocalypse-core. 

The idea of this was to get a better understanding of RISC-V processors. Maybe to build something worth looking at too, who knows.

Plan is to build it in python and VHDL(or Verilog???), I will document it, maybe record youtube videos too. Educational hopefully.

It is modelled to be like George Hotz's work. I hope I can be as half as great as him.

All the processes behind the thinking can be found in the `StudyFile.md`
## Things to implement

- Assembly language parser so that we don't have to input machine code
- Implement instructions like AVX (RVV for RISC??), basically extend ISA
- Pipelining
- Branch prediction
- Cache
- Refactor code to be human readable
- Maybe implement the stack?