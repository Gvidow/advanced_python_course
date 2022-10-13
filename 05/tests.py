import unittest.mock
from collections.abc import Generator
from lru_cache import LRUCache
from filter_file import filter_file


class TestLRUCache(unittest.TestCase):
    def test_lru_cache(self):
        cache = LRUCache(5)
        for i in range(7):
            cache[i] = i ** 2
        self.assertEqual(cache.size, 5)
        self.assertEqual(len(cache.data), 5)
        self.assertListEqual(list(cache.data.keys()), [2, 3, 4, 5, 6])

        cache.set(8, 4)
        self.assertIsNone(cache.get(2))
        self.assertEqual(cache.get(8), 4)

        self.assertEqual(cache[5], 25)
        self.assertEqual(cache[8], 4)
        self.assertEqual(cache.get(4), 16)
        self.assertEqual(cache.get(3), 9)
        self.assertEqual(cache.get(4), 16)
        cache.set(5, 2)
        cache[6] = 4

        cache[87] = 1111
        self.assertIsNone(cache.get(8))
        cache[88] = 12
        self.assertIsNone(cache.get(3))


class TestFilterFile(unittest.TestCase):
    class StringAsFile:
        def __init__(self, text, *args, **kwargs):
            self.text = text

        def __enter__(self):
            return self.text.split("\n")

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def test_on_file(self):
        file_path = "test.txt"
        list_words = [
            "Образом", "кадров", "Два", "человЕК", "при", "углеводов"
        ]

        res_generator = filter_file(file_path, list_words)
        self.assertIsInstance(res_generator, Generator)

        res_list = list(res_generator)
        self.assertEqual(len(res_list), 8)
        self.assertListEqual(res_list, [
            "1 Равным Образом рАмки и Место обучения каДРов",
            "2 РИС и гречка ДВА отличных источника углеводов",
            "3 Старайтесь ФОТографИровать пРи хорошем освеЩЕнии",
            "4 В наше время пракТИчески каждый челоВЕК",
            "5 образом",
            "6 КАДРОВ",
            "7 Два",
            "8 Образом кадров Два человЕК при углеводов"
        ])

    @unittest.mock.patch("filter_file.open")
    def test_with_mock(self, open_mock):
        open_mock.side_effect = self.StringAsFile
        res = list(filter_file(
            "one\ntWo good\ngoodly\nBEST GOOD\n", ["good", "two"]
        ))
        self.assertEqual(res, [
            "tWo good",
            "BEST GOOD"
        ])


if __name__ == "__main__":
    unittest.main()
