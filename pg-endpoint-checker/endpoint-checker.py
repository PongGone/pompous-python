import tkinter as tk
import requests
import re
from socket import gethostbyname, gaierror
import webbrowser
from tkinter import filedialog
from tkinter import messagebox

class EndpointCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Endpoint Checker")
        self.root.geometry("900x700")  # GUI size
        
        # Title and creator label
        self.title_label = tk.Label(root, text="Endpoint Checker", font=("Helvetica", 24))
        self.title_label.pack()
        self.creator_label = tk.Label(root, text="Made by PongGone", font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.creator_label.pack()
        self.creator_label.bind("<Button-1>", self.open_github_profile)

        # Instructions
        self.instructions_label = tk.Label(root, text="Instructions:\n1. Enter the endpoint URL or IP in the box below.\n2. Click 'Check Endpoint' to check the status.")
        self.instructions_label.pack()

        # Endpoint input
        self.endpoint_entry = tk.Entry(root, width=70)
        self.endpoint_entry.pack()

        # Check button
        self.check_button = tk.Button(root, text="Check Endpoint", command=self.check_endpoint)
        self.check_button.pack()

        # Logs display
        self.logs_label = tk.Label(root, text="Logs:")
        self.logs_label.pack()
        self.logs_text = tk.Text(root, width=100, height=20)
        self.logs_text.pack()

        # Clear logs button
        self.clear_logs_button = tk.Button(root, text="Clear Logs", command=self.clear_logs)
        self.clear_logs_button.pack()

        # Line break
        self.line_break_label = tk.Label(root, text="\n")
        self.line_break_label.pack()

        # Export logs button
        self.export_logs_button = tk.Button(root, text="Export Logs", command=self.export_logs)
        self.export_logs_button.pack()

        # Export logs instructions
        self.export_logs_instructions_label = tk.Label(root, text="Export Details:\nFile formats supported")
        self.export_logs_instructions_label.pack()

        # File format options
        self.file_format_options_label = tk.Label(root, text="CSV, JSON")
        self.file_format_options_label.pack()

    def check_endpoint(self):
        endpoint = self.endpoint_entry.get()
        try:
            # Check if the endpoint is an IP address or a domain name
            ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
            if ip_pattern.match(endpoint):
                # If it's an IP address, check if it starts with 'http://' or 'https://'
                if endpoint.startswith("http://") or endpoint.startswith("https://"):
                    url = endpoint
                else:
                    # Assume it's an IP address without protocol prefix
                    url = f"http://{endpoint}"
                    
                endpoint_ip = endpoint
            else:
                # Check if the endpoint starts with 'http://' or 'https://'
                if endpoint.startswith("http://") or endpoint.startswith("https://"):
                    url = endpoint
                else:
                    # Assume it's a domain name without protocol prefix
                    url = f"https://{endpoint}"
                    
                # Remove protocol prefix for DNS resolution
                endpoint_without_protocol = endpoint.replace("http://", "").replace("https://", "")
                endpoint_ip = gethostbyname(endpoint_without_protocol)

            response = requests.get(url)
            status_code = response.status_code
            response_time = response.elapsed.total_seconds()

            request_method = response.request.method
            request_url = response.request.url

            log_message = f"Endpoint: {endpoint_ip}\nResponse Time: {response_time:.2f} seconds\nHTTP Response Code: {status_code} - {self.get_status_description(status_code)}"
            log_message += f"\nRequest Method: {request_method}\nRequest URL: {request_url}\n"

            self.logs_text.insert(tk.END, log_message + "\n\n")

        except gaierror:
            self.logs_text.insert(tk.END, f"Error resolving DNS name: {endpoint}\n\n")
        except Exception as e:
            self.logs_text.insert(tk.END, f"Error checking endpoint: {str(e)}\n\n")

    def clear_logs(self):
        self.logs_text.delete(1.0, tk.END)

    def export_logs(self):
        logs = self.logs_text.get("1.0", tk.END)
        if logs.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("JSON files", "*.json")))
            if file_path:
                try:
                    with open(file_path, 'w') as file:
                        file.write(logs)
                    messagebox.showinfo("Export Logs", "Logs exported successfully.")
                except Exception as e:
                    messagebox.showerror("Export Logs", f"Error exporting logs: {str(e)}")
        else:
            messagebox.showwarning("Export Logs", "No logs to export.")

    def get_status_description(self, status_code):
        descriptions = {
            100: "Continue",
            101: "Switching Protocols",
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            307: "Temporary Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Payload Too Large",
            414: "URI Too Long",
            415: "Unsupported Media Type",
            416: "Range Not Satisfiable",
            417: "Expectation Failed",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported",
        }
        return descriptions.get(status_code, "Unknown")

    def open_github_profile(self, event):
        webbrowser.open_new("https://github.com/PongGone")

if __name__ == "__main__":
    root = tk.Tk()
    app = EndpointCheckerApp(root)
    root.mainloop()
