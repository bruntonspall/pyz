import opcodes
import unittest
import cpu
import mox
import ztext
from base import number

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

    def test_op_dec(self):
        op = opcodes.op_dec()
        op.operands = [0x01]
        op.optypes = [opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.cpu.get_variable(0x01).AndReturn(-2)
        self.cpu.set_variable(0x01, -3)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_load(self):
        op = opcodes.op_load()
        op.operands = [0x01]
        op.optypes = [opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.cpu.get_variable(0x01).AndReturn(6)
        self.cpu.set_variable(0x00, 6)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_not(self):
        op = opcodes.op_not()
        op.operands = [0x0F]
        op.optypes = [opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, number(0xFFF0))

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_not5(self):
        op = opcodes.op_not5()
        op.operands = [0x0F]
        op.optypes = [opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.cpu.set_variable(0x00, number(0xFFF0))

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_loadb(self):
        op = opcodes.op_loadb()
        op.operands = [0x10, 0x05]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_LARGE]
        op.store_loc = 0x00

        self.cpu.get_memory(0x15).AndReturn(0x01)
        self.cpu.set_variable(0x00, number(0x01))

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_loadw(self):
        op = opcodes.op_loadw()
        op.operands = [0x10, 0x05]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_LARGE]
        op.store_loc = 0x00

        self.cpu.get_memory(0x1A).AndReturn(0x01)
        self.cpu.set_variable(0x00, number(0x01))

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_print(self):
        op = opcodes.op_print()
        op.text = ztext.to_bytes(ztext.from_zscii("This is a test"))

        self.cpu.print_line(op.text)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    

if __name__ == '__main__':
    unittest.main()