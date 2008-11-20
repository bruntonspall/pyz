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

    def test_can_string_op(self):
        op = opcodes.op_or()
        op.operands = [0x03, 0x04]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00
        op.bytes = [0x00, 0x01]

        self.assertEquals("0x08 -opcodes.op_or (0x03 0x04 ) types ([Small (1), Small (1)]) -> (0) [0x00 0x01 ]", str(op))
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
        
    def test_op_print_num(self):
        op = opcodes.op_print_num()
        op.operands = [0x10]
        op.optypes = [opcodes.TYPE_SMALL]

        self.cpu.print_line([5, 9, 5, 14, 4, 4])

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
    
    def test_op_random(self):
        op = opcodes.op_random()
        op.operands = [0x5]
        op.optypes = [opcodes.TYPE_SMALL]
        op.store_loc = 1
        self.cpu.generate_random(5).AndReturn(4)
        self.cpu.set_variable(1,4)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
    
    def test_op_jump(self):
        op = opcodes.op_jump()
        op.operands = [0xE]
        op.optypes = [opcodes.TYPE_SMALL]
        self.cpu.get_pc().AndReturn(0x00)
        self.cpu.set_pc(0x0C)

        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
    
    def test_op_jg(self):
        op = opcodes.op_jg()
        op.operands = [0x7, 0x4]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.branch_loc = 0x0C
        op.branch_condition = True

        self.mymox.ResetAll()
        # No interactions expected
        self.mymox.ReplayAll()
        op.operands = [0x7, 0x9]
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
        self.mymox.ResetAll()
        self.cpu.get_pc().AndReturn(0x00)
        self.cpu.set_pc(0x0A)
        self.mymox.ReplayAll()
        
        op.operands = [0x7, 0x4]
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
        self.mymox.ResetAll()
        # No interactions expected
        self.mymox.ReplayAll()

        op.branch_condition = False
        op.execute(self.cpu)
        self.mymox.VerifyAll()

        self.mymox.ResetAll()
        self.cpu.get_pc().AndReturn(0x00)
        self.cpu.set_pc(0x0A)
        self.mymox.ReplayAll()

        op.operands = [0x7, 0x9]
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_jg_specials(self):
        op = opcodes.op_jg()
        op.operands = [0x7, 0x4]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.branch_loc = 0x00
        op.branch_condition = True

        self.mymox.ResetAll()
        self.cpu.ret(0)
        self.mymox.ReplayAll()
        op.operands = [0x7, 0x4]
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        self.mymox.ResetAll()
        op.branch_loc = 0x01
        self.cpu.ret(1)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_je(self):
        op = opcodes.op_je()
        op.operands = [0x7, 0x7]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.branch_loc = 0x0C
        op.branch_condition = True

        self.mymox.ResetAll()
        self.cpu.get_pc().AndReturn(0x04)
        self.cpu.set_pc(0x0e)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_jl(self):
        op = opcodes.op_jl()
        op.operands = [0x6, 0x7]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.branch_loc = 0x0C
        op.branch_condition = True

        self.mymox.ResetAll()
        self.cpu.get_pc().AndReturn(0x04)
        self.cpu.set_pc(0x0e)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_jl(self):
        op = opcodes.op_jl()
        op.operands = [0x0, 0x7]
        op.optypes = [opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.branch_loc = 0x0C
        op.branch_condition = True

        self.mymox.ResetAll()
        self.cpu.get_pc().AndReturn(0x04)
        self.cpu.set_pc(0x0e)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_store(self):
        op = opcodes.op_store()
        op.operands = [0x00, 0x02]
        op.optypes = [opcodes.TYPE_VAR, opcodes.TYPE_VAR]

        self.mymox.ResetAll()
        self.cpu.get_variable(0x02).AndReturn(0x04)
        self.cpu.set_variable(0x00, 0x04)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_call_2s(self):
        op = opcodes.op_call_2s()
        op.operands = [0x2c1f, 0x00]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [0], mox.IgnoreArg())
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_call_2n(self):
        op = opcodes.op_call_2n()
        op.operands = [0x2c1f, 0x00]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_VAR]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [0], None)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_call_1s(self):
        op = opcodes.op_call_1s()
        op.operands = [0x2c1f]
        op.optypes = [opcodes.TYPE_LARGE]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [], mox.IgnoreArg())
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_call_vs(self):
        op = opcodes.op_call_vs()
        op.operands = [0x2c1f, 0x00, 0x01]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [0x00, 0x01], mox.IgnoreArg())
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_call_vn(self):
        op = opcodes.op_call_vn()
        op.operands = [0x2c1f, 0x00, 0x01]
        op.optypes = [opcodes.TYPE_LARGE, opcodes.TYPE_SMALL, opcodes.TYPE_SMALL]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [0x00, 0x01], None)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_call_1n(self):
        op = opcodes.op_call_1n()
        op.operands = [0x2c1f]
        op.optypes = [opcodes.TYPE_LARGE]
        op.store_loc = 0x00

        self.mymox.ResetAll()
        self.cpu.call(0x2c1f, [], None)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_ret(self):
        op = opcodes.op_ret()
        op.operands = [0x2]
        op.optypes = [opcodes.TYPE_SMALL]

        self.mymox.ResetAll()
        self.cpu.ret(0x2)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_rtrue(self):
        op = opcodes.op_rtrue()
        self.cpu.ret(1)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_rfalse(self):
        op = opcodes.op_rfalse()
        self.cpu.ret(0)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_ret_popped(self):
        op = opcodes.op_ret_popped()
        self.cpu.get_variable(0).AndReturn(8)
        self.cpu.ret(8)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()

    def test_op_quit(self):
        op = opcodes.op_quit()
        self.cpu.quit()
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_print_num(self):
        op = opcodes.op_print_num()
        op.operands = [0x01]
        op.optypes = [opcodes.TYPE_SMALL]
        self.cpu.print_line(ztext.from_zscii("1"))
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        
    def test_op_pull(self):
        op = opcodes.op_pull()
        op.store_loc = 0x01
        self.cpu.get_variable(0).AndReturn(7)
        self.cpu.set_variable(1, 7)
        self.mymox.ReplayAll()
        op.execute(self.cpu)
        self.mymox.VerifyAll()
        

if __name__ == '__main__':
    unittest.main()