import unittest.mock
from main import parse_json


class TestParseJSON(unittest.TestCase):
    @unittest.mock.patch("main.parse_json")
    def test_parse_json(self, callback_mock):
        string = '{"animals": "cat dog duck pig", ' \
                 '"family": "father mother son"}'
        parse_json(string, ["family", "sun", "d"],
                   ["duck", "mother", "cat", "son", "meet"], callback_mock)
        self.assertEqual(callback_mock.call_count, 2)
        self.assertListEqual(callback_mock.mock_calls,
                             [unittest.mock.call("mother"),
                              unittest.mock.call("son")])

        string = """{
        "keep": "wrong business age identify truth carry",
        "member": "same speech help item help political",
        "writer": "help without far leg help boy",
        "skin": "election official wonder",
        "threat": "necessary decide still",
        "child": "protect without trouble here anything \
        far board office leg impact beat both",
        "source": ""
        }"""
        parse_json(string, ["source", "skin", "writer", "help", "child"],
                   ["far", "help", "here", "both", "help", "child", "wonder"],
                   callback_mock)
        self.assertEqual(callback_mock.call_count, 9)
        self.assertListEqual(callback_mock.mock_calls[2:],
                             list(map(unittest.mock.call,
                                      ["help", "far", "help", "wonder",
                                       "here", "far", "both"])))

        parse_json(string, ["skin", "help"], ["help"], callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

        parse_json(string, [], [], callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

        parse_json(string, None, None, callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

    def test_with_factory(self):
        pass


if __name__ == "__main__":
    unittest.main()
