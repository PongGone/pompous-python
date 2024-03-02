import tkinter as tk
from tkinter import messagebox
import ctypes
import webbrowser
import datetime
import socket
import subprocess
import psutil
import platform

class SystemHealthApp:
    def __init__(self, master):
        self.master = master
        master.title("PC Health Check")
        master.geometry("700x200")

        # Title
        self.title_label = tk.Label(master, text="PC Health Check", font=("Arial", 18, "bold"))
        self.title_label.pack()

        # Made by link
        self.github_link = tk.Label(master, text="Made by PongGone", fg="blue", cursor="hand2")
        self.github_link.pack()
        self.github_link.bind("<Button-1>", self.open_github)

        # Instructions
        self.instruction_label = tk.Label(master, text="Instructions:\n"
                                                        "Click 'Generate Report' to create a report file.\n"
                                                        "Disk, System, and Network Health",
                                           font=("Arial", 12))  # Increase font size
        self.instruction_label.pack(pady=10)

        # Generate Report Button
        self.generate_report_button = tk.Button(master, text="Generate Report", command=self.generate_report, font=("Arial", 14))
        self.generate_report_button.pack()

    def open_github(self, event):
        webbrowser.open_new("https://github.com/PongGone")

    def get_volume_label(self, drive_letter):
        MAX_VOL_NAME_SIZE = 256
        volume_name_buffer = ctypes.create_unicode_buffer(MAX_VOL_NAME_SIZE)
        file_system_flags = ctypes.c_ulong()
        ctypes.windll.kernel32.GetVolumeInformationW(ctypes.c_wchar_p(drive_letter + ":\\"),
                                                      volume_name_buffer, MAX_VOL_NAME_SIZE,
                                                      None, None, ctypes.byref(file_system_flags), None, 0)
        volume_label = volume_name_buffer.value.strip()  # Strip whitespace
        return volume_label if volume_label else "N/A"  # Return "N/A" if label is blank or unreadable

    def check_disk_health(self):
        disk_health_info = []

        try:
            disk_partitions = psutil.disk_partitions(all=True)

            for partition in disk_partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                device_name = self.get_volume_label(partition.device[:1])  # Get volume label for the drive letter
                disk_info = {
                    "Drive Label": partition.device,
                    "Device Name": device_name,
                    "Total": f"{disk_usage.total / (1024 ** 3):.2f} GB",
                    "Used": f"{disk_usage.used / (1024 ** 3):.2f} GB",
                    "Free": f"{disk_usage.free / (1024 ** 3):.2f} GB",
                    "Usage Percentage": f"{disk_usage.percent}%",
                    "Free Space Percentage": f"{100 - disk_usage.percent}%"  # Percentage of free space
                }
                disk_health_info.append(disk_info)

        except PermissionError:
            messagebox.showerror("Error", "Permission denied accessing one or more disk partitions.")
            return []

        except Exception as e:
            messagebox.showerror("Error", f"Error checking disk health: {str(e)}")
            return []

        return disk_health_info

    def check_system_performance(self):
        try:
            cpu_usage = psutil.cpu_percent(interval=1)  # Get CPU usage as a percentage
            memory_usage = psutil.virtual_memory().percent  # Get memory usage as a percentage

            system_performance_info = {
                "CPU Usage": f"{cpu_usage}%",
                "Memory Usage": f"{memory_usage}%"  # Added memory usage metric
            }

            return system_performance_info

        except Exception as e:
            messagebox.showerror("Error", f"Error checking system performance: {str(e)}")
            return {}

    def check_network_connection(self):
        try:
            # Determine connection type (Ethernet/Wi-Fi)
            connection_type = "Unknown"
            cmd = "ipconfig" if platform.system() == "Windows" else "ifconfig"
            result = subprocess.run(cmd, capture_output=True, text=True)
            if "Ethernet adapter" in result.stdout:
                connection_type = "Ethernet"
            elif "Wi-Fi adapter" in result.stdout:
                connection_type = "Wi-Fi"

            # Determine VPN connection status
            vpn_status = "No"
            for conn in psutil.net_connections():
                if conn.raddr and conn.laddr and conn.laddr.ip == '127.0.0.1' and conn.raddr.ip == '127.0.0.1':
                    vpn_status = "Yes"
                    break

            network_info = {
                "Connection Type": connection_type,
                "VPN Connected": vpn_status
            }

            return network_info

        except Exception as e:
            messagebox.showerror("Error", f"Error checking network connection: {str(e)}")
            return {}

    def generate_report(self):
        try:
            report = []

            # Get current time and date
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Get hostname
            hostname = socket.gethostname()

            # Overview Report
            report.append(f"Overview Report\nTime: {current_time}\nHostName: {hostname}\n")

            # Check Disk Health
            disk_health_info = self.check_disk_health()
            if disk_health_info:
                report.append("[Disk Health]")
                for disk_info in disk_health_info:
                    report.append("\n".join([f"{key}: {value}" for key, value in disk_info.items()]))
                disk_count = len(disk_health_info)
                report.append(f"\nThere {'is' if disk_count == 1 else 'are'} a total of ({disk_count}) {'data drive' if disk_count == 1 else 'data drives'} on the host.")

            # Check System Performance
            system_performance_info = self.check_system_performance()
            if system_performance_info:
                report.append("\n\n[System Performance]")
                report.append("\n".join([f"{key}: {value}" for key, value in system_performance_info.items()]))

            # Check Network Connection
            network_connection_info = self.check_network_connection()
            if network_connection_info:
                report.append("\n\n[Network Connection]")
                report.append("\n".join([f"{key}: {value}" for key, value in network_connection_info.items()]))

            # Append recommendations in paragraph form
            recommendations = []

            # Add recommendations based on disk health
            if disk_health_info:
                for disk_info in disk_health_info:
                    free_space_percentage = float(disk_info["Free Space Percentage"][:-1])
                    if free_space_percentage < 20:
                        recommendations.append(f"Recommendation for {disk_info['Drive Label']}: Disk space is low. Consider cleaning up or expanding storage.")
                    elif free_space_percentage < 50:
                        recommendations.append(f"Recommendation for {disk_info['Drive Label']}: Disk space is getting low. Consider cleaning up or expanding storage.")
                    else:
                        recommendations.append(f"Recommendation for {disk_info['Drive Label']}: Disk space is sufficient.")
            
            # Add recommendations based on network connection
            if network_connection_info["Connection Type"] == "Ethernet":
                recommendations.append("You are connected via Ethernet. Ensure the cable is securely plugged in.")
            elif network_connection_info["Connection Type"] == "Wi-Fi":
                recommendations.append("You are connected via Wi-Fi. Make sure you have a strong signal.")
            if network_connection_info["VPN Connected"] == "Yes":
                recommendations.append("You are connected to a VPN. Be cautious of network security and privacy.")

            if recommendations:
                report.append("\n\n[Recommendations]")
                report.append("\n" + "\n".join(recommendations))

            with open("system_health_report.txt", "w") as f:
                f.write("\n\n".join(report))

            messagebox.showinfo("Report Generation", "Report generated successfully and saved as 'system_health_report.txt'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")

def main():
    root = tk.Tk()
    app = SystemHealthApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
