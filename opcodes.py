import base
import ztext

# forms
FORM_LONG = 0x00
FORM_SHORT = 0x01
FORM_EXTENDED = 0x02
FORM_VARIABLE = 0x03

# Operand Types
COUNT_0OP = 0x01
COUNT_1OP = 0x02
COUNT_2OP = 0x03
COUNT_VAR = 0x04
COUNT_EXT = 0x05

TYPE_LARGE = 0x00
TYPE_SMALL = 0x01
TYPE_VAR = 0x02
TYPE_OMIT = 0x03

#OPCODES
ops = []
for x in range(COUNT_EXT+1):
    ops.append([])
    ops[x] = []
    for y in range(9):
        ops[x].append({})
        
class NotImplemented:
    pass

ALL_VERSIONS = [1,2,3,4,5,6,7,8]
VERSION_4UP = [4,5,6,7,8]
VERSION_5UP = [5,6,7,8]
VERSION_6UP = [6,7,8]
VERSION_PRE5 = [1,2,3,4]

def get_arg_value(op, cpu, arg):
    a = op.operands[arg]
    t = op.optypes[arg]
    if t == TYPE_LARGE or t == TYPE_SMALL:
        return base.number(a)
    return base.number(cpu.get_variable(a))
        
def get_arg(op, cpu, arg):
    a = op.operands[arg]
    return base.number(a)


class op_je:
    opcount = COUNT_2OP
    opcode = 0x01
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x01] = op_je

class op_jl:
    opcount = COUNT_2OP
    opcode = 0x02
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x02] = op_jl

class op_jg:
    opcount = COUNT_2OP
    opcode = 0x03
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x03] = op_jg

class op_dec_chk:
    opcount = COUNT_2OP
    opcode = 0x04
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x04] = op_dec_chk

class op_inc_chk:
    opcount = COUNT_2OP
    opcode = 0x05
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x05] = op_inc_chk

class op_jin:
    opcount = COUNT_2OP
    opcode = 0x06
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x06] = op_jin

class op_test:
    opcount = COUNT_2OP
    opcode = 0x07
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x07] = op_test

class op_or:
    opcount = COUNT_2OP
    opcode = 0x08
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) | get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x08] = op_or

class op_and:
    opcount = COUNT_2OP
    opcode = 0x09
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) & get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x09] = op_and

class op_test_attr:
    opcount = COUNT_2OP
    opcode = 0x0A
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0A] = op_test_attr

class op_set_attr:
    opcount = COUNT_2OP
    opcode = 0x0B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0B] = op_set_attr

class op_clear_attr:
    opcount = COUNT_2OP
    opcode = 0x0C
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0C] = op_clear_attr

class op_store:
    opcount = COUNT_2OP
    opcode = 0x0D
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0D] = op_store

class op_insert_obj:
    opcount = COUNT_2OP
    opcode = 0x0E
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0E] = op_insert_obj

class op_loadw:
    opcount = COUNT_2OP
    opcode = 0x0F
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, cpu.get_memory(get_arg(self, cpu, 0)+(get_arg(self, cpu, 1)*2)))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x0F] = op_loadw

class op_loadb:
    opcount = COUNT_2OP
    opcode = 0x10
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, cpu.get_memory(get_arg(self, cpu, 0)+get_arg(self, cpu, 1)))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x10] = op_loadb

class op_get_prop:
    opcount = COUNT_2OP
    opcode = 0x11
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x11] = op_get_prop

class op_get_prop_addr:
    opcount = COUNT_2OP
    opcode = 0x12
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x12] = op_get_prop_addr

class op_get_next_prop:
    opcount = COUNT_2OP
    opcode = 0x13
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x13] = op_get_next_prop

class op_add:
    opcount = COUNT_2OP
    opcode = 0x14
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        # Add arg1 and arg2, -> store in variable store_loc
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0)+get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x14] = op_add

class op_sub:
    opcount = COUNT_2OP
    opcode = 0x15
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) - get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x15] = op_sub

class op_mul:
    opcount = COUNT_2OP
    opcode = 0x16
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) * get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x16] = op_mul

class op_div:
    opcount = COUNT_2OP
    opcode = 0x17
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) / get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x17] = op_div

class op_mod:
    opcount = COUNT_2OP
    opcode = 0x18
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self,cpu,0) % get_arg_value(self,cpu,1))
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x18] = op_mod

class op_call_2s:
    opcount = COUNT_2OP
    opcode = 0x19
    store = True
    branch = False
    versions = VERSION_4UP
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.call(self.operands[0], [self.operands[1]], lambda r: cpu.set_variable(self.store_loc, r))
for v in VERSION_4UP:
    ops[COUNT_2OP][v][0x19] = op_call_2s

class op_call_2n:
    opcount = COUNT_2OP
    opcode = 0x1A
    store = False
    branch = False
    versions = VERSION_4UP
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.call(self.operands[0], [self.operands[1]], None)
for v in VERSION_4UP:
    ops[COUNT_2OP][v][0x1A] = op_call_2n

class op_set_colour:
    opcount = COUNT_2OP
    opcode = 0x1B
    store = False
    branch = False
    versions = [5]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [5]:
    ops[COUNT_2OP][v][0x1B] = op_set_colour

class op_set_colour6:
    opcount = COUNT_2OP
    opcode = 0x1B
    store = False
    branch = False
    versions = VERSION_6UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_6UP:
    ops[COUNT_2OP][v][0x1B] = op_set_colour6

class op_throw:
    opcount = COUNT_2OP
    opcode = 0x1C
    store = False,False
    branch = VERSION_5UP
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_2OP][v][0x1C] = op_throw

class op_jz:
    opcount = COUNT_1OP
    opcode = 0x00
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x00] = op_jz

class op_get_sibling:
    opcount = COUNT_1OP
    opcode = 0x01
    store = True
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x01] = op_get_sibling

class op_get_child:
    opcount = COUNT_1OP
    opcode = 0x02
    store = True
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x02] = op_get_child

class op_get_parent:
    opcount = COUNT_1OP
    opcode = 0x03
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x03] = op_get_parent

class op_get_prop_len:
    opcount = COUNT_1OP
    opcode = 0x04
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x04] = op_get_prop_len

class op_inc:
    opcount = COUNT_1OP
    opcode = 0x05
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(get_arg(self, cpu, 0), get_arg_value(self,cpu,0)+1)
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x05] = op_inc

class op_dec:
    opcount = COUNT_1OP
    opcode = 0x06
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(get_arg(self, cpu, 0), get_arg_value(self,cpu,0)-1)
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x06] = op_dec

class op_print_addr:
    opcount = COUNT_1OP
    opcode = 0x07
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x07] = op_print_addr

class op_call_1s:
    opcount = COUNT_1OP
    opcode = 0x08
    store = True
    branch = False
    versions = VERSION_4UP
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.call(self.operands[0], (), lambda r: cpu.set_variable(self.store_loc, r))
for v in VERSION_4UP:
    ops[COUNT_1OP][v][0x08] = op_call_1s

class op_remove_obj:
    opcount = COUNT_1OP
    opcode = 0x09
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x09] = op_remove_obj

class op_print_obj:
    opcount = COUNT_1OP
    opcode = 0x0A
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x0A] = op_print_obj

class op_ret:
    opcount = COUNT_1OP
    opcode = 0x0B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.ret(self.operands[0])
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x0B] = op_ret

class op_jump:
    opcount = COUNT_1OP
    opcode = 0x0C
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x0C] = op_jump

class op_print_paddr:
    opcount = COUNT_1OP
    opcode = 0x0D
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x0D] = op_print_paddr

class op_load:
    opcount = COUNT_1OP
    opcode = 0x0E
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, get_arg_value(self, cpu, 0))
for v in ALL_VERSIONS:
    ops[COUNT_1OP][v][0x0E] = op_load

class op_not:
    opcount = COUNT_1OP
    opcode = 0x0F
    store = True
    branch = False
    versions = VERSION_PRE5
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, ~get_arg_value(self, cpu, 0))
for v in VERSION_PRE5:
    ops[COUNT_1OP][v][0x0F] = op_not

class op_call_1n:
    opcount = COUNT_1OP
    opcode = 0x0F
    store = False
    branch = False
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_5UP:
    ops[COUNT_1OP][v][0x0F] = op_call_1n

class op_rtrue:
    opcount = COUNT_0OP
    opcode = 0x00
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x00] = op_rtrue

class op_rfalse:
    opcount = COUNT_0OP
    opcode = 0x01
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x01] = op_rfalse

class op_print:
    opcount = COUNT_0OP
    opcode = 0x02
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.print_line(self.text)
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x02] = op_print

class op_print_ret:
    opcount = COUNT_0OP
    opcode = 0x03
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x03] = op_print_ret

class op_nop:
    opcount = COUNT_0OP
    opcode = 0x04
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x04] = op_nop

class op_save:
    opcount = COUNT_0OP
    opcode = 0x05
    store = False
    branch = True
    versions = [1,2,3]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [1,2,3]:
    ops[COUNT_0OP][v][0x05] = op_save

class op_save4:
    opcount = COUNT_0OP
    opcode = 0x05
    store = False
    branch = True
    versions = [4]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [4]:
    ops[COUNT_0OP][v][0x05] = op_save4

class op_save5:
    opcount = COUNT_0OP
    opcode = 0x05
    store = False
    branch = False,VERSION_5UP
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x05] = op_save5

class op_restore:
    opcount = COUNT_0OP
    opcode = 0x06
    store = False
    branch = True
    versions = [1,2,3]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [1,2,3]:
    ops[COUNT_0OP][v][0x06] = op_restore

class op_restore4:
    opcount = COUNT_0OP
    opcode = 0x06
    store = False
    branch = True
    versions = [4]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [4]:
    ops[COUNT_0OP][v][0x06] = op_restore4

class op_restore5:
    opcount = COUNT_0OP
    opcode = 0x06
    store = False
    branch = False
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_5UP:
    ops[COUNT_0OP][v][0x06] = op_restore5

class op_restart:
    opcount = COUNT_0OP
    opcode = 0x07
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x07] = op_restart

class op_ret_popped:
    opcount = COUNT_0OP
    opcode = 0x08
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x08] = op_ret_popped

class op_pop:
    opcount = COUNT_0OP
    opcode = 0x09
    store = False
    branch = False
    versions = VERSION_PRE5
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_PRE5:
    ops[COUNT_0OP][v][0x09] = op_pop

class op_catch:
    opcount = COUNT_0OP
    opcode = 0x09
    store = True
    branch = False
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_5UP:
    ops[COUNT_0OP][v][0x09] = op_catch

class op_quit:
    opcount = COUNT_0OP
    opcode = 0x0A
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x0A] = op_quit

class op_new_line:
    opcount = COUNT_0OP
    opcode = 0x0B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_0OP][v][0x0B] = op_new_line

class op_show_status:
    opcount = COUNT_0OP
    opcode = 0x0C
    store = False
    branch = False
    versions = [3]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [3]:
    ops[COUNT_0OP][v][0x0C] = op_show_status

class op_show_status4:
    opcount = COUNT_0OP
    opcode = 0x0C
    store = False
    branch = False
    versions = VERSION_4UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_4UP:
    ops[COUNT_0OP][v][0x0C] = op_show_status4

class op_verify:
    opcount = COUNT_0OP
    opcode = 0x0D
    store = False
    branch = True
    versions = [3,4,5,6,7,8]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [3,4,5,6,7,8]:
    ops[COUNT_0OP][v][0x0D] = op_verify

class op_ext:
    opcount = COUNT_0OP
    opcode = 0x0E
    store = False
    branch = False
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_5UP:
    ops[COUNT_0OP][v][0x0E] = op_ext

class op_piracy:
    opcount = COUNT_0OP
    opcode = 0x0F
    store = False
    branch = True
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in VERSION_5UP:
    ops[COUNT_0OP][v][0x0F] = op_piracy

class op_call:
    opcount = COUNT_VAR
    opcode = 0x00
    store = True
    branch = False
    versions = [1,2,3]
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in [1,2,3]:
    ops[COUNT_VAR][v][0x00] = op_call

class op_call_vs:
    opcount = COUNT_VAR
    opcode = 0x00
    store = True
    branch = False
    versions = VERSION_4UP
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.call(self.operands[0],self.operands[1:],lambda r: cpu.set_variable(self.store_loc, r))
for v in VERSION_4UP:
    ops[COUNT_VAR][v][0x00] = op_call_vs

class op_storew:
    opcount = COUNT_VAR
    opcode = 0x01
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x01] = op_storew

class op_storeb:
    opcount = COUNT_VAR
    opcode = 0x02
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x02] = op_storeb

class op_put_prop:
    opcount = COUNT_VAR
    opcode = 0x03
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x03] = op_put_prop

class op_sread:
    opcount = COUNT_VAR
    opcode = 0x04
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x04] = op_sread

class op_sread:
    opcount = COUNT_VAR
    opcode = 0x04
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x04] = op_sread

class op_aread:
    opcount = COUNT_VAR
    opcode = 0x04
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x04] = op_aread

class op_print_char:
    opcount = COUNT_VAR
    opcode = 0x05
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x05] = op_print_char

class op_print_num:
    opcount = COUNT_VAR
    opcode = 0x06
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.print_line("%d" % get_arg_value(self, cpu, 0))
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x06] = op_print_num

class op_random:
    opcount = COUNT_VAR
    opcode = 0x07
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x07] = op_random

class op_push:
    opcount = COUNT_VAR
    opcode = 0x08
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x08] = op_push

class op_pull:
    opcount = COUNT_VAR
    opcode = 0x09
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x09] = op_pull

class op_pull6:
    opcount = COUNT_VAR
    opcode = 0x09
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x09] = op_pull6

class op_split_window:
    opcount = COUNT_VAR
    opcode = 0x0A
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0A] = op_split_window

class op_set_window:
    opcount = COUNT_VAR
    opcode = 0x0B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0B] = op_set_window

class op_ext_NAME2:
    opcount = COUNT_VAR
    opcode = 0x0C
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0C] = op_ext_NAME2

class op_erase_window:
    opcount = COUNT_VAR
    opcode = 0x0D
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0D] = op_erase_window

class op_erase_line:
    opcount = COUNT_VAR
    opcode = 0x0E
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0E] = op_erase_line

class op_erase_line6:
    opcount = COUNT_VAR
    opcode = 0x0E
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0E] = op_erase_line6

class op_set_cursor:
    opcount = COUNT_VAR
    opcode = 0x0F
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0F] = op_set_cursor

class op_set_cursor6:
    opcount = COUNT_VAR
    opcode = 0x0F
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x0F] = op_set_cursor6

class op_get_cursor:
    opcount = COUNT_VAR
    opcode = 0x10
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x10] = op_get_cursor

class op_set_text_style:
    opcount = COUNT_VAR
    opcode = 0x11
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x11] = op_set_text_style

class op_buffer_mode:
    opcount = COUNT_VAR
    opcode = 0x12
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x12] = op_buffer_mode

class op_output_stream:
    opcount = COUNT_VAR
    opcode = 0x13
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x13] = op_output_stream

class op_output_stream5:
    opcount = COUNT_VAR
    opcode = 0x13
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x13] = op_output_stream5

class op_output_stream6:
    opcount = COUNT_VAR
    opcode = 0x13
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x13] = op_output_stream6

class op_input_stream:
    opcount = COUNT_VAR
    opcode = 0x14
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x14] = op_input_stream

class op_sound_effect:
    opcount = COUNT_VAR
    opcode = 0x15
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x15] = op_sound_effect

class op_read_char:
    opcount = COUNT_VAR
    opcode = 0x16
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x16] = op_read_char

class op_scan_table:
    opcount = COUNT_VAR
    opcode = 0x17
    store = True
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x17] = op_scan_table

class op_not5:
    opcount = COUNT_VAR
    opcode = 0x18
    store = True
    branch = False
    versions = VERSION_5UP
    def __init__(self):
        pass
    def execute(self, cpu):
        cpu.set_variable(self.store_loc, ~get_arg_value(self, cpu, 0))
for v in VERSION_5UP:
    ops[COUNT_VAR][v][0x18] = op_not5

class op_call_vn:
    opcount = COUNT_VAR
    opcode = 0x19
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x19] = op_call_vn

class op_call_vn2:
    opcount = COUNT_VAR
    opcode = 0x1A
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1A] = op_call_vn2

class op_tokenise:
    opcount = COUNT_VAR
    opcode = 0x1B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1B] = op_tokenise

class op_encode_text:
    opcount = COUNT_VAR
    opcode = 0x1C
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1C] = op_encode_text

class op_copy_table:
    opcount = COUNT_VAR
    opcode = 0x1D
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1D] = op_copy_table

class op_print_table:
    opcount = COUNT_VAR
    opcode = 0x1E
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1E] = op_print_table

class op_check_arg_count:
    opcount = COUNT_VAR
    opcode = 0x1F
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_VAR][v][0x1F] = op_check_arg_count

class op_ext_save:
    opcount = COUNT_EXT
    opcode = 0x00
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x00] = op_ext_save

class op_ext_restore:
    opcount = COUNT_EXT
    opcode = 0x01
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x01] = op_ext_restore

class op_ext_log_shift:
    opcount = COUNT_EXT
    opcode = 0x02
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x02] = op_ext_log_shift

class op_ext_art_shift:
    opcount = COUNT_EXT
    opcode = 0x03
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x03] = op_ext_art_shift

class op_ext_set_font:
    opcount = COUNT_EXT
    opcode = 0x04
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x04] = op_ext_set_font

class op_ext_draw_picture:
    opcount = COUNT_EXT
    opcode = 0x05
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x05] = op_ext_draw_picture

class op_ext_picture_data:
    opcount = COUNT_EXT
    opcode = 0x06
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x06] = op_ext_picture_data

class op_ext_erase_picture:
    opcount = COUNT_EXT
    opcode = 0x07
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x07] = op_ext_erase_picture

class op_ext_set_margins:
    opcount = COUNT_EXT
    opcode = 0x08
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x08] = op_ext_set_margins

class op_ext_save_undo:
    opcount = COUNT_EXT
    opcode = 0x09
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x09] = op_ext_save_undo

class op_ext_restore_undo:
    opcount = COUNT_EXT
    opcode = 0x0A
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x0A] = op_ext_restore_undo

class op_ext_print_unicode:
    opcount = COUNT_EXT
    opcode = 0x0B
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x0B] = op_ext_print_unicode

class op_ext_check_unicode:
    opcount = COUNT_EXT
    opcode = 0x0C
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x0C] = op_ext_check_unicode

class op_ext_move_window:
    opcount = COUNT_EXT
    opcode = 0x10
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x10] = op_ext_move_window

class op_ext_window_size:
    opcount = COUNT_EXT
    opcode = 0x11
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x11] = op_ext_window_size

class op_ext_window_style:
    opcount = COUNT_EXT
    opcode = 0x12
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x12] = op_ext_window_style

class op_ext_get_wind_prop:
    opcount = COUNT_EXT
    opcode = 0x13
    store = True
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x13] = op_ext_get_wind_prop

class op_ext_scroll_window:
    opcount = COUNT_EXT
    opcode = 0x14
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x14] = op_ext_scroll_window

class op_ext_pop_stack:
    opcount = COUNT_EXT
    opcode = 0x15
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x15] = op_ext_pop_stack

class op_ext_read_mouse:
    opcount = COUNT_EXT
    opcode = 0x16
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x16] = op_ext_read_mouse

class op_ext_mouse_window:
    opcount = COUNT_EXT
    opcode = 0x17
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x17] = op_ext_mouse_window

class op_ext_push_stack:
    opcount = COUNT_EXT
    opcode = 0x18
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x18] = op_ext_push_stack

class op_ext_put_wind_prop:
    opcount = COUNT_EXT
    opcode = 0x19
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x19] = op_ext_put_wind_prop

class op_ext_print_form:
    opcount = COUNT_EXT
    opcode = 0x1A
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x1A] = op_ext_print_form

class op_ext_make_menu:
    opcount = COUNT_EXT
    opcode = 0x1B
    store = False
    branch = True
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x1B] = op_ext_make_menu

class op_ext_picture_table:
    opcount = COUNT_EXT
    opcode = 0x1C
    store = False
    branch = False
    versions = ALL_VERSIONS
    def __init__(self):
        pass
    def execute(self, cpu):
        raise NotImplemented
for v in ALL_VERSIONS:
    ops[COUNT_EXT][v][0x1C] = op_ext_picture_table
