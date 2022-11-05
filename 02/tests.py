import unittest.mock
from main import parse_json
from factory_data import TestDataFactory


class TestParseJSON(unittest.TestCase):
    @unittest.mock.patch("main.parse_json")
    def test_parse_json(self, callback_mock):
        string = '{"animals": "cat dog duck pig", ' \
                 '"family": "father mother son"}'
        parse_json(string, ["family", "sun", "d"],
                   ["duck", "mother", "cat", "son", "meet"], callback_mock)
        self.assertEqual(callback_mock.call_count, 2)
        self.assertSetEqual(set(map(lambda x: x.args[0],
                                    callback_mock.mock_calls)),
                            set(["mother", "son"]))

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
        self.assertSetEqual(set(map(lambda x: x.args[0],
                            callback_mock.mock_calls[2:])),
                            set(["here", "far", "both",
                                 "help", "far", "help", "wonder"]))

        parse_json(string, ["skin", "help"], ["help"], callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

        parse_json(string, [], [], callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

        parse_json(string, None, None, callback_mock)
        self.assertEqual(callback_mock.call_count, 9)

    def test_with_factory(self):
        def checking_calls():
            cou = 0
            set_calls = set()

            def counter(*args):
                nonlocal cou
                cou += 1
                if len(args) > 0:
                    set_calls.add(*args)
                return cou - 1, set_calls

            return counter

        for _ in range(1000):
            test = TestDataFactory()
            counter_calls = checking_calls()
            parse_json(test.parse_dict(), test.required_fields,
                       test.keywords, counter_calls)
            expected = (test.expected_count_calls, test.call_args_set)
            result = counter_calls()
            self.assertTupleEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
