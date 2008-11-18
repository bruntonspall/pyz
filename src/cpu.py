import opcodes
import ztext
import random
from base import number

# States
STOPPED = 0
RUNNING = 1

class RNG:
    RANDOM = 0
    SEQUENTIAL = 1
    def __init__(self, seed = 0):
        self.rng = random.Random()
        self.seed(seed)
    def seed(self, seed):
        if seed > 1000:
            self.rng.seed(seed)
            self.mode = RNG.RANDOM
        if seed == 0:
            self.rng.seed()
            self.mode = RNG.RANDOM
        if seed > 0 and seed <= 1000:
            self.seednum = seed
            self.mode = RNG.SEQUENTIAL
            self.start = 0
        
    def random(self, max):
        if self.mode == RNG.RANDOM:
            return self.rng.randint(1, max)
        else:
            self.start += 1
            self.start %= self.seednum
            return self.start
                
            

def decode_type_byte(b):
    args = []
    for x in range(4):
        args.append(b & 0x03)
        b = b >> 2
    args.reverse()
    return args
        
class Op:
    def __init__(self, cpu):
        self.bytes = []
        code = cpu._get_next_pc_byte()
        self.bytes.append(code)
        self.operands = []
        self.optypes = []
        self.op = None
        if code == 0xBE and cpu.version >= 5:
            self.handle_extended_form(cpu)
        elif (code & 0xC0) == 0xC0:
            self.handle_variable_form(cpu, code)
        elif (code & 0x80) == 0x80:
            self.handle_short_form(cpu, code)
        else:
            self.handle_long_form(cpu, code)
        self.op = opcodes.ops[self.op_count][cpu.version][self.opcode]()
        self.op.operands = self.operands
        self.op.optypes = self.optypes
        self.op.op_count = self.op_count
        self.op.bytes = self.bytes
        if self.op.store:
            self.store = cpu._get_next_pc_byte()
            self.bytes.append(self.store)
            self.op.store_loc = self.store
        if self.op.branch:
            branch = cpu._get_next_pc_byte()
            self.bytes.append(branch)
            self.branch_condition = False
            if branch & 0x80:
                self.branch_condition = True
            if branch & 0x40:
                self.branch = branch & 0x3F
            else:
                b = cpu._get_next_pc_byte()
                self.bytes.append(b)
                self.branch = ((branch & 0x3F) << 8) + b
            self.op.branch_loc = self.branch
            self.op.branch_condition = self.branch_condition

        if code == 0xB2 or code == 0xB3:
            self.handle_inline_text(cpu)
            self.op.text = self.text

    def handle_inline_text(self, cpu):
        self.text = []
        word = 0
        while (word & 0x8000) == 0:
            word = cpu._get_next_pc_2byte()
            self.bytes.append(word >> 8)
            self.bytes.append(word & 0xFF)
            self.text += [(word & 0x7c00) >> 10, (word & 0x03e0) >> 5, word & 0x001f]


    def handle_long_form(self, cpu, code):
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
        b = cpu._get_next_pc_byte()
        self.bytes.append(b)
        self.operands.append(b)
        b = cpu._get_next_pc_byte()
        self.bytes.append(b)
        self.operands.append(b)
        self.opcode = code & 0x1F


    def handle_short_form(self, cpu, code):
        self.form = opcodes.FORM_SHORT
        if (code & 0x30) == 0x30:
            self.op_count = opcodes.COUNT_0OP
            self.optypes.append(opcodes.TYPE_OMIT)
        else:
            self.op_count = opcodes.COUNT_1OP
            self.optypes.append(opcodes.TYPES[(code & (opcodes.TYPE_OMIT << 4)) >> 4])
            if self.optypes[0] == opcodes.TYPE_LARGE:
                word = cpu._get_next_pc_2byte()
                self.bytes.append(word >> 8)
                self.bytes.append(word & 0xFF)
                self.operands.append(word)
            elif self.optypes[0] == opcodes.TYPE_SMALL or self.optypes[0] == opcodes.TYPE_VAR:
                b = cpu._get_next_pc_byte()
                self.bytes.append(b)
                self.operands.append(b)
        self.opcode = code & 0x0F


    def handle_variable_form(self, cpu, code):
        self.form = opcodes.FORM_VARIABLE
        if (code & 0x20) == 0x20:
            self.op_count = opcodes.COUNT_VAR
            self._parse_var_args(cpu)
        else:
            self.op_count = opcodes.COUNT_2OP
            self._parse_var_args(cpu)
        self.opcode = code & 0x1F


    def handle_extended_form(self, cpu):
        self.form = opcodes.FORM_EXTENDED
        self.op_count = opcodes.COUNT_VAR
        b = cpu._get_next_pc_byte()
        self.bytes.append(b)
        self.opcode = b
        self._parse_var_args(cpu)

        
    def __str__(self):
        return "Op 0x%02x (form %s, opcount %s)" % (self.opcode, self.form, self.op_count)
        
    def _parse_var_args(self, cpu):
        b = cpu._get_next_pc_byte()
        self.bytes.append(b)
        args = decode_type_byte(b)
        for a in args:
            self.optypes.append(opcodes.TYPES[a])
            if opcodes.TYPES[a] == opcodes.TYPE_LARGE:
                word = cpu._get_next_pc_2byte()
                self.bytes.append(word >> 8)
                self.bytes.append(word & 0xFF)
                self.operands.append(word)
            elif opcodes.TYPES[a] == opcodes.TYPE_SMALL or opcodes.TYPES[a] == opcodes.TYPE_VAR:
                b = cpu._get_next_pc_byte()
                self.bytes.append(b)
                self.operands.append(b)
    
    def execute(self, cpu):
        self.op.execute(cpu)

class EndOfExecution:
    pass

class ExecutionContext:
    def __init__(self):
        self.stack = []
        self.pc = 0x00
        self.locals = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

class CPU:
    def __init__(self, memory, rng = RNG()):
        self.memory = memory
        self.rng = rng
        self.callstack = []
        self.callstack.append(ExecutionContext())
        self.version = 0x05
        self.var_start = None
        self.state = STOPPED
        
    def init(self):
        # Sets up the state of the VM from memory
        self.callstack = []
        self.callstack.append(ExecutionContext())
        self.set_pc(self.memory.get_2byte(0x03))
        self.version = 0x05
        self.state = RUNNING
        #self.next_op = self.get_next_op()
        
    def quit(self):
        self.print_line(ztext.from_zscii("END OF EXECUTION"))
        self.state = STOPPED

    def _calc_packed_location(self, location):
        mult = 2
        if self.version in [4,5,6,7]: mult = 4
        if self.version == 8: mult = 8
        return location * mult
    
    def set_local(self, num, val):
        self.callstack[0].locals[num] = val
        
    def get_local(self, num):
        return self.callstack[0].locals[num]
        
    def _fetch(self):
        
        if self.state == RUNNING:
            self.next_op = self.get_next_op()
    
    def _execute(self):
        if self.state == RUNNING:
            self.next_op.execute(self)
    
    def step(self):
        self._fetch()
        self._execute()
        
    def call(self, location, args, result):
        context = ExecutionContext()
        self.callstack.insert(0, context)
        self.set_pc(self._calc_packed_location(location))
        num_locals = self._get_next_pc_byte()
        context.on_ret = result
        
        for pos,arg in zip(range(len(args)),args):
            self.set_local(pos+1, arg)
            
        
    def ret(self, value = None):
        old_context = self.callstack.pop(0)
        if old_context.on_ret:
            old_context.on_ret(value)        
        
    def set_pc(self, pc):
        self.callstack[0].pc = pc
        
    def get_pc(self):
        return self.callstack[0].pc
    
    def increment_pc(self, v=1):
        self.callstack[0].pc += v
        
    def get_stack(self):
        return self.callstack[0].stack
        
    def _get_next_pc_2byte(self):
        self.increment_pc(2)
        return (self.memory.get_high_byte(self.get_pc() - 2) << 8) + self.memory.get_high_byte(self.get_pc() - 1)
        
    def _get_next_pc_byte(self):
        self.increment_pc()
        return self.memory.get_high_byte(self.get_pc() - 1)
        
    def get_next_op(self):
        return Op(self)
        
    def get_variable(self, var):
        if self.var_start == None:
            self.var_start = self.memory.get_2byte(0x06)        
        if var > 0x0F:
            return self.memory.get_2byte(self.var_start + var - 0x10)
        if var < 0x10 and var > 0x00:
            return self.get_local(var)
        if var == 0:
            if len(self.get_stack()) == 0:
                raise StackEmpty
            return self.get_stack().pop()
            
    def set_variable(self, var, value):
        if self.var_start == None:
            self.var_start = self.memory.get_2byte(0x06)        
        if var > 0x0F:
            return self.memory.put_2byte(self.var_start + var - 0x10, value)
        if var < 0x10 and var > 0x00:
            return self.set_local(var, value)
        if var == 00:
            self.get_stack().append(value)
            
    def get_memory(self, location):
        return self.memory.get_byte(location)

    def set_memory(self, location, value):
        return self.memory.put_byte(location, value)
    
    def print_line(self, text):
        print ztext.to_zscii(text)
        
    def generate_random(self, max):
        if max <= 0:
            self.rng.seed(max)
        else:
            return self.rng.random(max)
        
    def debug_step(self):
        print "=== CPU STATE ==="
        print "PC: 0x%02x" % (self.get_pc())
        self._fetch()
        print "Next Op: %s" % (self.next_op.op)
        print "Locals: %s" % (self.callstack[0].locals)
        print "Stack: %s" % (self.get_stack())
        print "=== EXECUTE ==="
        self._execute()
        print "Locals: %s" % (self.callstack[0].locals)
        print "Stack: %s" % (self.get_stack())
    def print_state(self):
        print "=== CPU STATE ==="
        print "PC: 0x%02x" % (self.get_pc())
        print "Next Op: %s" % (self.next_op.op)
        print "Locals: %s" % (self.callstack[0].locals)
        print "Stack: %s" % (self.get_stack())
        print "=== END CPU STATE ==="
        

class StackEmpty(Exception):
    pass
