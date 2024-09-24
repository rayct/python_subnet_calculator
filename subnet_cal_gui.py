import tkinter as tk
from tkinter import messagebox
import ipaddress
import time

# Function to log results to a file
def log_results(ip, subnet_prefix, network_address, broadcast_address, first_usable, last_usable, total_hosts, next_network_address):
    with open("log.txt", "a") as log_file:
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"IP Address: {ip}\n")
        log_file.write(f"Subnet Prefix: /{subnet_prefix}\n")
        log_file.write(f"Network Address: {network_address}\n")
        log_file.write(f"Broadcast Address: {broadcast_address}\n")
        log_file.write(f"First Usable IP: {first_usable}\n")
        log_file.write(f"Last Usable IP: {last_usable}\n")
        log_file.write(f"Total Usable Hosts: {total_hosts}\n")
        log_file.write(f"Next Network Address: {next_network_address}\n")
        log_file.write("=" * 40 + "\n")  # Divider between entries

# Function to perform subnet calculations
def calculate_subnet():
    try:
        ip = ip_entry.get()
        subnet_prefix = int(prefix_entry.get())

        # Create an IP network object
        network = ipaddress.IPv4Network(f"{ip}/{subnet_prefix}", strict=False)

        # Extract information
        network_address = network.network_address
        broadcast_address = network.broadcast_address
        first_usable = list(network.hosts())[0]
        last_usable = list(network.hosts())[-1]
        total_hosts = network.num_addresses - 2  # -2 for network and broadcast addresses
        next_network_address = network_address + network.num_addresses

        # Display results in the GUI
        result_text.set(f"Network Address: {network_address}\n"
                        f"Broadcast Address: {broadcast_address}\n"
                        f"First Usable IP: {first_usable}\n"
                        f"Last Usable IP: {last_usable}\n"
                        f"Total Usable Hosts: {total_hosts}\n"
                        f"Next Network Address: {ipaddress.IPv4Address(next_network_address)}")

        # Log the results to the log.txt file
        log_results(ip, subnet_prefix, network_address, broadcast_address, first_usable, last_usable, total_hosts, ipaddress.IPv4Address(next_network_address))

    except Exception as e:
        messagebox.showerror("Error", f"Invalid Input: {e}")

# GUI Setup
app = tk.Tk()
app.title("Subnet Calculator")
app.geometry("600x500")
app.configure(bg="#f5f5f5")

# Title Label
title_label = tk.Label(app, text="Network Subnet Calculator", font=("Arial", 20, "bold"), bg="#f5f5f5", fg="#333")
title_label.pack(pady=20)

# IP Address Entry
ip_label = tk.Label(app, text="Enter IP Address:", font=("Arial", 12), bg="#f5f5f5", fg="#333")
ip_label.pack()
ip_entry = tk.Entry(app, font=("Arial", 12), width=25, bd=2, relief="solid")
ip_entry.pack(pady=5)

# Subnet Prefix Entry
prefix_label = tk.Label(app, text="Enter Subnet Prefix (e.g., 24):", font=("Arial", 12), bg="#f5f5f5", fg="#333")
prefix_label.pack()
prefix_entry = tk.Entry(app, font=("Arial", 12), width=25, bd=2, relief="solid")
prefix_entry.pack(pady=5)

# Calculate Button
calculate_button = tk.Button(app, text="Calculate", font=("Arial", 12, "bold"), bg="#ff8000", fg="white", command=calculate_subnet)
calculate_button.pack(pady=20)

# Result Text Display
result_text = tk.StringVar()
result_label = tk.Label(app, textvariable=result_text, font=("Arial", 12), bg="#f5f5f5", fg="#333", justify="left")
result_label.pack(pady=10)

# Version and Author Info at Bottom Right
version_author_label = tk.Label(app, text="Version: 1.0.0 | Author: rayturner.dev", font=("Arial", 10), bg="#f5f5f5", fg="#333", anchor="se")
version_author_label.pack(side="bottom", anchor="se", padx=10, pady=10)

# Start the main loop
app.mainloop()
