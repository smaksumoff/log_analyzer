import unittest
from unittest.mock import mock_open, patch
from reports.handlers_report import HandlerReport


class TestHandlersReport(unittest.TestCase):
    """
    Test cases for the HandlerReport class.
    """

    def setUp(self) -> None:
        """
        Set up a HandlersReport instance before each test
        """
        self.report = HandlerReport()

    @patch("builtins.open", new_callable=mock_open, read_data="""
    2025-03-27 12:05:14,000 INFO django.request: GET /api/v1/auth/login/ 200 OK [192.168.1.28] 
    2025-03-27 12:10:14,000 DEBUG django.request: GET /api/v1/products/ 200 OK [192.168.1.29]
    2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected""")
    def test_process_file(self, mock_file):
        log_data = self.report.process_file("test_file.log")
        expected_result = {
            "/api/v1/auth/login/": {"DEBUG": 0, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
            "/api/v1/products/": {"DEBUG": 1, "INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
        }
        self.assertEqual(log_data, expected_result)

    def test_merge_files_data(self):
        file_data_1 = {
            "/api/v1/auth/login/": {"DEBUG": 1, "INFO": 2, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
        }
        file_data_2 = {
            "/api/v1/auth/login/": {"DEBUG": 0, "INFO": 3, "WARNING": 1, "ERROR": 0, "CRITICAL": 1},
            "/api/v1/products/": {"DEBUG": 2, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
        }

        self.report.merge_files_data(file_data_1)
        self.report.merge_files_data(file_data_2)

        expected_result = {
            "/api/v1/auth/login/": {"DEBUG": 1, "INFO": 5, "WARNING": 1, "ERROR": 0, "CRITICAL": 1},
            "/api/v1/products/": {"DEBUG": 2, "INFO": 1, "WARNING": 0, "ERROR": 0, "CRITICAL": 0},
        }
        self.assertEqual(self.report.data, expected_result)


# Run the tests
if __name__ == "__main__":
    unittest.main()
