import opcodes

def decode_type_byte(b):
    args = []
    for x in range(4):
        args.append(b&0x03)
        b = b >> 2
    args.reverse()
    return args
        
class Op:
    def __init__(self, cpu):
        code = cpu._get_next_pc_byte()
        print "Translating code 0x%02x" % (code)
        self.operands = []
        self.optypes = []
        self.op = None
        if code == 0xBE and cpu.version >= 5:
            self.form = opcodes.FORM_EXTENDED
            self.op_count = opcodes.COUNT_VAR
            self.opcode = cpu._get_next_pc_byte()
            self._parse_var_args(cpu)
        elif (code & 0xC0) == 0xC0:
            self.form = opcodes.FORM_VARIABLE
            if (code & 0x10) == 0x10:
                self.op_count = opcodes.COUNT_VAR
                self._parse_var_args(cpu)
            else:
                self.op_count = opcodes.COUNT_2OP
                self._parse_var_args(cpu)
            self.opcode = code &0x1F
        elif (code & 0x80) == 0x80:
            self.form = opcodes.FORM_SHORT
            if (code & 0x30) == 0x30:
                self.op_count = opcodes.COUNT_0OP
                self.optypes.append(opcodes.TYPE_OMIT)
            else:
                self.op_count = opcodes.COUNT_1OP
                self.optypes.append((code & (opcodes.TYPE_OMIT << 4)) >> 4)
                if self.optypes[0] == opcodes.TYPE_LARGE:
                    self.operands.append(cpu._get_next_pc_2byte())
                else:
                    self.operands.append(cpu._get_next_pc_byte())
                
            self.opcode = code & 0x0F
        else:
            self.form = opcodes.FORM_LONG
            self.op_count = opcodes.COUNT_2OP
            if (code & 0x40) == 0x40:
                self.optypes.append(opcodes.TYPE_VAR)
            else:
                self.optypes.append(opcodes.TYPE_SMALL)
            if (code & 0x20) == 0x20:
                self.optypes.append(opcodes.TYPE_VAR)
            else:
                self.optypes.append(opcodes.TYPE_SMALL)
            self.operands.append(cpu._get_next_pc_byte())
            self.operands.append(cpu._get_next_pc_byte())
                
            self.opcode = code & 0x1F
        print "Loading op [0x%02x][0x%02x][0x%02x]" % (self.op_count, cpu.version, self.opcode)
        self.op = opcodes.ops[self.op_count][cpu.version][self.opcode]
        if self.op.store:
            self.store = cpu._get_next_pc_byte()
        
    def __str__(self):
        return "Op 0x%02x (form %s, opcount %s)" % (self.opcode, self.form, self.op_count)
        
    def _parse_var_args(self, cpu):
        args = decode_type_byte(cpu._get_next_pc_byte())
        for a in args:
            self.optypes.append(a)
            if a == opcodes.TYPE_LARGE:
                self.operands.append(cpu._get_next_pc_2byte())
            elif a == opcodes.TYPE_VAR or a == opcodes.TYPE_SMALL:
                self.operands.append(cpu._get_next_pc_byte())


class CPU:
    def __init__(self, memory):
        self.memory = memory
        self.stack = []
        self.pc = 0x00
        self.version = 0x05
        self.var_start = None
        
    def init(self):
        # Sets up the state of the VM from memory
        self.set_pc(self.memory.get_2byte(0x03))
        self.stack = []
        self.callstack = []
        self.version = 0x05
        self.next_op = self.get_next_op()
        
    def _fetch(self):
        self.next_op = self.get_next_op()
    def _execute(self):
        pass
    def step(self):
        self._fetch()
        self._execute()
        
    def set_pc(self, pc):
        self.pc = pc
        
    def get_pc(self):
        return self.pc
    
    def _get_next_pc_2byte(self):
        self.pc += 2
        return (self.memory.get_high_byte(self.pc-2) << 8) + self.memory.get_high_byte(self.pc-1)
        
    def _get_next_pc_byte(self):
        self.pc += 1
        return self.memory.get_high_byte(self.pc-1)
        
    def get_next_op(self):
        return Op(self)
        
    def get_variable(self, var):
        if self.var_start == None:
            self.var_start = self.memory.get_2byte(0x06)        
        if var > 0x0F:
            return self.memory.get_2byte(self.var_start + var - 0x10)
        if var == 0:
            if len(self.stack) == 0:
                raise StackEmpty
            return self.stack.pop()
            
    def set_variable(self, var, value):
        if self.var_start == None:
            self.var_start = self.memory.get_2byte(0x06)        
        if var > 0x0F:
            return self.memory.put_2byte(self.var_start + var - 0x10, value)
        if var == 00:
            self.stack.append(value)
            
    def call(self, addr):
        loc = self.memory._calc_location_p(addr)
        args = self.memory.get_high_byte(loc)
        self.set_pc(loc+1)
        

class StackEmpty(Exception):
    pass
