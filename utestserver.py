import unittest
from server import *

class ServerTest(unittest.TestCase):
	def test_idx(self):
		s = Segment()
		idx = s.strToIdx("test")
		self.assertEqual(idx, 1287)

	def test_collision(self):
		s = Segment()
		idx = s.strToIdx("test.variable.12")
		numColl = 0
		for i in range(0, 516 * 16 * 8):
			idxC = s.strToIdx(str(i))
			if idxC == idx:
				print("Collision at " + str(i))
				numColl += 1
		self.assertEqual(numColl, 0)
		

	def test_ids(self):
		s = Segment()
		ids = s.strToIds("test.variable.at.current.location.123")
		self.assertEqual(ids, "ent.location.123")

	def test_setget(self):
		ost = "test123"
		s = Segment()
		
		s.set("test.1", ost)
		
		x = s.get("test.1")
		st = str(x[2]).strip()
		
		self.assertEqual(ost, st)

if __name__ == '__main__':
	unittest.main()