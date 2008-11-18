import src.cpu as cpu
import src.memory as memory

if __name__ == '__main__':
  import sys
  c = cpu.CPU(memory.Memory([ ord(b) for b in file(sys.argv[1]).read()]))
  c.init()
  while c.state:
    c.debug_step()
