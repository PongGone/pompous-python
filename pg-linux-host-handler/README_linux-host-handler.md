# Linux Host Handler

Linux Host Handler is a Python application designed to retrieve and display information about a Linux host. It provides details such as host name, processor, installed RAM, platform, OS type, network information, and more.

## Features

- **Host Information**: Retrieve information about the host, including host name, processor, installed RAM, device ID, and product ID.
- **System Information**: Get details about the platform, OS type, release, version, system type, and installation date.
- **Network Information**: Fetch local IP addresses for network interfaces.
- **Logs Display**: View the retrieved information in the application interface.
- **Export Logs**: Export logs in either JSON or CSV format for further analysis.

## Requirements

- Python 3.x
- Required Python packages: `tkinter`, `requests`, `socket`, `json`, `csv`, `os`, `psutil`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PongGone/linux-host-handler.git
   ```

2. Navigate to the project directory:
   ```bash
   cd linux-host-handler
   ```

3. Run the application:
   ```bash
   python host_handler.py
   ```

## Usage

1. Launch the application by executing the `host_handler.py` file.
2. Click on the desired category (Host, System, Network) to retrieve information about the Linux host.
3. View the logs displayed in the application interface.
4. Optionally, export the logs in either JSON or CSV format using the "Export Logs" button.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

This application is developed and maintained by [PongGone](https://github.com/PongGone).
