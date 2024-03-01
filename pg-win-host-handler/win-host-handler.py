import tkinter as tk
from tkinter import messagebox, filedialog
import platform
import socket
import json
import csv
import os
import psutil
from datetime import datetime

class HostHandlerApp:
    """A simple application to retrieve and display Windows host information."""
    def __init__(self, root, width=900, height=700):
        self.root = root
        self.root.title("Windows Host Handler")
        self.root.geometry(f"{width}x{height}")
        
        self.host_identifier = self.get_device_name()  # Store the host identifier
        self.host_count = {}  # Dictionary to keep track of counts for each host
        self.logs = ""  # Initialize logs as empty string
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets."""
        self.label_title = tk.Label(self.root, text="Windows Host Handler", font=("Helvetica", 16))
        self.label_title.pack()

        self.label_author = tk.Label(self.root, text="Made by PongGone", font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.label_author.pack()
        self.label_author.bind("<Button-1>", lambda e: self.open_github())
        
        self.label_instructions = tk.Label(self.root, text="Instructions:", font=("Helvetica", 10, "bold"))
        self.label_instructions.pack()

        self.label_instructions_text = tk.Label(self.root, text="Click on the category to retrieve host local information.", font=("Helvetica", 10))
        self.label_instructions_text.pack()

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        self.btn_get_host_info = tk.Button(button_frame, text="Host", command=self.get_host_info)
        self.btn_get_host_info.pack(side="left", padx=5)

        self.btn_get_system_info = tk.Button(button_frame, text="System", command=self.get_system_info)
        self.btn_get_system_info.pack(side="left", padx=5)

        self.btn_get_network_info = tk.Button(button_frame, text="Network", command=self.get_network_info)
        self.btn_get_network_info.pack(side="left", padx=5)

        self.label_line_break = tk.Label(self.root, text="\n")
        self.label_line_break.pack()

        self.label_logs = tk.Label(self.root, text="Logs:", font=("Helvetica", 10, "bold"))
        self.label_logs.pack()

        self.text_logs = tk.Text(self.root, height=15, width=80)
        self.text_logs.pack()

        self.btn_clear_logs = tk.Button(self.root, text="Clear Logs", command=self.clear_logs)
        self.btn_clear_logs.pack(pady=(5, 10))

        self.label_export = tk.Label(self.root, text="Export Details:", font=("Helvetica", 10, "bold"))
        self.label_export.pack()

        self.label_export_text = tk.Label(self.root, text="File formats supported\nCSV, JSON", font=("Helvetica", 10))
        self.label_export_text.pack()

        self.btn_export_logs = tk.Button(self.root, text="Export Logs", command=self.export_logs)
        self.btn_export_logs.pack(pady=(0, 10))

    def open_github(self):
        """Open GitHub repository."""
        os.system("start https://github.com/PongGone")

    def get_host_info(self):
        """Retrieve host information."""
        try:
            host_info = {
                "Host Name": socket.gethostname(),
                "Host Name": platform.node(),
                "Processor": self.get_cpu_info(),
                "Installed RAM": self.get_formatted_ram_size(psutil.virtual_memory().total),
                "Product ID": self.get_product_id()
            }
            self.update_logs(host_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch host information: {e}")

    def get_system_info(self):
        """Retrieve system information."""
        try:
            system_info = {
                "Platform": platform.platform(),
                "OS Type": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "System Type": self.get_system_type(),
                "Installed on": self.get_installed_on()
            }
            self.update_logs(system_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch system information: {e}")

    def get_network_info(self):
        """Retrieve network information."""
        try:
            network_info = {}
            interfaces = psutil.net_if_addrs()
            for interface, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        network_info[f"Local IP Address ({interface})"] = addr.address
            self.update_logs(network_info)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch network information: {e}")

    def update_logs(self, info_dict):
        """Update logs with new information."""
        for key, value in info_dict.items():
            if key == "Hostname":
                host = value
                if host in self.host_count:
                    self.host_count[host] += 1
                else:
                    self.host_count[host] = 1
            else:
                self.logs += f"{key}: {value}\n"
        self.logs += "\n"  # Add a break between logs
        self.display_logs()

    def display_logs(self):
        """Display information in the logs."""
        self.text_logs.delete('1.0', tk.END)
        self.text_logs.insert(tk.END, self.logs)

    def clear_logs(self):
        """Clear logs."""
        self.logs = ""
        self.display_logs()

    def export_logs(self):
        """Export logs."""
        try:
            filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=(("JSON files", "*.json"), ("CSV files", "*.csv")))
            if filename:
                if filename.endswith(".json"):
                    self.export_json(filename)
                elif filename.endswith(".csv"):
                    self.export_csv(filename)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs: {e}")

    def export_json(self, filename):
        """Export logs as JSON."""
        logs_dict = {}
        logs_list = self.logs.split('\n')
        for log in logs_list:
            log = log.strip()
            if log:
                key, value = log.split(": ", 1)
                logs_dict[key] = value
        with open(filename, "w") as file:
            json.dump({"host_count": self.host_count, "logs": logs_dict}, file, indent=4)

    def export_csv(self, filename):
        """Export logs as CSV."""
        logs_list = [line.split(": ", 1) for line in self.logs.split('\n') if line.strip()]
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(logs_list)

    def get_formatted_ram_size(self, bytes_size):
        """Format RAM size."""
        sizes = ["B", "KB", "MB", "GB", "TB"]
        index = 0
        while bytes_size > 1024 and index < len(sizes) - 1:
            bytes_size /= 1024.0
            index += 1
        return "{:.2f} {}".format(bytes_size, sizes[index])

    def get_cpu_info(self):
        """Retrieve CPU information."""
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for processor in c.Win32_Processor():
                return f"{processor.Name.strip()} {processor.MaxClockSpeed}MHz"
        elif platform.system() == "Linux":
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.strip() and line.split(':')[0].strip() == "model name":
                        return line.split(':')[1].strip()
        elif platform.system() == "Darwin":
            return platform.processor()
        return platform.processor()

    def get_product_id(self):
        """Retrieve product ID."""
        if platform.system() == "Windows":
            try:
                import winreg
                reg_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                product_id, _ = winreg.QueryValueEx(reg_key, "ProductId")
                winreg.CloseKey(reg_key)
                return product_id
            except Exception as e:
                print(f"Error retrieving Product ID: {e}")
                return "N/A"
        return "N/A"

    def get_system_type(self):
        """Retrieve system type."""
        if platform.system() == "Windows":
            architecture, _ = platform.architecture()
            return f"{architecture} operating system"
        return "N/A"

    def get_installed_on(self):
        """Retrieve installed on date."""
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for os in c.Win32_OperatingSystem():
                installed_on = datetime.strptime(os.InstallDate[:-11], "%Y%m%d%H%M%S").strftime("%m/%d/%Y %I:%M:%S %p")
                return installed_on
        return "N/A"

    def get_device_name(self):
        """Retrieve device name."""
        if platform.system() == "Windows":
            try:
                import winreg
                reg_path = r"SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName"
                reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                device_name, _ = winreg.QueryValueEx(reg_key, "ComputerName")
                winreg.CloseKey(reg_key)
                return device_name
            except Exception as e:
                print(f"Error retrieving device name from registry: {e}")
                return socket.gethostname()
        else:
            return socket.gethostname()

if __name__ == "__main__":
    root = tk.Tk()
    app = HostHandlerApp(root)
    root.mainloop()
