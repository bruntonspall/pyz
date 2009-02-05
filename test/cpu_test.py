import ztext
import memory
import cpu
import opcodes
import unittest
import logging
import mox
import io
class testOpcodeTranslation(unittest.TestCase):
    def setUp(self):
        self.memory = memory.Memory( [
        0x98, 0xE8, 0x18, 0xE8, 0x98, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory, None, None)
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
        
class testCpuUsesMemory(unittest.TestCase):
    def testCanGetMemory(self):
        mymox = mox.Mox()
        mock_memory = mymox.CreateMock(memory.Memory)
        c = cpu.CPU(mock_memory, None, None)
        mock_memory.get_byte(0x04)
        mymox.ReplayAll()
        c.get_memory(0x04)        
    def testCanSetMemory(self):
        mymox = mox.Mox()
        mock_memory = mymox.CreateMock(memory.Memory)
        c = cpu.CPU(mock_memory, None, None)
        mock_memory.put_byte(0x04, 0x11)
        mymox.ReplayAll()
        c.set_memory(0x04, 0x11)        
class testGameState(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory, None, None)
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
    def testCanReadAndWriteStackVariables(self):
        self.mock_memory.get_2byte(0x06).AndReturn(0x0100)
        self.mymox.ReplayAll()

        self.assertRaises( cpu.StackEmpty, self.cpu.get_variable, 0x00)
        self.cpu.set_variable(0x00, 0x100)
        self.cpu.set_variable(0x00, 0x10)
        self.mymox.VerifyAll()                
        self.assertEquals(0x10,self.cpu.get_variable(0x00))
        self.assertEquals(0x100,self.cpu.get_variable(0x00))
        
    def testInitAndQuit(self):
        self.mock_memory.get_2byte(0x03).AndReturn(0x0100)
        self.mymox.ReplayAll()
        self.assertEquals(cpu.STOPPED, self.cpu.state)
        self.cpu.init()
        self.assertEquals(0x100, self.cpu.get_pc())
        self.assertEquals(cpu.RUNNING, self.cpu.state)
        self.cpu.quit()
        self.assertEquals(cpu.STOPPED, self.cpu.state)
        
class testRandom(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.mock_rng = self.mymox.CreateMock(cpu.RNG)
        self.cpu = cpu.CPU(self.mock_memory, self.mock_rng, None)
        self.cpu.set_pc(0x00)
        
    def testCanGetARandomNumber(self):
        self.mock_rng.random(5).AndReturn(3)
        self.mock_rng.random(5).AndReturn(1)
        self.mymox.ReplayAll()
        self.assertEquals(3,self.cpu.generate_random(5))
        self.assertEquals(1,self.cpu.generate_random(5))
    
    def testCanSeedTheRNG(self):
        self.mock_rng.seed(71)
        self.mymox.ReplayAll()
        self.cpu.generate_random(-71)    

    def testSeedOfLessThan1000GeneratesSequential(self):
        self.cpu = cpu.CPU(self.mock_memory)
        self.cpu.generate_random(-5)
        self.assertEquals(1, self.cpu.generate_random(5))
        self.assertEquals(2, self.cpu.generate_random(5))
        self.assertEquals(3, self.cpu.generate_random(5))
        self.assertEquals(4, self.cpu.generate_random(5))
        self.assertEquals(5, self.cpu.generate_random(5))
        self.assertEquals(1, self.cpu.generate_random(5))
        
    def testSeedOfGreaterThan1000GeneratesRandom(self):
        self.cpu = cpu.CPU(self.mock_memory)
        self.cpu.generate_random(-1001)
        val = self.cpu.generate_random(5)
        self.assertTrue(val >= 1 and val <= 5 )
        
        
class testRoutines(unittest.TestCase):
    def setUp(self):
        self.mymox = mox.Mox()
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory, None, None)
        self.mock_memory.get_2byte(0x03).AndReturn(0x00) # op A0
        
    def testCanCallToAnotherRoutineAndReturn(self):
        # call 1s with 1OP
        self.mock_memory.get_high_byte(0x00).AndReturn(0x88) # op A0
        self.mock_memory.get_high_byte(0x01).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0x10) # operand 1 - 0x0010
        self.mock_memory.get_high_byte(0x03).AndReturn(0x00) # Store on stack
        self.mock_memory.get_high_byte(0x40).AndReturn(0x00) # Function Header - no local variables
        
        self.mock_memory.get_high_byte(0x41).AndReturn(0x9B) # ret 1 value (small)
        self.mock_memory.get_high_byte(0x42).AndReturn(0x42) # value to return
        self.mock_memory.get_2byte(0x06).AndReturn(0x100) # get memory offset for variables
            
        self.mymox.ReplayAll()
        self.cpu.init()
        self.cpu.step()
        
        self.assertEquals(0x41,self.cpu.get_pc())
        self.assertEquals(2, len(self.cpu.callstack))
        
        self.cpu.step()
        self.assertEquals(0x04,self.cpu.get_pc())
        self.assertEquals(1, len(self.cpu.callstack))
        self.assertEquals(0x42, self.cpu.get_stack()[0])
        
        self.mymox.VerifyAll()

    def testStackAndLocalsGetSavedWhenCallingToAnotherRoutineAndRestoredUponReturn(self):
        # call 1s with 1OP
        self.mock_memory.get_2byte(0x06).AndReturn(0x100) # get memory offset for variables
        self.mock_memory.get_high_byte(0x00).AndReturn(0x88) # op A0
        self.mock_memory.get_high_byte(0x01).AndReturn(0x00) # operand 1
        self.mock_memory.get_high_byte(0x02).AndReturn(0x10) # operand 1 - 0x0010
        self.mock_memory.get_high_byte(0x03).AndReturn(0x03) # Store in variable 3
        self.mock_memory.get_high_byte(0x40).AndReturn(0x00) # Function Header - no local variables
        
        self.mock_memory.get_high_byte(0x41).AndReturn(0x9B) # ret 1 value (small)
        self.mock_memory.get_high_byte(0x42).AndReturn(0x42) # value to return
            
        self.mymox.ReplayAll()
        self.cpu.init()
        self.cpu.set_variable(1, 8)
        self.assertEquals(8, self.cpu.get_variable(1))
        self.assertEquals(0, self.cpu.get_variable(3))
        self.cpu.step()
        self.assertEquals(0, self.cpu.get_variable(1))
        self.cpu.set_variable(1, 4)
        self.assertEquals(4, self.cpu.get_variable(1))
        self.assertEquals(0, self.cpu.get_variable(3))
        self.cpu.step()
        self.assertEquals(8, self.cpu.get_variable(1))
        self.assertEquals(0x42, self.cpu.get_variable(3))
        
        self.mymox.VerifyAll()
        
    def testRealVMTest(self):
        # This test will execute from the following vm, and it's main routine adds together
        # two numbers, by setting a global variable, then calling an add function with the second
        # variable as a parameter.
        self.memory = memory.Memory( [ ord(b) for b in file('zcode_print.z5').read()] )
        self.cpu = cpu.CPU(self.memory)
        self.cpu.init()

        self.cpu._fetch()
        self.assertEquals(1, len(self.cpu.next_op.operands))
        self.assertEquals(1, len(self.cpu.callstack))
        self.assertEquals(opcodes.op_call_vs.opcode, self.cpu.next_op.opcode)
        self.cpu._execute()
        
        self.cpu._fetch()
        self.assertEquals(0, len(self.cpu.next_op.operands))
        self.assertEquals(opcodes.op_print.opcode, self.cpu.next_op.opcode)
        self.assertEquals(2, len(self.cpu.callstack))
        self.cpu._execute()

        self.cpu._fetch()
        self.assertEquals(2, len(self.cpu.next_op.operands))
        self.assertEquals(opcodes.op_call_2s.opcode, self.cpu.next_op.opcode)
        self.assertEquals(2, len(self.cpu.callstack))
        self.cpu._execute()

        self.cpu._fetch()        
        self.assertEquals(2, len(self.cpu.next_op.operands))
        self.assertEquals(opcodes.op_add.opcode, self.cpu.next_op.opcode)
        self.assertEquals(3, len(self.cpu.callstack))
        
        # Execute the add operation -> results in stack having answer pushed
        self.cpu._execute()
        self.assertEquals(1, len(self.cpu.get_stack()))
        self.assertEquals(8, self.cpu.get_stack()[0])

        #self.cpu._fetch()        
        # Program in main as compiled
        #call_2n      long_2 short_7 -> sp 
        # add x short_1 -> sp
        # ret_popped
        # ret short_2

class IOTest(unittest.TestCase):
    def testCPUHasInputOutputStreams(self):
        self.mymox = mox.Mox()
        self.mock_io = self.mymox.CreateMock(io.IOSystem)
        self.mock_memory = self.mymox.CreateMock(memory.Memory)
        self.cpu = cpu.CPU(self.mock_memory, None, self.mock_io)
        self.mymox.ReplayAll()
        self.assertEquals(self.mock_io, self.cpu.get_io())
        

if __name__ == '__main__':
    unittest.main()
