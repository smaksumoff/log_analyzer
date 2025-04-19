import re


class HandlerReport:
    """
    Generates a report for HTTP endpoints (handlers) and their logging levels
    from Django application logs.
    """
    LOG_LEVELS: list[str] = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def __init__(self):
        self.data: dict[str, dict[str, int]] = {}

    def process_file(self, log_file: str) -> dict:
        """
        Processes a single log file and extracts log level counts per handler.
        :param log_file: The path to the log file.
        :return: A dictionary where each key is a handler, and the value is
                 another dictionary mapping log levels to their occurrence counts..
        """
        data: dict[str, dict[str, int]] = {}

        # Regex pattern to extract logging level and handler URI
        log_pattern = re.compile("(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL).*django.request.*?(?P<handler>/\S+)")

        with open(log_file, "r") as file:
            for line in file:
                match = log_pattern.search(line)
                if match:
                    level = match.group("level")
                    handler = match.group("handler")
                    if handler not in data:
                        data[handler] = {level: 0 for level in self.LOG_LEVELS}
                    data[handler][level] += 1

        return data

    def merge_files_data(self, file_data: dict[str, dict[str, int]]) -> None:
        """
        Merges extracted log data from a single file into the main data dictionary.
        :param file_data: Data from a single file.
        """
        for handler, levels in file_data.items():
            # Initialize a new handler in self.data if not already present
            if handler not in self.data:
                self.data[handler] = {level: 0 for level in self.LOG_LEVELS}

            # Update counts for each log level
            for level in levels:
                self.data[handler][level] += levels[level]

    def generate(self, log_files: list[str]) -> str:
        """
        Processes multiple log files and generates a formatted report.
        :param log_files: List of file paths.
        :return: A report as a string represented in the form of a table
        """
        # Process each file and merge results into self.data
        for log_file in log_files:
            file_data = self.process_file(log_file)
            self.merge_files_data(file_data)

        # Format the report from the consolidated data
        return self.format_report()

    def format_report(self):
        """
        Formats the consodilated log data into a table-like report.
        :return: A string representation of the report, formatted as a table
                 with rows for handlers, columns for log levels, and cell values for log level counts.
        """
        # Sort the handlers alphabetically
        handlers = sorted(self.data.items())

        # Dictionary to track total counts for each log level across all handlers
        total_by_level = {level: 0 for level in self.LOG_LEVELS}

        # Create the header row for the table
        report_rows = ["HANDLERS".ljust(25) + "".join(level.ljust(10) for level in self.LOG_LEVELS)]

        # Add rows for each handler and its log level counts
        for handler, levels in handlers:
            line = handler.ljust(25) + "".join(str(levels[level]).ljust(10) for level in self.LOG_LEVELS)
            report_rows.append(line)

            for level in self.LOG_LEVELS:
                total_by_level[level] += levels[level]

        # Add the totals row at the end of the table
        total_row = "TOTAL".ljust(25) + "".join(str(total_by_level[level]).ljust(10) for level in self.LOG_LEVELS)
        report_rows.append(total_row)

        return "\n".join(report_rows)
