import unittest
import main as m

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class TestMainMethod(unittest.TestCase):
	
	def test_isJsonValid(self):
		json = {}
		self.assertFalse(m.isJsonValid(None))
		self.assertFalse(m.isJsonValid(json))
		json["name"] = "toto"
		self.assertFalse(m.isJsonValid(json))
		json["url"] = "anUrl"
		self.assertFalse(m.isJsonValid(json))
		json["chapter"] = "25"
		self.assertTrue(m.isJsonValid(json))

	def test_canApplyConfigChanges(self):
		args = Namespace(name="toto", url="", chapter="")
		self.assertFalse(m.canApplyConfigChanges(None))
		self.assertFalse(m.canApplyConfigChanges(args))
		args.name="OnePiece"
		args.chapter = -2
		self.assertFalse(m.canApplyConfigChanges(args))
		args.chapter = 25
		self.assertTrue(m.canApplyConfigChanges(args))

if __name__ == '__main__':
	unittest.main()