import memory
import unittest
import logging
class testMemory(unittest.TestCase):
    def setUp(self):
        self.memory = memory.Memory( [
        # Header is 64 bytes
        # Byte 4 says where high memory starts
        # Byte 15 (0x0e) says where dynamic ends
        0x00, 0x01, 0x02, 0x03, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x00,     # 0x00 HEADER
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x10 HEADER
        0x00, 0x00, 0x02, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x20 HEADER
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x30 HEADER
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x40 DYNAMIC
        0x00, 0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x50 STATIC
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])    # 0x60 HIGH

    # Spec 1.1
    # Spec 1.1.1.1
    def testMemoryLayout(self):
        self.assertEquals(0x70, self.memory.size())
        self.assertEquals(0x60, self.memory.high_mem_start())
        self.assertEquals(0x60, self.memory.get_byte(0x04))
        self.assertEquals(0x50, self.memory.static_mem_start())
        self.assertEquals(0x50, self.memory.get_byte(0x0e))
        self.assertEquals(memory.HEADER, self.memory.get_type_at(0x01))
        self.assertEquals(memory.DYNAMIC, self.memory.get_type_at(0x41))
        self.assertEquals(memory.STATIC, self.memory.get_type_at(0x51))
        self.assertEquals(memory.HIGH, self.memory.get_type_at(0x61))
        self.assertEquals(memory.NONE, self.memory.get_type_at(0x71))
        
    # Spec 1.1.1
    # Spec 1.1.1.2
    def testDynamicMemoryCanBeWrittenAndReadFrom(self):
        self.assertEqual(0x00, self.memory.get_byte(0x42))
        self.memory.put_byte(0x42, 0x20)
        self.assertEqual(0x20, self.memory.get_byte(0x42))
        self.assertEqual(0x2000, self.memory.get_2byte(0x21))
        self.memory.put_2byte(0x21, 0x1234)
        self.assertEqual(0x1234, self.memory.get_2byte(0x21))
        self.assertEqual(0x12, self.memory.get_byte(0x42))
        self.assertEqual(0x34, self.memory.get_byte(0x43))
    
    # Spec 1.1.2
    def testStaticMemoryCanBeReadFromOnly(self):
        self.assertEqual(0x00, self.memory.get_byte(0x50))
        self.assertEqual(0x01, self.memory.get_byte(0x51))
        self.assertEqual(0x20, self.memory.get_byte(0x52))
        self.assertEqual(0x2000, self.memory.get_2byte(0x29))
        self.assertRaises(memory.ReadOnlyException, lambda m: m[0].put_byte(m[1], m[2]), (self.memory, 0x51, 0x00))
        self.assertRaises(memory.ReadOnlyException, lambda m: m[0].put_2byte(m[1], m[2]), (self.memory, 0x29, 0x00))
        
    # Spec 1.1.3
    def testHighMemoryCannotBeAccessedDirectly(self):
        self.assertRaises(memory.OutOfRangeException, lambda m: m[0].put_byte(m[1], m[2]), (self.memory, 0x61, 0x00))
        self.assertRaises(memory.OutOfRangeException, lambda m: m[0].put_2byte(m[1], m[2]), (self.memory, 0x31, 0x00))
        self.assertRaises(memory.OutOfRangeException, lambda m: m[0].get_byte(m[1]), (self.memory, 0x61))
        self.assertRaises(memory.OutOfRangeException, lambda m: m[0].get_2byte(m[1]), (self.memory, 0x31))
        # High Memory can be read from for strings and zcode
        self.assertEqual(0x01, self.memory.get_high_byte(0x61))

    # Spec 1.2.1
    def testByteAndWordAddressesWork(self):
        self.assertEquals(0x00, self.memory.get_byte(0))
        self.assertEquals(0x01, self.memory.get_byte(1))
        self.assertEquals(0x0001, self.memory.get_2byte(0))
        self.assertEquals(0x0203, self.memory.get_2byte(1))
        self.assertEquals(0x02, self.memory.get_byte(0x22))
        self.assertEquals(0x03, self.memory.get_byte(0x23))
        self.assertEquals(0x0203, self.memory.get_2byte(0x11))
        
    # Spec 1.2.3
    def testPackedAddressWork(self):
        self.memory.set_version(1)
        self.assertEquals(0x00, self.memory.loadp(0x30))
        self.assertEquals(0x02, self.memory.loadp(0x31))
        self.memory.set_version(2)
        self.assertEquals(0x00, self.memory.loadp(0x30))
        self.assertEquals(0x02, self.memory.loadp(0x31))
        self.memory.set_version(3)
        self.assertEquals(0x00, self.memory.loadp(0x30))
        self.assertEquals(0x02, self.memory.loadp(0x31))
        self.memory.set_version(4)
        self.assertEquals(0x00, self.memory.loadp(0x18))
        self.assertEquals(0x04, self.memory.loadp(0x19))
        self.memory.set_version(5)
        self.assertEquals(0x00, self.memory.loadp(0x18))
        self.assertEquals(0x04, self.memory.loadp(0x19))
        self.memory.set_version(6)
        self.assertEquals(0x00, self.memory.loadp(0x18))
        self.assertEquals(0x04, self.memory.loadp(0x19))
        self.memory.set_version(7)
        self.assertEquals(0x00, self.memory.loadp(0x18))
        self.assertEquals(0x04, self.memory.loadp(0x19))
        self.memory.set_version(8)
        self.assertEquals(0x00, self.memory.loadp(0x0c))
        self.assertEquals(0x08, self.memory.loadp(0x0d))
        
    

if __name__ == '__main__':
    unittest.main()
