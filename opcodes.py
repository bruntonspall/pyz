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

#2OP
class Operation:
    def __init__(self, count, opcode, store, branch, versions = [1,2,3,4,5,6,7]):
        self.opcode = opcode
        self.store = store
        self.branch = branch
        for v in versions:
            ops[count][v][opcode] = self

VERSION_4UP = [4,5,6,7,8]
VERSION_5UP = [5,6,7,8]
VERSION_6UP = [6,7,8]
VERSION_PRE5 = [1,2,3,4]
        
op_je =         Operation(COUNT_2OP, 0x01, False, True) 
op_jl =         Operation(COUNT_2OP, 0x02, False, True)  
op_jg =         Operation(COUNT_2OP, 0x03, False, True) 
op_dec_chk =    Operation(COUNT_2OP, 0x04, False, True) 
op_inc_chk =    Operation(COUNT_2OP, 0x05, False, True) 
op_jin =        Operation(COUNT_2OP, 0x06, False, True) 
op_test =       Operation(COUNT_2OP, 0x07, False, True) 
op_or =         Operation(COUNT_2OP, 0x08, True, False) 
op_and =        Operation(COUNT_2OP, 0x09, True, False) 
op_test_attr =  Operation(COUNT_2OP, 0x0A, False, True) 
op_set_attr =   Operation(COUNT_2OP, 0x0B, False, False) 
op_clear_attr = Operation(COUNT_2OP, 0x0C, False, True) 
op_store =      Operation(COUNT_2OP, 0x0D, False, False) 
op_insert_obj = Operation(COUNT_2OP, 0x0E, False, False) 
op_loadw =      Operation(COUNT_2OP, 0x0F, True, False) 
op_loadb =      Operation(COUNT_2OP, 0x10, True, False) 
op_get_prop =   Operation(COUNT_2OP, 0x11, True, False) 
op_get_prop_addr = Operation(COUNT_2OP, 0x12, True, False)
op_get_next_prop = Operation(COUNT_2OP, 0x13, True, False)
op_add =        Operation(COUNT_2OP, 0x14, True, False)
op_sub =        Operation(COUNT_2OP, 0x15, True, False)
op_mul =        Operation(COUNT_2OP, 0x16, True, False)
op_div =        Operation(COUNT_2OP, 0x17, True, False)
op_mod =        Operation(COUNT_2OP, 0x18, True, False)
op_call_2s =    Operation(COUNT_2OP, 0x19, True, False, VERSION_4UP)
op_call_2n =    Operation(COUNT_2OP, 0x1A, False,False, VERSION_4UP)
op_set_colour = Operation(COUNT_2OP, 0x1B, False,False, [5])
op_set_colour6 = Operation(COUNT_2OP, 0x1B, False,False, VERSION_6UP)
op_throw = Operation(COUNT_2OP, 0x1C, False,False, VERSION_5UP)

                  
op_jz =         Operation(COUNT_1OP, 0x00, False, True)
op_get_sibling = Operation(COUNT_1OP, 0x01, True, True)
op_get_child =  Operation(COUNT_1OP, 0x02, True, True)
op_get_parent = Operation(COUNT_1OP, 0x03, True, False)
op_get_prop_len = Operation(COUNT_1OP, 0x04, True, False)
op_inc =        Operation(COUNT_1OP, 0x05, False,False)
op_dec =        Operation(COUNT_1OP, 0x06, False,False)
op_print_addr = Operation(COUNT_1OP, 0x07, False,False)
op_call_1s =    Operation(COUNT_1OP, 0x08, True,False, VERSION_4UP)
op_remove_obj = Operation(COUNT_1OP, 0x09, False,False)
op_print_obj =  Operation(COUNT_1OP, 0x0A, False,False)
op_ret =        Operation(COUNT_1OP, 0x0B, False,False)
op_jump =       Operation(COUNT_1OP, 0x0C, False,False)
op_print_paddr = Operation(COUNT_1OP, 0x0D, False,False)
op_load =       Operation(COUNT_1OP, 0x0E, True,False)
op_not =        Operation(COUNT_1OP, 0x0F, True,False, VERSION_PRE5)
#Version 5 and above only... how to represent?
op_call_1n =    Operation(COUNT_1OP, 0x0F, False,False, VERSION_5UP)

# 0OP operations
op_rtrue =          Operation(COUNT_0OP, 0x00, False, False)#    0OP:176 0       rtrue
op_rfalse =         Operation(COUNT_0OP, 0x01, False, False)#    0OP:177 1       rfalse
op_print =          Operation(COUNT_0OP, 0x02, False, False)#    0OP:178 2       print (literal-string)
op_print_ret =      Operation(COUNT_0OP, 0x03, False, False)#    0OP:179 3       print_ret (literal-string)
op_nop =            Operation(COUNT_0OP, 0x04, False, False)#    0OP:180 4   1/- nop
op_save =           Operation(COUNT_0OP, 0x05, False, True, [1,2,3])#  * 0OP:181 5    1  save ?(label)
op_save4 =           Operation(COUNT_0OP, 0x05, False, True, [4])#                 4  save -> (result)
op_save5 =           Operation(COUNT_0OP, 0x05, False, False,VERSION_5UP)#                 5  [illegal]
op_restore =        Operation(COUNT_0OP, 0x06, False, True, [1,2,3])#  * 0OP:182 6    1  restore ?(label)
op_restore4 =        Operation(COUNT_0OP, 0x06, False, True, [4])#                 4  restore -> (result)
op_restore5 =        Operation(COUNT_0OP, 0x06, False, False, VERSION_5UP)#                 5  [illegal]
op_restart =        Operation(COUNT_0OP, 0x07, False, False)#    0OP:183 7       restart
op_ret_popped =     Operation(COUNT_0OP, 0x08, False, False)#    0OP:184 8       ret_popped
op_pop =            Operation(COUNT_0OP, 0x09, False, False, VERSION_PRE5)#    0OP:185 9    1  pop
op_catch =          Operation(COUNT_0OP, 0x09, True, False, VERSION_5UP)#*               5/6 catch -> (result)
op_quit =           Operation(COUNT_0OP, 0x0A, False, False)#    0OP:186 A       quit
op_new_line =       Operation(COUNT_0OP, 0x0B, False, False)#    0OP:187 B       new_line
op_show_status =    Operation(COUNT_0OP, 0x0C, False, False, [3])#    0OP:188 C    3  show_status
op_show_status4 =    Operation(COUNT_0OP, 0x0C, False, False, VERSION_4UP)#                 4  [illegal]
op_verify =         Operation(COUNT_0OP, 0x0D, False, True, [3,4,5,6,7,8])#  * 0OP:189 D    3  verify ?(label)
op_ext =            Operation(COUNT_0OP, 0x0E, False, False, VERSION_5UP)#    0OP:190 E    5  [first byte of extended opcode]
op_piracy =         Operation(COUNT_0OP, 0x0F, False, True, VERSION_5UP)#  * 0OP:191 F   5/- piracy ?(label)

# VAR op calls
#
#St Br Opcode Hex  V Inform name and syntax
op_call = Operation(COUNT_VAR, 0x00, True,False, [1,2,3])
op_call_vs = Operation(COUNT_VAR, 0x00, True,False, VERSION_4UP)
op_storew  = Operation(COUNT_VAR, 0x01, False, False)#      VAR:225 1      storew array word-index value
op_storeb  = Operation(COUNT_VAR, 0x02, False, False)#      VAR:226 2      storeb array byte-index value
op_put_prop = Operation(COUNT_VAR, 0x03, False, False)#      VAR:227 3      put_prop object property value
op_sread   = Operation(COUNT_VAR, 0x04, False, False)#      VAR:228 4   1 sread text parse
op_sread = Operation(COUNT_VAR, 0x04, False, False)#                  4 sread text parse time routine
op_aread = Operation(COUNT_VAR, 0x04, True , False)#*                 5 aread text parse time routine -> (result)
op_print_char = Operation(COUNT_VAR, 0x05, False, False)#      VAR:229 5      print_char output-character-code
op_print_num = Operation(COUNT_VAR, 0x06, False, False)#      VAR:230 6      print_num value
op_random = Operation(COUNT_VAR, 0x07, True , False)#*     VAR:231 7      random range -> (result)
op_push = Operation(COUNT_VAR, 0x08, False, False)#      VAR:232 8      push value
op_pull = Operation(COUNT_VAR, 0x09, False, False)#      VAR:233 9   1 pull (variable)
op_pull6 = Operation(COUNT_VAR, 0x09, True , False)#*                 6 pull stack -> (result)
op_split_window = Operation(COUNT_VAR, 0x0A, False, False)#      VAR:234 A   3 split_window lines
op_set_window = Operation(COUNT_VAR, 0x0B, False, False)#      VAR:235 B   3 set_window window
op_ext_NAME2 = Operation(COUNT_VAR, 0x0C, True , False)#*     VAR:236 C   4 call_vs2 routine ...0 to 7 args... -> (result)
op_erase_window = Operation(COUNT_VAR, 0x0D, False, False)#      VAR:237 D   4 erase_window window
op_erase_line = Operation(COUNT_VAR, 0x0E, False, False)#      VAR:238 E  4/- erase_line value
op_erase_line6 = Operation(COUNT_VAR, 0x0E, False, False)#                  6 erase_line pixels
op_set_cursor = Operation(COUNT_VAR, 0x0F, False, False)#      VAR:239 F   4 set_cursor line column
op_set_cursor6 = Operation(COUNT_VAR, 0x0F, False, False)#                  6 set_cursor line column window
op_get_cursor = Operation(COUNT_VAR, 0x10, False, False)#      VAR:240 10 4/6 get_cursor array
op_set_text_style = Operation(COUNT_VAR, 0x11, False, False)#      VAR:241 11  4 set_text_style style
op_buffer_mode = Operation(COUNT_VAR, 0x12, False, False)#      VAR:242 12  4 buffer_mode flag
op_output_stream = Operation(COUNT_VAR, 0x13, False, False)#      VAR:243 13  3 output_stream number
op_output_stream5 = Operation(COUNT_VAR, 0x13, False, False)#                  5 output_stream number table
op_output_stream6 = Operation(COUNT_VAR, 0x13, False, False)#                  6 output_stream number table width
op_input_stream = Operation(COUNT_VAR, 0x14, False, False)#      VAR:244 14  3 input_stream number
op_sound_effect = Operation(COUNT_VAR, 0x15, False, False)#      VAR:245 15 5/3 sound_effect number effect volume routine
op_read_char = Operation(COUNT_VAR, 0x16, True , False)#*     VAR:246 16  4 read_char 1 time routine -> (result)
op_scan_table = Operation(COUNT_VAR, 0x17, True , True )#*  * VAR:247 17   4 scan_table x table len form -> (result)
op_not = Operation(COUNT_VAR, 0x18, True , False)#*     VAR:248 18 5/6 not value -> (result)
op_call_vn = Operation(COUNT_VAR, 0x19, False, False)#      VAR:249 19  5 call_vn routine ...up to 3 args...
op_call_vn2 = Operation(COUNT_VAR, 0x1A, False, False)#      VAR:250 1A  5 call_vn2 routine ...up to 7 args...
op_tokenise = Operation(COUNT_VAR, 0x1B, False, False)#      VAR:251 1B  5 tokenise text parse dictionary flag
op_encode_text = Operation(COUNT_VAR, 0x1C, False, False)#      VAR:252 1C  5 encode_text zscii-text length from coded-text
op_copy_table = Operation(COUNT_VAR, 0x1D, False, False)#      VAR:253 1D  5 copy_table first second size
op_print_table = Operation(COUNT_VAR, 0x1E, False, False)#  VAR:254 1E      5 print_table zscii-text width height skip
op_check_arg_count = Operation(COUNT_VAR, 0x1F, False, True )#* VAR:255 1F      5 check_arg_count argument-number


#EXT Codes
# St Br Opcode Hex  V Inform name and syntax
op_ext_save = Operation(COUNT_EXT, 0x00, True , False)#*     EXT:0 0     5 save table bytes name -> (result)
op_ext_restore = Operation(COUNT_EXT, 0x01, True , False)#*     EXT:1   1   5 restore table bytes name -> (result)
op_ext_log_shift = Operation(COUNT_EXT, 0x02, True , False)#*     EXT:2   2   5 log_shift number places -> (result)
op_ext_art_shift = Operation(COUNT_EXT, 0x03, True , False)#*     EXT:3   3   5/- art_shift number places -> (result)
op_ext_set_font = Operation(COUNT_EXT, 0x04, True , False)#*     EXT:4   4   5 set_font font -> (result)
op_ext_draw_picture = Operation(COUNT_EXT, 0x05, False, False)#      EXT:5   5   6 draw_picture picture-number y x
op_ext_picture_data = Operation(COUNT_EXT, 0x06, False, True )#   * EXT:6    6   6 picture_data picture-number array ?(label)
op_ext_erase_picture = Operation(COUNT_EXT, 0x07, False, False)#      EXT:7   7   6 erase_picture picture-number y x
op_ext_set_margins = Operation(COUNT_EXT, 0x08, False, False)#      EXT:8   8   6 set_margins left right window
op_ext_save_undo = Operation(COUNT_EXT, 0x09, True , False)#*     EXT:9   9   5 save_undo -> (result)
op_ext_restore_undo = Operation(COUNT_EXT, 0x0A, True , False)#*     EXT:10 A    5 restore_undo -> (result)
op_ext_print_unicode = Operation(COUNT_EXT, 0x0B, False, False)#      EXT:11 B   5/* print_unicode char-number
op_ext_check_unicode = Operation(COUNT_EXT, 0x0C, False, False)#      EXT:12 C   5/* check_unicode char-number -> (result)
op_ext_move_window = Operation(COUNT_EXT, 0x10, False, False)#      EXT:16 10   6 move_window window y x
op_ext_window_size = Operation(COUNT_EXT, 0x11, False, False)#      EXT:17 11   6 window_size window y x
op_ext_window_style = Operation(COUNT_EXT, 0x12, False, False)#      EXT:18 12   6 window_style window flags operation
op_ext_get_wind_prop = Operation(COUNT_EXT, 0x13, True , False)#*     EXT:19 13   6 get_wind_prop window property-number -> (result)
op_ext_scroll_window = Operation(COUNT_EXT, 0x14, False, False)#      EXT:20 14   6 scroll_window window pixels
op_ext_pop_stack = Operation(COUNT_EXT, 0x15, False, False)#      EXT:21 15   6 pop_stack items stack
op_ext_read_mouse = Operation(COUNT_EXT, 0x16, False, False)#      EXT:22 16   6 read_mouse array
op_ext_mouse_window = Operation(COUNT_EXT, 0x17, False, False)#      EXT:23 17   6 mouse_window window
op_ext_push_stack = Operation(COUNT_EXT, 0x18, False, True )#   * EXT:24 18    6 push_stack value stack ?(label)
op_ext_put_wind_prop = Operation(COUNT_EXT, 0x19, False, False)#      EXT:25 19   6 put_wind_prop window property-number value
op_ext_print_form = Operation(COUNT_EXT, 0x1A, False, False)#      EXT:26 1A   6 print_form formatted-table
op_ext_make_menu = Operation(COUNT_EXT, 0x1B, False, True )#   * EXT:27 1B    6 make_menu number table ?(label)
op_ext_picture_table = Operation(COUNT_EXT, 0x1C, False, False)#      EXT:28 1C   6 picture_table table

