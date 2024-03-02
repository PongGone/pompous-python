# Endpoint Checker

Endpoint Checker is a Python application designed to check the status of HTTP endpoints. 
It allows users to enter a URL or IP address and retrieves information such as response time, HTTP response code, and request details.

## Features

- **Check Endpoint**: Enter a URL or IP address to check its status, including response time, HTTP response code, and request details.
- **Logs Display**: View the logs of endpoint checks in the application interface.
- **Clear Logs**: Clear the logs to start a fresh session.
- **Export Logs**: Export logs in either CSV or JSON format for further analysis.
- **User-Friendly Interface**: Simple and intuitive GUI for easy operation.

## Requirements

- Python 3.x
- Required Python packages: `tkinter`, `requests`, `re`, `socket`, `webbrowser`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PongGone/endpoint-checker.git
   ```

2. Navigate to the project directory:
   ```bash
   cd endpoint-checker
   ```

3. Run the application:
   ```bash
   python endpoint_checker.py
   ```

## Usage

1. Launch the application by executing the `endpoint_checker.py` file.
2. Enter the endpoint URL or IP address in the provided box.
3. Click on the "Check Endpoint" button to retrieve information about the endpoint's status.
4. View the logs displayed in the application interface.
5. Optionally, export the logs in either CSV or JSON format using the "Export Logs" button.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

This application is developed and maintained by [PongGone](https://github.com/PongGone).
