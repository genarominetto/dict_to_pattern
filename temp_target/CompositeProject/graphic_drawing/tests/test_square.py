import unittest
from graphic_drawing.components.leafs.square import Square

class TestSquare(unittest.TestCase):
    def test_square_creation(self):
        square = Square("TestSquare", 15, False)
        self.assertEqual(square.name, "TestSquare")
        self.assertEqual(square.size, 15)
        self.assertFalse(square.is_active)

    def test_square_structure(self):
        square = Square("TestSquare", 15, False)
        expected_structure = {'Square': 'TestSquare'}
        self.assertEqual(square.get_structure_as_dict(), expected_structure)

if __name__ == '__main__':
    unittest.main()
