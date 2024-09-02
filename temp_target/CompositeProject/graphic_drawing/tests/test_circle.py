import unittest
from graphic_drawing.components.leafs.circle import Circle

class TestCircle(unittest.TestCase):
    def test_circle_creation(self):
        circle = Circle("TestCircle", 10, True)
        self.assertEqual(circle.name, "TestCircle")
        self.assertEqual(circle.size, 10)
        self.assertTrue(circle.is_active)

    def test_circle_structure(self):
        circle = Circle("TestCircle", 10, True)
        expected_structure = {'Circle': 'TestCircle'}
        self.assertEqual(circle.get_structure_as_dict(), expected_structure)

if __name__ == '__main__':
    unittest.main()
