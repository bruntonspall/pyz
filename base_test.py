import base
import memory
import unittest
import logging
class testBaseNumbers(unittest.TestCase):
    def setUp(self):
        self.memory = memory.Memory( [
        # Header is 64 bytes
        # Byte 4 says wehre high memory starts
        # Byte 15 (0x0e) says where dynamic ends
        0x00, 0x01, 0x02, 0x03, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x50, 0x00,     # 0x00 HEADER
        0xFF, 0xFF, 0x00, 0x00, 0x80, 0x00, 0x7F, 0xFF, 0x80, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x10 HEADER
        0x00, 0x00, 0x02, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x20 HEADER
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x30 HEADER
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x40 DYNAMIC
        0x00, 0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,     # 0x50 STATIC
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])    # 0x60 HIGH
        
    # Spec 2.1
    # Spec 2.2
    def testCanInterpretBasicNumbers(self):
        self.assertEquals(0x01, base.number(0x0001))
        self.assertEquals(-1, base.number(0xFFFF))
        self.assertEquals(32767, base.number(0x7FFF))
        self.assertEquals(-1, base.number(0xFFFF).as_signed())
        self.assertEquals(0, base.number(0x0000).as_signed())
        self.assertEquals(-32768, base.number(0x8000).as_signed())
        self.assertEquals(32767, base.number(0x7FFF).as_signed())
        self.assertEquals(-32767, base.number(self.memory.get_2byte(0x0c)).as_signed())
        
    # Spec 2.2.1
    def testCanPerformanMathOnNumbers(self):
        two = base.number(0x0002)
        sixteen = base.number(0x0010)
        minus_two = base.number(0xFFFE)
        self.assertEqual(two, two)
        self.assertEqual(minus_two, minus_two)
        self.assertEqual(base.number(4), two+two)
        self.assertEqual(base.number(14), sixteen+minus_two)
        self.assertEqual(base.number(-2), base.number(0)+minus_two)
        self.assertEqual(base.number(-2), base.number(0)-two)
        self.assertEqual(base.number(14), sixteen-two)
        self.assertEqual(base.number(8), base.number(4)*two)
        self.assertEqual(base.number(-8), base.number(4)*minus_two)
        self.assertEqual(two, base.number(4)/two)
        self.assertEqual(two, base.number(5)/two)
        self.assertEqual(base.number(1), base.number(5)%two)
        self.assertEqual("2", str(two))
        self.assertEqual("-2", str(minus_two))            

    # Spec 2.3.1
    def testDivByZeroErrors(self):
        one = base.number(1)
        zero = base.number(0)
        self.assertRaises(ZeroDivisionError, lambda a: a[0]/a[1], (one, zero)) 
        self.assertRaises(ZeroDivisionError, lambda a: a[0]%a[1], (one, zero))
        
    # Spec 2.3.2
    def testOverflow(self):
        # Not a formal part of spec, so we don't actually care right now
        # Suggestion is that 0x8000 + 0x8000 (or * 2) should be 0x0000
        self.assertEquals(0, base.number(0x8000) + base.number(0x8000))

if __name__ == '__main__':
    unittest.main()
