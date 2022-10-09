import unittest
from descriptor import Data


class TestDescriptor(unittest.TestCase):
    def test_data(self):
        data = Data(num=-10, name="good", price=2)
        self.assertEqual(len(data.__dict__), 3)
        self.assertEqual(data.__dict__["__num"], -10)
        self.assertEqual(data.__dict__["__name"], "good")
        self.assertEqual(data.__dict__["__price"], 2)

        data.num = 12
        self.assertEqual(data.num, 12)
        self.assertEqual(data.__dict__["__num"], 12)

        data.name = "very good"
        self.assertEqual(data.name, "very good")
        self.assertEqual(data.__dict__["__name"], "very good")

        data.price += 1
        self.assertEqual(data.price, 3)
        self.assertEqual(data.__dict__["__price"], 3)

        self.assertFalse("num" in data.__dict__)
        self.assertFalse("name" in data.__dict__)
        self.assertFalse("dict" in data.__dict__)

        with self.assertRaises(TypeError):
            Data(1.3, "bad test", 2)

        with self.assertRaises(TypeError):
            Data(-10, "bad test", -10)

        with self.assertRaises(TypeError):
            Data(6, 6, 6)

        data2 = Data(4, "test", 5)
        with self.assertRaises(TypeError):
            data2.price -= 10

        data2.price -= 4
        self.assertEqual(data2.price, 1)

        with self.assertRaises(TypeError):
            data2.name = 14

        with self.assertRaises(TypeError):
            data2.num = "text"

        del data2.num
        self.assertEqual(len(data2.__dict__), 2)
        self.assertFalse(hasattr(data2, "num"))
        self.assertFalse(hasattr(data2, "__num"))


class TestMetaClass(unittest.TestCase):
    def test_class(self):
        pass


if __name__ == "__main__":
    unittest.main()
