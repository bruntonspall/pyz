import ztext
import memory
import unittest
import logging
class testBaseNumbers(unittest.TestCase):
    mem = memory.Memory( [
        0x98, 0xE8, 0x18, 0xE8, 0x98, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      
    # Spec 3.2
    def testBasicZTextIsSequenceOfZChars(self):
        t = ztext.get_text_at(self.mem, 0x00)
        self.assertEquals(3, len(t))
        self.assertEquals(6, t[0])
        self.assertEquals(7, t[1])
        self.assertEquals(8, t[2]) 

    def testCanGetMultiByteText(self):
        t = ztext.get_text_at(self.mem, 0x01)
        self.assertEquals(6, len(t))
        self.assertEquals(6, t[0])
        self.assertEquals(7, t[1])
        self.assertEquals(8, t[2]) 
        self.assertEquals(6, t[3])
        self.assertEquals(7, t[4])
        self.assertEquals(8, t[5]) 
        
    # Spec 3.2.1
    # Spec 3.2.3
    # Spec 3.2.4
    
    def testCanGetZsciiFromZtext(self):
        self.assertEquals("abc",ztext.to_zscii([6,7,8]))
        self.assertEquals("Abc",ztext.to_zscii([4,6,7,8]))
        self.assertEquals("", ztext.to_zscii([4,4,4,4]))
        
    def testCanGetZtextFromZcii(self):
        self.assertEquals([6,7,8],ztext.from_zscii("abc"))
        self.assertEquals([4,4,4], ztext.from_zscii(""))
        self.assertEquals([4,6,7,8,4,4],ztext.from_zscii("Abc"))
        
    def testCanEncodeZTextToMemory(self):
        self.assertEquals([0x98, 0xE8],ztext.to_bytes(ztext.from_zscii("abc")))
        self.assertEquals([0x90, 0x84], ztext.to_bytes(ztext.from_zscii("")))
        self.assertEquals([0x10, 0xC7, 0xA0, 0x84],ztext.to_bytes(ztext.from_zscii("Abc")))
        

if __name__ == '__main__':
    unittest.main()
