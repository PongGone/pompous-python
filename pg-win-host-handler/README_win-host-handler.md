# Windows Host Handler

Windows Host Handler is a Python application designed to retrieve and display various information about a Windows host system.

It provides insights into the host, system, and network details in a user-friendly graphical interface.

## Features

- **Host Information**: Retrieve details like hostname, processor, installed RAM, and product ID.
- **System Information**: Fetch system platform, OS type, release, version, system type, and installation date.
- **Network Information**: Obtain local IP addresses of network interfaces.
- **Export Logs**: Export retrieved information in JSON or CSV formats.
- **User-Friendly Interface**: Simple and intuitive GUI for easy navigation.

## Requirements

- Python 3.x
- Required Python packages: `tkinter`, `platform`, `socket`, `json`, `csv`, `os`, `psutil`, `datetime`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PongGone/win-host-handler.git
   ```

2. Navigate to the project directory:
   ```bash
   cd win-host-handler
   ```

3. Run the application:
   ```bash
   python win_host_handler.py
   ```

## Usage

1. Launch the application by executing the `win_host_handler.py` file.
2. Click on the desired category (Host, System, or Network) to retrieve information.
3. View the retrieved information in the application's interface.
4. Optionally, export the logs in either JSON or CSV format using the provided buttons.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

This application is developed and maintained by [PongGone](https://github.com/PongGone).
