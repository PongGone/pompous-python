# PC Health Check

PC Health Check is a Python application for generating system health reports. It provides insights into disk health, system performance, and network connection status.

## Features

- **Disk Health**: Check disk usage, including total, used, and free space, and percentage of usage.
- **System Performance**: Monitor CPU and memory usage.
- **Network Connection**: Detect connection type (Ethernet/Wi-Fi) and VPN status.
- **Generate Report**: Create a comprehensive system health report with recommendations.
- **User-Friendly Interface**: Simple and intuitive GUI for easy operation.

## Requirements

- Python 3.x
- Required Python packages: `tkinter`, `ctypes`, `webbrowser`, `datetime`, `socket`, `subprocess`, `psutil`, `platform`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/PongGone/pc-healthcheck.git
   ```

2. Navigate to the project directory:
   ```bash
   cd pc-healthcheck
   ```

3. Run the application:
   ```bash
   python pc_healthcheck.py
   ```

## Usage

1. Launch the application by executing the `pc_healthcheck.py` file.
2. Click on the "Generate Report" button to create a system health report.
3. View the generated report (`system_health_report.txt`) for disk health, system performance, network connection, and recommendations.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

This application is developed and maintained by [PongGone](https://github.com/PongGone).
