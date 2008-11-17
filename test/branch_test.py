import cpu
import memory
import unittest

class testActualZFile(unittest.TestCase):
    def setUp(self):
        self.cpu = cpu.CPU(memory.Memory([ ord(b) for b in file('branch.z5').read()]))
    
    def testExecutesAndPrints(self):
        self.cpu.init()
        self.cpu.step()
        self.cpu.step()
        self.cpu.step()
        self.cpu.step()
        self.cpu.step()
        self.cpu.step()
        self.assertRaises(cpu.EndOfExecution, self.cpu.step)
if __name__ == '__main__':
    unittest.main()