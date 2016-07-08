
import unittest, logging

from wurst_parser import WurstParser

TEST_FILE = "./tests/tests.wurst"

BOYS  = ["samuel", "bill", "james", "michael", "mike"]
GIRLS = ["jill", "mary", "alice"]


class TestWurstParser(unittest.TestCase):

	def test_visibility_rules(self):
		functions = WurstParser(TEST_FILE).run()

		self.assertTrue(any(["samuel()"  in fn for fn in functions]))
		self.assertTrue(any(["bill()"    in fn for fn in functions]))
		self.assertTrue(any(["james()"   in fn for fn in functions]))
		self.assertTrue(any(["michael()" in fn for fn in functions]))
		self.assertTrue(any(["andrew()"  in fn for fn in functions]))
		self.assertTrue(any(["mike()"    in fn for fn in functions]))

		self.assertTrue(all(["jill()"  not in fn for fn in functions]))
		self.assertTrue(all(["mary()"  not in fn for fn in functions]))
		self.assertTrue(all(["alice()" not in fn for fn in functions]))
		self.assertTrue(all(["bree()"  not in fn for fn in functions]))


if __name__ == "__main__":
	logging.basicConfig(filename='test.log', level=logging.DEBUG)
	unittest.main()
