import cpu
import memory
import unittest
import opcodes
import mox

class testActualZFile(unittest.TestCase):
    def testExecutesAndPrints(self):
        mymox = mox.Mox()
        rng = mymox.CreateMock(cpu.RNG)
        self.cpu = cpu.CPU(memory.Memory([ ord(b) for b in file('branch.z5').read()]), rng)
        rng.random(5).AndReturn(1)
        mymox.ReplayAll()
        self.cpu.init()
        op = None
        c = 0
        while op.__class__ != opcodes.op_quit and c < 50:
            self.cpu._fetch()
            op = self.cpu.next_op.op
            self.cpu.print_state()
            c += 1
            self.cpu._execute()
if __name__ == '__main__':
    unittest.main()