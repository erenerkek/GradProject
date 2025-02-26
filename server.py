import socket
import sqlite3
import threading
import json

# Veritabanı bağlantısı
conn = sqlite3.connect('sys_monitor.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS computers
             (serial TEXT PRIMARY KEY, cpu REAL, ram REAL, disk REAL, ip TEXT, port INTEGER)''')
conn.commit()

# Sunucu Ayarları
HOST = '0.0.0.0'  # Tüm ağ bağlantılarını dinle
PORT = 65432

# Socket oluşturma
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def handle_client(client_socket, addr):
    print(f"[+] {addr} bağlandı.")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            # Gelen veriyi işle (JSON formatında bekliyoruz)
            data = json.loads(data)
            serial = data['serial']
            
            # Veritabanına kaydet/güncelle
            c.execute("REPLACE INTO computers VALUES (?, ?, ?, ?, ?, ?)",
                      (serial, data['cpu'], data['ram'], data['disk'], addr[0], addr[1]))
            conn.commit()
            
            # Tüm bilgisayarların verisini gönder
            c.execute("SELECT * FROM computers")
            rows = c.fetchall()
            computers = [{'serial': row[0], 'cpu': row[1], 'ram': row[2], 'disk': row[3]} for row in rows]
            client_socket.send(json.dumps(computers).encode('utf-8'))
            
    except Exception as e:
        print(f"[-] Hata: {e}")
    finally:
        client_socket.close()
        print(f"[-] {addr} bağlantısı kesildi.")

print("[*] Sunucu dinleniyor...")
while True:
    client_socket, addr = server.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()