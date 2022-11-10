import unittest
from custom_list import CustomList


def is_equal(lst1, lst2):
    if len(lst1) != len(lst2):
        return False
    return all(lst1[i] == lst2[i] for i in range(len(lst1)))


class TestCustomList(unittest.TestCase):
    def test_init(self):
        lst = [2, 4, 6]
        custom_lst = CustomList(lst)
        self.assertIsInstance(custom_lst, CustomList)
        self.assertNotIsInstance(lst, CustomList)

        custom_lst2 = CustomList(range(10))
        self.assertIsInstance(custom_lst2, CustomList)
        self.assertEqual(len(custom_lst2), 10)
        for i in range(10):
            self.assertEqual(custom_lst2[i], i)

    def test_add(self):
        lst1 = CustomList([1, 2, 3])
        lst2 = CustomList((6, 3, 1, 8, -3))
        lst1_copy = lst1
        lst2_copy = lst2
        lst3 = lst1 + lst2

        self.assertIs(lst1, lst1_copy)
        self.assertIs(lst2, lst2_copy)
        self.assertTrue(is_equal(lst1, [1, 2, 3]))
        self.assertTrue(is_equal(lst2, [6, 3, 1, 8, -3]))
        self.assertTrue(is_equal(lst3, [7, 5, 4, 8, -3]))
        self.assertIsInstance(lst3, CustomList)
        self.assertIsNot(lst3, lst1)
        self.assertIsNot(lst3, lst2)

        lst4 = lst1
        self.assertIsInstance(lst4, CustomList)
        lst4 += lst2
        self.assertIs(lst4, lst1)

        # lst3 = [7, 5, 4, 8, -3]
        lst4 = [1, 2] + lst3
        lst1 = lst3 + [1, 2]
        self.assertTrue(is_equal(lst4, [8, 7, 4, 8, -3]))
        self.assertTrue(is_equal(lst4, lst1))
        self.assertIsNot(lst4, lst1)

    def test_sub(self):
        lst1 = CustomList([10, 5])
        lst2 = CustomList((6, 3, 9, 1))
        lst1_copy = lst1
        lst2_copy = lst2
        lst3 = lst1 - lst2

        self.assertIs(lst1, lst1_copy)
        self.assertIs(lst2, lst2_copy)
        self.assertTrue(is_equal(lst1, [10, 5]))
        self.assertTrue(is_equal(lst2, [6, 3, 9, 1]))
        self.assertTrue(is_equal(lst3, [4, 2, -9, -1]))

        self.assertIsNot(lst3, lst1)
        self.assertIsNot(lst3, lst2)
        self.assertIsInstance(lst3, CustomList)

        lst4 = lst1
        lst4 -= lst2
        self.assertIs(lst4, lst1)

        # lst3 = [4, 2, -9, -1]
        lst4 = [5, 9, -6] - lst3
        lst1 = lst3 - [5, 9, -6]
        self.assertTrue(is_equal(lst4, [1, 7, 3, 1]))
        self.assertTrue(is_equal(lst1, [-1, -7, -3, -1]))

        lst5 = CustomList()
        lst5 -= list(range(10))
        self.assertEqual(len(lst5), 10)
        for i in range(10):
            self.assertEqual(lst5[i], -i)

    def test_compare(self):
        lst1 = CustomList([1, 2, 3, 4])
        lst2 = CustomList([1, 2, 3, 4, 5])
        lst3 = CustomList([1, 1, 1, 3, 2, 2])
        self.assertTrue(lst1 == lst3)
        self.assertTrue(lst1 != lst2)
        self.assertTrue(lst1 <= lst3)
        self.assertTrue(lst1 >= lst3)
        self.assertTrue(lst1 < lst2)
        self.assertTrue(lst1 <= lst2)
        self.assertTrue(lst2 > lst1)
        self.assertTrue(lst2 >= lst1)
        self.assertFalse(lst1 < lst3)
        self.assertFalse(lst1 > lst3)
        self.assertFalse(lst1 != lst3)
        self.assertFalse(lst1 > lst2)
        self.assertFalse(lst2 < lst1)

    def test_str(self):
        lst1 = CustomList([1, -4, 6, 7])
        lst2 = CustomList([-3, 2, 4, 10, -1, 12, -24])
        self.assertEqual(str(lst1), "[1, -4, 6, 7], 10")
        self.assertEqual(str(lst2), "[-3, 2, 4, 10, -1, 12, -24], 0")


if __name__ == "__main__":
    unittest.main()
