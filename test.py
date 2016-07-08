
import unittest, logging

from wurst_parser import WurstParser

FILE_TESTS       = "./tests/tests.wurst"
FILE_PLAYER_COPY = "./tests/Player.wurst"

BOYS  = ["samuel", "bill", "james", "michael", "mike"]
GIRLS = ["jill", "mary", "alice"]


class TestWurstParser(unittest.TestCase):

	def test_visibility_rules(self):
		functions = WurstParser(FILE_TESTS).run()

		self.assertTrue(any(["samuel()"  in fn for fn in functions]))
		self.assertTrue(any(["bill()"    in fn for fn in functions]))
		self.assertTrue(any(["james()"   in fn for fn in functions]))
		self.assertTrue(any(["michael()" in fn for fn in functions]))
		self.assertTrue(any(["andrew()"  in fn for fn in functions]))
		self.assertTrue(any(["mike()"    in fn for fn in functions]))
		self.assertTrue(any(["calvin()"  in fn for fn in functions]))
		self.assertTrue(any(["david()"   in fn for fn in functions]))
		self.assertTrue(any(["eric()"    in fn for fn in functions]))

		self.assertTrue(all(["jill()"   not in fn for fn in functions]))
		self.assertTrue(all(["mary()"   not in fn for fn in functions]))
		self.assertTrue(all(["alice()"  not in fn for fn in functions]))
		self.assertTrue(all(["bree()"   not in fn for fn in functions]))
		self.assertTrue(all(["carina()" not in fn for fn in functions]))
		self.assertTrue(all(["danika()" not in fn for fn in functions]))

	def test_copy_of_handles_Player(self):
		functions = WurstParser(FILE_PLAYER_COPY).run()

		self.assertEquals(len(functions), 27)

		self.assertTrue(any(["getPlayer()" in fn for fn in functions]))


if __name__ == "__main__":
	logging.basicConfig(filename='test.log', level=logging.DEBUG)
	unittest.main()
