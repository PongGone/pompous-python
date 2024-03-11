import tkinter as tk
import requests
import re
from socket import gethostbyname, gaierror
import webbrowser
from tkinter import filedialog
from tkinter import messagebox
import threading
import time
from datetime import datetime

class EndpointCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Endpoint Checker")
        self.root.geometry("900x600")  # GUI size
        
        # Title and creator label
        self.title_label = tk.Label(root, text="Endpoint Checker", font=("Helvetica", 24))
        self.title_label.pack()
        self.creator_label = tk.Label(root, text="Made by PongGone", font=("Helvetica", 10), fg="blue", cursor="hand2")
        self.creator_label.pack()
        self.creator_label.bind("<Button-1>", self.open_github_profile)

        # Endpoint input
        self.endpoint_label = tk.Label(root, text="Enter endpoint URL or IP:")
        self.endpoint_label.pack()
        self.endpoint_entry = tk.Entry(root, width=70)
        self.endpoint_entry.pack()

        # Check button
        self.check_button = tk.Button(root, text="Check Endpoint", command=self.check_endpoint)
        self.check_button.pack()

        # User input logs display
        self.user_input_logs_label = tk.Label(root, text="User Logs:")
        self.user_input_logs_label.pack()
        self.user_input_logs_text = tk.Text(root, width=100, height=10)
        self.user_input_logs_text.pack()

        # Background check logs display
        self.background_logs_label = tk.Label(root, text="Background Logs:")
        self.background_logs_label.pack()
        self.background_logs_text = tk.Text(root, width=100, height=10)
        self.background_logs_text.pack()

        # Clear logs button for user input logs
        self.clear_user_input_logs_button = tk.Button(root, text="Clear User Input Logs", command=self.clear_user_input_logs)
        self.clear_user_input_logs_button.pack()

        # Clear logs button for background check logs
        self.clear_background_logs_button = tk.Button(root, text="Clear Background Check Logs", command=self.clear_background_logs)
        self.clear_background_logs_button.pack()

        # Start background thread for endpoint checking
        self.background_thread = threading.Thread(target=self.background_checking)
        self.background_thread.daemon = True
        self.background_thread.start()

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

            request_time = datetime.now()
            response = requests.get(url)
            response_time = datetime.now()

            status_code = response.status_code
            response_elapsed = response_time - request_time

            request_method = response.request.method
            request_url = response.request.url

            log_message = f"Endpoint: {endpoint_ip}\nRequest Time: {request_time}\nResponse Time: {response_time}\nElapsed Time: {response_elapsed}\nHTTP Response Code: {status_code} - {self.get_status_description(status_code)}"
            log_message += f"\nRequest Method: {request_method}\nRequest URL: {request_url}\n"

            self.update_user_input_logs(log_message)

        except gaierror:
            self.update_user_input_logs(f"Error resolving DNS name: {endpoint}\n\n")
        except Exception as e:
            self.update_user_input_logs(f"Error checking endpoint: {str(e)}\n\n")

    def clear_user_input_logs(self):
        self.user_input_logs_text.delete(1.0, tk.END)

    def clear_background_logs(self):
        self.background_logs_text.delete(1.0, tk.END)

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

    def background_checking(self):
        hosts = ('https://www.evernorth.com', 
                 'https://www.express-scripts.com', 
                 'https://www.cigna.com' )

        while True:
            for host in hosts:
                self.check_background_endpoint(host)
                time.sleep(2)

    def check_background_endpoint(self, host):
        try:
            request_time = datetime.now()
            response = requests.get(host, verify=True, timeout=(0.5, 0.5))
            response_time = datetime.now()
            response_elapsed = response_time - request_time
            
            log_message = f"Background Check - Endpoint: {host}\nRequest Time: {request_time}\nResponse Time: {response_time}\nElapsed Time: {response_elapsed}\nHTTP Response Code: {response.status_code} - {self.get_status_description(response.status_code)}\n"
            self.update_background_logs(log_message)
        except (requests.ConnectionError, requests.Timeout) as err:
            timestamp = datetime.now()
            log_message = f"Background Check - Error checking endpoint {host}: {err}\nTimestamp: {timestamp}\n"
            self.update_background_logs(log_message)
        except Exception as e:
            timestamp = datetime.now()
            log_message = f"Background Check - Error checking endpoint {host}: {str(e)}\nTimestamp: {timestamp}\n"
            self.update_background_logs(log_message)

    def update_user_input_logs(self, log_message):
        self.user_input_logs_text.insert(tk.END, log_message + "\n\n")

    def update_background_logs(self, log_message):
        self.background_logs_text.insert(tk.END, log_message + "\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = EndpointCheckerApp(root)
    root.mainloop()
