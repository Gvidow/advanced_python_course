import unittest
from descriptor import Data
from metaclass import CustomMeta, CustomClass


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
        instance = CustomClass(val=14)
        self.assertTrue(hasattr(instance, "custom_val"))
        self.assertFalse(hasattr(instance, "val"))
        self.assertEqual(instance.custom_val, 14)
        self.assertEqual(instance.custom_x, 5)

        self.assertFalse(hasattr(CustomClass, "x"))
        self.assertTrue(hasattr(CustomClass, "custom_x"))
        self.assertTrue(hasattr(CustomClass, "custom_line"))
        self.assertEqual(instance.custom_line(), 100)

        self.assertEqual(str(instance), "Custom_by_metaclass")

        instance.dynamic = 20
        self.assertEqual(instance.custom_dynamic, 20)
        with self.assertRaises(AttributeError):
            type(instance.dynamic)

        with self.assertRaises(AttributeError):
            type(instance.x)
        with self.assertRaises(AttributeError):
            type(instance.val)
        with self.assertRaises(AttributeError):
            type(instance.line())
        with self.assertRaises(AttributeError):
            type(instance.yyy)
        with self.assertRaises(AttributeError):
            type(CustomClass.x)

    def test_create_class(self):
        A = CustomMeta("A", (), {"x": 12})
        B = CustomMeta("B", (A,), {"y": 2})

        instance_a = A()
        self.assertEqual(instance_a.custom_x, 12)
        self.assertFalse(hasattr(instance_a, "x"))
        self.assertEqual(instance_a.custom_x, 12)

        instance_b = B()
        self.assertTrue(issubclass(B, A))
        self.assertEqual(instance_b.custom_y, 2)


if __name__ == "__main__":
    unittest.main()
