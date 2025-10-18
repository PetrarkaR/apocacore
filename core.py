from fileParser import *
from cpu import *

if __name__ == '__main__':
    parser=Parser()
    filename = parser.arguments()
    machine,memory = parser.assemble(filename)
    if(parser.run=='Run'):
      emulator = ApocaCore()
      emulator.load_memory(memory)
      emulator.load_program(machine)
      emulator.run()
      emulator.examine_all_registers()
      emulator.dump_vector_registers()
      emulator.dump_memory(512,64)
      emulator.dump_memory(768,32)