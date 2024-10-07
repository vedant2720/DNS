
import socket
import dns.resolver
import tkinter as tk
from tkinter import Text, Scrollbar

class DNSServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("DNS Server Log")

        self.log_text = Text(master, height=20, width=50)
        self.log_text.pack(side=tk.LEFT, fill=tk.Y)

        self.scrollbar = Scrollbar(master, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # Define the DNS server address and port
        self.server_address = ('127.0.0.1', 12345)

        # Create a UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.server_address)

        self.log_text.insert(tk.END, f"DNS server listening on {self.server_address}\n")

        self.listen()

    def listen(self):
        while True:
            # Receive data from the client
            data, client_address = self.server_socket.recvfrom(1024)
            domain_name = data.decode()

            try:
                # Use dnspython to resolve the domain name to an IP address
                answers = dns.resolver.resolve(domain_name, 'A')
                ip_addresses = [answer.address for answer in answers]

                # Log the request and resolved IP addresses
                log_message = f"Received request for {domain_name} from {client_address}\n"
                log_message += f"Resolved {domain_name} to {', '.join(ip_addresses)}\n"
                self.log_text.insert(tk.END, log_message)
                self.log_text.yview(tk.END)

                # Send the resolved IP addresses back to the client
                self.server_socket.sendto(', '.join(ip_addresses).encode(), client_address)

            except dns.resolver.NXDOMAIN:
                # If an exception occurs (e.g., domain not found), log an error message
                log_message = f"Invalid domain provided: {domain_name} from {client_address}\n"
                self.log_text.insert(tk.END, log_message)
                self.log_text.yview(tk.END)

                # Send an error message back to the client
                error_message = "Invalid domain"
                self.server_socket.sendto(error_message.encode(), client_address)

if __name__ == "__main__":
    root = tk.Tk()
    app = DNSServerGUI(root)
    root.mainloop()

