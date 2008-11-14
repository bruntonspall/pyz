import opcodes
import unittest
import cpu
import mox

class testRoutines(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.cpu = self.mymox.CreateMock(cpu.CPU)

    def test_op_or(self):
        op = opcodes.op_or()
        op.operands = [0x03, 0x04]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x07)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_or_var(self):
        op = opcodes.op_or()
        op.operands = [0x00, 0x01]
        op.optypes = [opcodes.TYPE_VAR, opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.cpu.get_variable(0x00).AndReturn(0x06)
        self.cpu.get_variable(0x01).AndReturn(0x04)
        self.cpu.set_variable(0x00, 0x06)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_and(self):
        op = opcodes.op_and()
        op.operands = [0x03, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x01)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_add(self):
        op = opcodes.op_add()
        op.operands = [0x03, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x08)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_sub(self):
        op = opcodes.op_sub()
        op.operands = [0x03, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, -2)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_mul(self):
        op = opcodes.op_mul()
        op.operands = [0x03, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x0F)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_div(self):
        op = opcodes.op_div()
        op.operands = [0x11, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x03)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_mod(self):
        op = opcodes.op_mod()
        op.operands = [0x11, 0x05]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, 0x02)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_inc(self):
        op = opcodes.op_inc()
        op.operands = [0x01]
        op.optypes = [opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.cpu.get_variable(0x01).AndReturn(-1)
        self.cpu.set_variable(0x01, 0x00)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

if __name__ == '__main__':
    unittest.main()