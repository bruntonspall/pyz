import io
import unittest
import mox

class TestOutputStreamSupport(unittest.TestCase):
    empty_set = set()
    set_one = set([1])
    set_two = set([2])
    set_onetwo = set([1,2])
    def testCanSelectOutputStreams(self):
        iosys = io.IOSystem([], [])
        self.assertEquals(self.empty_set, iosys.get_active_outputs())
        iosys.activate_output(1)
        self.assertEquals(self.set_one, iosys.get_active_outputs())
        iosys.activate_output(2)
        self.assertEquals(self.set_onetwo, iosys.get_active_outputs())
        iosys.deactivate_output(1)
        self.assertEquals(self.set_two, iosys.get_active_outputs())
        iosys.activate_output(1)
        self.assertEquals(self.set_onetwo, iosys.get_active_outputs())
        iosys.activate_output(1)
        self.assertEquals(self.set_onetwo, iosys.get_active_outputs())
        
    def testPrintsGoToActiveStreams(self):
        TEST_STRING = "This is a test string"
        TEST_STRING2 = "This is another test string"
        mymox = mox.Mox()
        os1 = mymox.CreateMock(io.OStream)
        os2 = mymox.CreateMock(io.OStream)
        
        os1.print_string(TEST_STRING)
        os2.print_string(TEST_STRING)
        os1.print_string(TEST_STRING2)
        mymox.ReplayAll()

        iosys = io.IOSystem([], [os1, os2])
        iosys.activate_output(1)
        iosys.activate_output(2)
        iosys.print_string(TEST_STRING);
        iosys.deactivate_output(2)
        iosys.print_string(TEST_STRING2);
        
        mymox.VerifyAll()
        
        
        
    
if __name__ == '__main__':
    unittest.main()