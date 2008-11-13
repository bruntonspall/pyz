import ztext
import memory
import cpu
import opcodes
import unittest
import logging
import mox
class testOpcodeTranslation(unittest.TestCase):
    def setUp(self):
        self.memory = memory.Memory( [
        0x98, 0xE8, 0x18, 0xE8, 0x98, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory)
        self.cpu.set_pc(0x00)
        
        
    # Spec 4.3.1
    # Spec 4.4.1
    def testCanTranslateShortForm(self):
        # Short form if bit 8 is set, i.e. 0x80 and above
        # Opcode is in bits 3-0 (i.e. 0x0F)
        # Type is in bits 5-4 (i.e. 0x30) 
        self.mock_memory.get_high_byte(0x00).AndReturn(0x85) # operation 80
        self.mock_memory.get_high_byte(0x01).AndReturn(0x01) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0x02) # operand 1
        self.mock_memory.get_high_byte(0x03).AndReturn(0x97) # operation 80
        self.mock_memory.get_high_byte(0x04).AndReturn(0x04) # operand 1
        self.mock_memory.get_high_byte(0x05).AndReturn(0xA3) # operation 80
        self.mock_memory.get_high_byte(0x06).AndReturn(0x06) # operand 1
        self.mock_memory.get_high_byte(0x07).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x08).AndReturn(0xB0) # operation 80
        
        self.mymox.ReplayAll()
        # If Type is omitted, count is 0OP, else count is 1OP
        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_SHORT,op.form)
        self.assertEquals(opcodes.COUNT_1OP,op.op_count)
        self.assertEquals(opcodes.TYPE_LARGE,op.optypes[0])
        self.assertEquals(0x05,op.opcode)
        self.assertEquals(0x0102,op.operands[0])
        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_SHORT,op.form)
        self.assertEquals(opcodes.COUNT_1OP,op.op_count)
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[0])
        self.assertEquals(0x07,op.opcode)
        self.assertEquals(0x04,op.operands[0])
        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.COUNT_1OP,op.op_count)
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[0])
        self.assertEquals(0x03,op.opcode)
        self.assertEquals(0x06,op.operands[0])
        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.COUNT_0OP,op.op_count)
        self.assertEquals(opcodes.TYPE_OMIT,op.optypes[0])
        self.assertEquals(0x00,op.opcode)
        
        self.mymox.VerifyAll()                
    # Spec 4.3.2
    # Spec 4.4.2
    def testCanTranslateLongForm(self):
        # Long form is anything with 0x70 and below
        # Opcode is always 0x1F bits (4-0)
        # bit 6 set indicates op1 is variable, not set means small constant
        # bit 5 set indicates op2 is variable, not set means small constant
        self.mock_memory.get_high_byte(0x00).AndReturn(0x73) # operation 80
        self.mock_memory.get_high_byte(0x01).AndReturn(0x01) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0x02) # operand 1
        self.mock_memory.get_high_byte(0x03).AndReturn(0x00) # store
        self.mock_memory.get_high_byte(0x04).AndReturn(0x17) # operation 80
        self.mock_memory.get_high_byte(0x05).AndReturn(0x04) # operand 1
        self.mock_memory.get_high_byte(0x06).AndReturn(0x05) # operand 1
        self.mock_memory.get_high_byte(0x07).AndReturn(0x00) # store
        self.mymox.ReplayAll()

        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_LONG,op.form)
        self.assertEquals(opcodes.COUNT_2OP,op.op_count)
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[0])
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[1])
        self.assertEquals(0x13,op.opcode)
        self.assertEquals(0x01,op.operands[0])
        self.assertEquals(0x02,op.operands[1])

        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_LONG,op.form)
        self.assertEquals(opcodes.COUNT_2OP,op.op_count)
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[0])
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[1])
        self.assertEquals(0x17,op.opcode)
        self.assertEquals(0x04,op.operands[0])
        self.assertEquals(0x05,op.operands[1])

        self.mymox.VerifyAll()                
    
    # Spec 4.3.3
    # Spec 4.4.3
    def testCanTranslateVariableForm(self):
        self.mock_memory.get_high_byte(0x00).AndReturn(0xCB)
        self.mock_memory.get_high_byte(0x01).AndReturn(0x1F) #00011111 (Large, Small, Omit, Omit)
        self.mock_memory.get_high_byte(0x02).AndReturn(0x01)
        self.mock_memory.get_high_byte(0x03).AndReturn(0x02)
        self.mock_memory.get_high_byte(0x04).AndReturn(0x03)
        self.mock_memory.get_high_byte(0x05).AndReturn(0xE1)
        self.mock_memory.get_high_byte(0x06).AndReturn(0x27) #00100111 (Large, Var, Small, Omit)
        self.mock_memory.get_high_byte(0x07).AndReturn(0x07)
        self.mock_memory.get_high_byte(0x08).AndReturn(0x08)
        self.mock_memory.get_high_byte(0x09).AndReturn(0x09)
        self.mock_memory.get_high_byte(0x0A).AndReturn(0x0A)
        self.mymox.ReplayAll()

        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_VARIABLE,  op.form)
        self.assertEquals(opcodes.COUNT_2OP,  op.op_count)
        self.assertEquals(0x0B,  op.opcode)
        self.assertEquals(2, len(op.operands))
        self.assertEquals(opcodes.TYPE_LARGE,op.optypes[0])
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[1])
        self.assertEquals(0x0102,op.operands[0])
        self.assertEquals(0x03,op.operands[1])

        op = self.cpu.get_next_op()
        self.assertEquals(opcodes.FORM_VARIABLE,  op.form)
        self.assertEquals(opcodes.COUNT_VAR,  op.op_count)
        self.assertEquals(0x01,  op.opcode)
        self.assertEquals(3, len(op.operands))
        self.assertEquals(opcodes.TYPE_LARGE,op.optypes[0])
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[1])
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[2])
        self.assertEquals(0x0708,op.operands[0])
        self.assertEquals(0x09,op.operands[1])
        self.assertEquals(0x0A,op.operands[2])

        self.mymox.VerifyAll()                
        
    # Spec 4.3.4
    def testCanTranslateExtendedForm(self):
        self.mock_memory.get_high_byte(0x00).AndReturn(0xBE)
        self.mock_memory.get_high_byte(0x01).AndReturn(0x01)
        self.mock_memory.get_high_byte(0x02).AndReturn(0x27) # Large, Var, Small, Omit
        self.mock_memory.get_high_byte(0x03).AndReturn(0x01)
        self.mock_memory.get_high_byte(0x04).AndReturn(0x02)
        self.mock_memory.get_high_byte(0x05).AndReturn(0x03)
        self.mock_memory.get_high_byte(0x06).AndReturn(0x04)
        self.mymox.ReplayAll()

        op = self.cpu.get_next_op()
        self.mymox.VerifyAll()                
        self.assertEqual(opcodes.COUNT_VAR, op.op_count)
        self.assertEqual(0x01, op.opcode)
        self.assertEquals(3, len(op.operands))
        self.assertEquals(opcodes.TYPE_LARGE,op.optypes[0])
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[1])
        self.assertEquals(opcodes.TYPE_SMALL,op.optypes[2])
        self.assertEquals(0x0102,op.operands[0])
        self.assertEquals(0x03,op.operands[1])
        self.assertEquals(0x04,op.operands[2])
        
    def testUnderstandsStoreOperations(self):
        self.mock_memory.get_high_byte(0x00).AndReturn(0xAE)
        self.mock_memory.get_high_byte(0x01).AndReturn(0x0F)
        self.mock_memory.get_high_byte(0x02).AndReturn(0x00)
        self.mymox.ReplayAll()
        op = self.cpu.get_next_op()
        self.mymox.VerifyAll()                

        self.assertEqual(opcodes.FORM_SHORT, op.form)
        self.assertEqual(opcodes.COUNT_1OP, op.op_count)
        self.assertEqual(opcodes.op_load.opcode, op.opcode)
        self.assertEquals(1, len(op.operands))
        self.assertEquals(opcodes.TYPE_VAR,op.optypes[0])
        self.assertEquals(0x0F,op.operands[0])
        self.assertEquals(0x00,op.store)
    
    def testUnderstandsBranchOperations(self):
        self.mock_memory.get_high_byte(0x00).AndReturn(0xA0) # op A0
        self.mock_memory.get_high_byte(0x01).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0xC0) # Branch if true, 0 offset 
        
        self.mock_memory.get_high_byte(0x03).AndReturn(0xA0) # op A0
        self.mock_memory.get_high_byte(0x04).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x05).AndReturn(0x01) # branch if false, 2 byte offset, 0x100
        self.mock_memory.get_high_byte(0x06).AndReturn(0x00)
        self.mymox.ReplayAll()
        op = self.cpu.get_next_op()
        self.assertEquals(0x00,op.branch)
        self.assertEquals(True,op.branch_condition)

        op = self.cpu.get_next_op()
        self.assertEquals(0x100,op.branch)
        self.assertEquals(False,op.branch_condition)
        self.mymox.VerifyAll()                

    def testUnderstandsTextOpcodes(self):
        self.mock_memory.get_high_byte(0x00).AndReturn(0xB2) # op print
        self.mock_memory.get_high_byte(0x01).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0x00) # branch if false, 2 byte offset, 0x100
        self.mock_memory.get_high_byte(0x03).AndReturn(0x80) # operand 1
        self.mock_memory.get_high_byte(0x04).AndReturn(0x00) # branch if false, 2 byte offset, 0x100
        self.mymox.ReplayAll()
        op = self.cpu.get_next_op()
        self.mymox.VerifyAll()                
        self.assertEquals(0x05, self.cpu.get_pc())
        
        
class testGameState(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory)
        self.cpu.set_pc(0x00)

    # Spec 6.2 Global variables
    def testCanReadAndWriteGlobalVariables(self):
        self.mock_memory.get_2byte(0x06).AndReturn(0x0100)
        self.mock_memory.get_2byte(0x0100).AndReturn(0x0001)
        self.mock_memory.get_2byte(0x0101).AndReturn(0x0002)
        self.mock_memory.put_2byte(0x0101, 0x100)
        self.mymox.ReplayAll()

        self.assertEquals(0x01,self.cpu.get_variable(0x10))
        self.assertEquals(0x02,self.cpu.get_variable(0x11))
        self.cpu.set_variable(0x11, 0x100)
        self.mymox.VerifyAll()                

    # Spec 6.3 The stack
    def testCanReadAndWriteGlobalVariables(self):
        self.mock_memory.get_2byte(0x06).AndReturn(0x0100)
        self.mymox.ReplayAll()

        self.assertRaises( cpu.StackEmpty, self.cpu.get_variable, 0x00)
        self.cpu.set_variable(0x00, 0x100)
        self.cpu.set_variable(0x00, 0x10)
        self.mymox.VerifyAll()                
        self.assertEquals(0x10,self.cpu.get_variable(0x00))
        self.assertEquals(0x100,self.cpu.get_variable(0x00))

class testRoutines(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory)
        self.cpu.set_pc(0x00)
        print "Starting test "+str(self)

        
    def testRealVMTest(self):
        # This test will execute from the following vm, and it's main routine adds together
        # two numbers, by setting a global variable, then calling an add function with the second
        # variable as a parameter.
        import zcode_add
        self.memory = memory.Memory( zcode_add.zcode )
        self.cpu = cpu.CPU(self.memory)
        self.cpu.init()
        # Call internal function to seperate fetch/execute cycle
        self.cpu._fetch()
        self.assertEquals(1, len(self.cpu.next_op.operands))
        self.assertEquals(1, len(self.cpu.callstack))
        self.assertEquals(opcodes.op_call_vs.opcode, self.cpu.next_op.opcode)
        self.cpu._execute()
        
        # Get next instruction... execute should ahve pushed us 1 level down and 
        # jumped to the branch point
        self.cpu._fetch()
        self.assertEquals(2, len(self.cpu.next_op.operands))
        self.assertEquals(opcodes.call_2n, self.cpu.next_op.op_code)
        self.assertEquals(2, len(self.cpu.callstack))
#        self.cpu.step()
#        self.assertEquals(2, len(self.cpu.next_op.operands))
#        self.assertEquals(opcodes.add, self.cpu.next_op.op_code)
#        self.assertEquals(3, len(self.cpu.callstack))
        
        # Program in main as compiled
        #call_2n      long_2 short_7 -> sp 
        # add x_short_1 -> sp
        # ret_popped
        # ret short_2


if __name__ == '__main__':
    unittest.main()
