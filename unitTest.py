import unittest
import chatParser

singleRoll     = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\singleRoll.html"
singleMessage  = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\singleMessage.html"
rollTheText    = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\rollThenText.html"
nameTest       = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\nameTest.html"
multiRoll      = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\multiRoll.html"
meTextThenRoll = "E:\\GitProjects\\roll20Analyzer\\data\\testData\\meTextThenRoll.html"

class MyTestCase(unittest.TestCase):


    def test_Parth_notEmpty(self):
        self.assertGreater(len(chatParser.getParse(singleRoll)), len([]))
        self.assertGreater(len(chatParser.getParse(singleMessage)), len([]))
        self.assertGreater(len(chatParser.getParse(rollTheText)), len([]))
        self.assertGreater(len(chatParser.getParse(nameTest)), len([]))
        self.assertGreater(len(chatParser.getParse(multiRoll)), len([]))
        self.assertGreater(len(chatParser.getParse(meTextThenRoll)), len([]))

if __name__ == '__main__':
    unittest.main()
