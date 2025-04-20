import unittest
from unittest.mock import patch, MagicMock
from main import parse_args


class TestParseArgs(unittest.TestCase):
    @patch("sys.argv", ["main.py", "file1.log", "file2.log", "--report", "handlers"])
    @patch("os.path.isfile", MagicMock(side_effect=lambda x: x in ["file1.log", "file2.log"]))
    def test_valid_args(self):
        """Test parse_args with valid arguments."""
        logs, report_type = parse_args()
        self.assertEqual(logs, ["file1.log", "file2.log"])
        self.assertEqual(report_type, "handlers")

    @patch("sys.argv", ["main.py", "--report", "handlers"])
    @patch("os.path.isfile", MagicMock(return_value=False))
    def test_missing_log_files(self):
        """Test parse_args when no log files are specified."""
        with self.assertRaises(ValueError) as e:
            parse_args()
        self.assertEqual(str(e.exception), "Error: No log files specified.")

    @patch("sys.argv", ["main.py", "file1.log", "--report", "invalid_report"])
    @patch("os.path.isfile", MagicMock(side_effect=lambda x: x == "file1.log"))
    def test_invalid_report_type(self):
        """Test parse_args with an invalid report type."""
        with self.assertRaises(ValueError) as e:
            parse_args()
        self.assertEqual(str(e.exception), "Error: Invalid report type. Available types: handlers.")

    @patch("sys.argv", ["main.py", "file1.log", "file2.log", "file3.log", "--report", "handlers"])
    @patch("os.path.isfile", MagicMock(side_effect=lambda x: x == "file1.log"))
    def test_missing_file(self):
        """Test parse_args with an invalid report type."""
        with self.assertRaises(FileNotFoundError) as e:
            parse_args()
        self.assertEqual(
            str(e.exception),
            "Error: The following log files do not exist or are not accessible: file2.log, file3.log"
        )

    @patch("sys.argv", ["main.py", "file1.txt", "file2.log", "--report", "handlers"])
    @patch("os.path.isfile", MagicMock(side_effect=lambda x: x in ["file1.txt", "file2.log"]))
    def test_non_log_extension(self):
        """Test parse_args when a file does not have the .log extension."""
        logs, report_type = parse_args()
        self.assertEqual(logs, ["file2.log"])
        self.assertEqual(report_type, "handlers")


if __name__ == "__main__":
    unittest.main()
