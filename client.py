# ...existing code...
import tkinter as tk
from tkinter import ttk
import psutil
import socket
import json
import time
from threading import Thread

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client App")
        
        # IP Address Label
        self.ip_label = tk.Label(root, text="IP Address: Not Connected")
        self.ip_label.pack()

        # Other GUI elements
        self.serial_entry = tk.Entry(root)
        self.serial_entry.pack()
        
        self.tree = ttk.Treeview(root, columns=('serial', 'cpu', 'ram', 'disk'), show='headings')
        self.tree.heading('serial', text='Serial')
        self.tree.heading('cpu', text='CPU')
        self.tree.heading('ram', text='RAM')
        self.tree.heading('disk', text='Disk')
        self.tree.pack()

        self.is_connected = False

    def get_system_info(self):
        return {
            'cpu': psutil.cpu_percent(interval=1),
            'ram': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent
        }

    def send_data(self):
        while self.is_connected:
            try:
                data = self.get_system_info()
                data['serial'] = self.serial_entry.get()
                self.socket.send(json.dumps(data).encode('utf-8'))
                
                # Sunucudan güncel verileri al
                response = self.socket.recv(4096).decode('utf-8')
                computers = json.loads(response)
                
                # Tabloyu güncelle
                self.tree.delete(*self.tree.get_children())
                for comp in computers:
                    self.tree.insert('', 'end', values=(comp['serial'], comp['cpu'], comp['ram'], comp['disk']))
                
                time.sleep(1)
            except Exception as e:
                print(f"Hata: {e}")
                self.is_connected = False
                break

    def connect_to_server(self):
        if not self.is_connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ip_address = self.ip_entry.get()
                self.socket.connect((ip_address, 65432))
                self.is_connected = True
                self.ip_label.config(text=f"IP Address: {ip_address}")
                Thread(target=self.send_data, daemon=True).start()
            except Exception as e:
                print(f"Connection Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()