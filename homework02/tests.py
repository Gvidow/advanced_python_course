import unittest.mock
from main import parse_json


class TestParseJSON(unittest.TestCase):
    @unittest.mock.patch("main.parse_json")
    def test_parse_json(self, mockk):
        s = '{"animals": "cat dog duck pig", "family": "father mother soon"}'
        parse_json(s, ["family", "sun", "d"], ["duck", "mother", "cat", "soon", "meet"], mockk)
        # mock_calls
        # call_args_list

        self.assertEqual(mockk.call_count, 2)
        self.assertListEqual(mockk.mock_calls, [unittest.mock.call("mother"),
                                                unittest.mock.call("soon")])


if __name__ == "__main__":
    unittest.main()
