import unittest
import client
import unittest.mock


class TestServerAndClient(unittest.TestCase):
    class StringAsFile:
        def __init__(self, text, *args, **kwargs):
            self.text = text

        def __enter__(self):
            return self.text.split("\n")

        def __exit__(self, *args):
            pass

    def test_fetch_urls(self):
        with unittest.mock.patch("client.open") as mock_open_file,\
                unittest.mock.patch("client.print") as mock_print_client:
            mock_open_file.side_effect = self.StringAsFile
            client.main(10, "https://example.org/")
            self.assertEqual(1, mock_print_client.call_count)
            self.assertIn("https://example.org/", mock_print_client.call_args_list[0].args[0])


if __name__ == "__main__":
    unittest.main()
