# Django Log Analyzer

`Django Log Analyzer` is a Python CLI tool designed to analyze Django application logs and generate reports. It processes multiple log files, extracts useful insights about API handlers and their logging levels, and outputs the results in a tabular format. The application is modular and extensible, making it easy to add new report types in the future.

---

## Features

- **Handles multiple log files**: Processes and combines data from multiple files into a single summarized report.
- **Generates API handler-level reports**: Groups logs by handlers and log levels, such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`.
- **Validates inputs**: Ensures all specified files exist and raises errors for invalid report types or missing files.
- **Displays results in a tabular format**: Clearly organizes data for easy interpretation.
- **Extensible architecture**: Easily add new report types without modifying the existing codebase.

---

## Installation

Follow these steps to set up the project:

1. Clone this repository:
   ```zsh
   git clone https://github.com/smaksumoff/log_analyzer.git
2. Navigate to the project directory:
   ```zsh
   cd logging_analyzer
3. (Optional) Set up a virtual environment:
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
4. Install the required dependencies:
   ```zsh
   pip install -r requirements.txt

---

## Usage

### General Command Syntax
   ```zsh
   python3 main.py <log_file_1> <log_file_2> ... --report <report_name>
   ```
### Example Command
Using the handlers report on two sample log files:
   ```zsh
   python3 main.py logs/app1.log logs/app2.log --report handlers
   ```
**Expected output:**

| HANDLERS             | DEBUG | INFO | WARNING | ERROR   | CRITICAL |
|:---------------------|:------|:-----|:--------|:--------|:---------|
| /admin/dashboard/    | 10    | 45   | 12      | 6       | 1        |
| /api/v1/auth/login/  | 8     | 50   | 4       | 10      | 0        |
| /api/v1/orders/      | 12    | 24   | 9       | 3       | 2        |
| **TOTAL**            | 30    | 119  | 25      | 19      | 3        |

---

## Extending the Application

The application allows developers to add new report types without making substantial changes to existing code. 

### Steps to Add a New Report

1. Create a New Report Class:
   - Go to the reports/ directory.
   - Create a new file, e.g., **new_report.py**.
   - Define a class that implements:
     - `process_file`: to handle log parsing.
     - `merge_files_data`: to consolidate data from multiple files.
     - `format_report`: to format the final output.
     
2. Update the `REPORTS` Dictionary:
   - Open `main.py` and add your report class to the `REPORTS` dictionary:
   ``` Python
   from reports.new_report import NewReport
   
   REPORTS = {
        "handlers": HandlerReport,
        "new_report": NewReport
   }
   ```
3. Test Your New Report:
   - Write tests for your new report in the `tests/ directory`, e.g., `test_new_report.py`.
   - Verify that the report behaves as expected.

--- 

## Final Notes

This README is designed to guide users on:

1. **Installation**: Setting up the tool locally.
2. **Usage**: Running the application and interpreting its output.
3. **Testing**: Ensuring functionality through unit tests.
4. **Extensibility**: Adding new report types without disrupting the existing code.
