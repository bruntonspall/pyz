if __name__ == '__main__':
    import ztext
    import memory
    import unittest
    import logging
    class testBaseNumbers(unittest.TestCase):
        def setUp(self):
            self.memory = memory.Memory( [
            0x98, 0xE8, 0x18, 0xE8, 0x98, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
            logging.basicConfig(level=logging.DEBUG)
            logging.warn("=== Running Setup for "+self.id())
            
        # Spec 3.2
        def testBasicZTextIsSequenceOfZChars(self):
            text = ztext.ztext(self.memory)
            t = text.get_text_at(0x00)
            self.assertEquals(3, len(t))
            self.assertEquals(6, t[0])
            self.assertEquals(7, t[1])
            self.assertEquals(8, t[2]) 

        def testCanGetMultiByteText(self):
            text = ztext.ztext(self.memory)
            t = text.get_text_at(0x01)
            self.assertEquals(6, len(t))
            self.assertEquals(6, t[0])
            self.assertEquals(7, t[1])
            self.assertEquals(8, t[2]) 
            self.assertEquals(6, t[3])
            self.assertEquals(7, t[4])
            self.assertEquals(8, t[5]) 
            
        def testCanGetAsciiFromZscii(self):
            self.assertEquals("abc",ztext.to_ascii([6,7,8]))
            
    unittest.main()  
