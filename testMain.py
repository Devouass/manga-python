import unittest
import main as m
import logger

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestMainMethod(unittest.TestCase):

	def __init__(self, *args, **kwargs):
		super(TestMainMethod, self).__init__(*args, **kwargs)
		logger.getLogger().setMute(True)
	
	#def test_isJsonValid(self):
	#	json = {}
	#	self.assertFalse(m.isJsonValid(None))
	#	self.assertFalse(m.isJsonValid(json))
	#	json["name"] = "toto"
	#	self.assertFalse(m.isJsonValid(json))
	#	json["url"] = "anUrl"
	#	self.assertFalse(m.isJsonValid(json))
	#	json["chapter"] = "25"
	#	self.assertTrue(m.isJsonValid(json))

	#def test_canApplyConfigChanges(self):
	#	args = Namespace(name="toto", url="", chapter="")
	#	mc = m.MainClass()
	#	self.assertFalse(mc.canApplyConfigChanges(None))
	#	self.assertFalse(mc.canApplyConfigChanges(args))
	#	args.name="OnePiece"
	#	args.chapter = -2
	#	self.assertFalse(mc.canApplyConfigChanges(args))
	#	args.chapter = 25
	#	self.assertTrue(mc.canApplyConfigChanges(args))

if __name__ == '__main__':
	unittest.main()