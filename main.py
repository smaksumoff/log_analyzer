import os
import sys
from reports.handlers_report import HandlerReport

REPORTS = {
    "handlers": HandlerReport
}


def parse_args() -> tuple[list[str], str]:
    """
    Parses arguments passed to the script via the command line.
    :return: Tuple containing a list of log file paths and the report type.
    """
    # Extract parameters
    logs: list[str] = []
    report_type: str | None = None

    for arg in sys.argv[1:]:
        if arg.startswith("--report"):
            report_type = sys.argv[sys.argv.index(arg) + 1]
            break
        elif arg.endswith(".log"):
            logs.append(arg)

    if not logs:
        raise ValueError("Error: No log files specified.")
    if report_type not in REPORTS:
        raise ValueError(f"Error: Invalid report type. Available types: {', '.join(REPORTS.keys())}.")

    # Check for file existence
    missing_files = [log_file for log_file in logs if not os.path.isfile(log_file)]
    if missing_files:
        raise FileNotFoundError(
            "Error: The following log files do not exist or are not accessible: "
            + ", ".join(missing_files)
        )

    return logs, report_type


def main() -> None:
    """
    Main entry point of the script.
    """
    try:
        log_files, report_type = parse_args()

        # Report generation
        report_class = REPORTS[report_type]()
        result: str = report_class.generate(log_files)

        print(result)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
