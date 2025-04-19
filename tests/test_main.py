import unittest
from unittest.mock import patch
from main import parse_args, main


class TestMain(unittest.TestCase):
    @patch("os.path.isfile", return_value=True)  # Mock os.path.isfile to always return True
    @patch("sys.argv", ["main.py", "file1.log", "file2.log", "--report", "handlers"])
    def test_parse_args_valid_input(self, mock_argv, mock_isfile):
        """
        Test parse_args with valid input arguments, includes log files and a valid report type.
        """
        logs, report_type = parse_args()
        self.assertEqual(logs, ["file1.log", "file2.log"])
        self.assertEqual(report_type, "handlers")


if __name__ == "__main__":
    unittest.main()
