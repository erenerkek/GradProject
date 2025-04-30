import os
import wmi
import sys
import uuid
import hashlib
import asyncio
import websockets
import psutil
import json
import threading
import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySideExtn import *
from qt_material import apply_stylesheet

from ui_untitled import Ui_MainWindow

# Unique Kod Oluşturma
def generate_unique_id():
    mac = uuid.getnode()
    unique_id = hashlib.md5(str(mac).encode()).hexdigest()[:12]
    config_file = "device_id.txt"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read().strip()
    else:
        with open(config_file, "w") as f:
            f.write(unique_id)
    return unique_id

# WebSocket Sunucusu        
async def send_system_info(websocket, path):
    print("WebSocket sunucusu veri gönderimine başladı")
    while True:
        processes = []
        for x in psutil.pids():
            try:
                p = psutil.Process(x)
                processes.append({
                    'pid': p.pid,
                    'name': p.name(),
                    'status': p.status(),
                    'create_time': datetime.datetime.fromtimestamp(p.create_time(), datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception:
                continue
        
        net_stats = {}
        for x in psutil.net_if_stats():
            net_stats[x] = {
                'isup': str(psutil.net_if_stats()[x].isup),
                'duplex': str(psutil.net_if_stats()[x].duplex),
                'speed': str(psutil.net_if_stats()[x].speed),
                'mtu': str(psutil.net_if_stats()[x].mtu)
            }

        net_io = {}
        for x in psutil.net_io_counters(pernic=True):
            net_io[x] = {
                'bytes_sent': psutil.net_io_counters(pernic=True)[x].bytes_sent,
                'bytes_recv': psutil.net_io_counters(pernic=True)[x].bytes_recv,
                'packets_sent': psutil.net_io_counters(pernic=True)[x].packets_sent,
                'packets_recv': psutil.net_io_counters(pernic=True)[x].packets_recv,
                'errin': psutil.net_io_counters(pernic=True)[x].errin,
                'errout': psutil.net_io_counters(pernic=True)[x].errout,
                'dropin': psutil.net_io_counters(pernic=True)[x].dropin,
                'dropout': psutil.net_io_counters(pernic=True)[x].dropout
            }

        net_addrs = {}
        for x in psutil.net_if_addrs():
            net_addrs[x] = []
            for y in psutil.net_if_addrs()[x]:
                net_addrs[x].append({
                    'family': str(y.family),
                    'address': str(y.address),
                    'netmask': str(y.netmask),
                    'broadcast': str(y.broadcast),
                    'ptp': str(y.ptp)
                })

        net_conns = []
        for x in psutil.net_connections():
            net_conns.append({
                'fd': str(x.fd),
                'family': str(x.family),
                'type': str(x.type),
                'laddr': str(x.laddr),
                'raddr': str(x.raddr),
                'status': str(x.status),
                'pid': str(x.pid)
            })

        data = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'total_ram': psutil.virtual_memory().total / (1024 * 1024 * 1024),
            'free_ram': psutil.virtual_memory().available / (1024 * 1024 * 1024),
            'used_ram': psutil.virtual_memory().used / (1024 * 1024 * 1024),
            'processes': processes,
            'net_stats': net_stats,
            'net_io': net_io,
            'net_addrs': net_addrs,
            'net_conns': net_conns
        }
        await websocket.send(json.dumps(data))
        
        try:
            command = await asyncio.wait_for(websocket.recv(), timeout=0.1)
            command_data = json.loads(command)
            pid = command_data.get('pid')
            action = command_data.get('action')
            if pid and action:
                p = psutil.Process(pid)
                if action == 'suspend':
                    p.suspend()
                elif action == 'resume':
                    p.resume()
                elif action == 'terminate':
                    p.terminate()
                elif action == 'kill':
                    p.kill()
        except asyncio.TimeoutError:
            pass
        await asyncio.sleep(1)

def run_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = websockets.serve(send_system_info, '0.0.0.0', 8765)
    loop.run_until_complete(server)
    loop.run_forever()

# WebSocket İstemcisi
class WebSocketClient(QThread):
    data_received = Signal(dict)
    status_changed = Signal(bool)

    def __init__(self, uri):
        super().__init__()
        self.uri = uri
        self.connected = False

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    self.connected = True
                    self.status_changed.emit(True)
                    self.websocket = websocket
                    while True:
                        data = await websocket.recv()
                        self.data_received.emit(json.loads(data))
            except Exception as e:
                self.connected = False
                self.status_changed.emit(False)
                print(f"Bağlantı hatası: {e}")
                await asyncio.sleep(2)

    def run(self):
        asyncio.run(self.connect())

# Giriş Ekranı UI
class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(600, 400)
        
        self.centralwidget = QWidget(LoginWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        self.top_layout = QHBoxLayout()
        self.device_id_label = QLabel("Benim Kodum: Yükleniyor...")
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Kod gir (örneğin: xyz789)")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP gir (örneğin: 192.168.1.10)")
        self.add_button = QPushButton("Ekle")
        self.top_layout.addWidget(self.device_id_label)
        self.top_layout.addWidget(self.code_input)
        self.top_layout.addWidget(self.ip_input)
        self.top_layout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.top_layout)
        
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(5)
        self.device_table.setHorizontalHeaderLabels(["Kod", "Durum", "Bağlantı", "Kontrol", "İzle"])
        self.verticalLayout.addWidget(self.device_table)
        
        LoginWindow.setCentralWidget(self.centralwidget)

# Giriş Ekranı Mantığı
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        
        self.device_id = generate_unique_id()
        self.ui.device_id_label.setText(f"Benim Kodum: {self.device_id}")
        self.devices = {self.device_id: {"status": "Yerel Bilgisayar", "ip": None, "connected": True}}
        self.load_devices()
        
        self.ui.add_button.clicked.connect(self.add_device)
        
        self.ws_clients = {}
        self.start_monitoring()
        
        self.update_device_table()
        print("LoginWindow başlatıldı")

    def add_device(self):
        device_code = self.ui.code_input.text().strip()
        device_ip = self.ui.ip_input.text().strip()
        if device_code and device_ip and device_code not in self.devices:
            self.devices[device_code] = {"status": "Uzak Bilgisayar", "ip": device_ip, "connected": False}
            self.start_monitoring_device(device_code)
            self.save_devices()
            self.update_device_table()
            self.ui.code_input.clear()
            self.ui.ip_input.clear()

    def start_monitoring(self):
        for device_code, info in self.devices.items():
            if info["ip"]:
                self.start_monitoring_device(device_code)

    def start_monitoring_device(self, device_code):
        if device_code not in self.ws_clients:
            uri = f"ws://{self.devices[device_code]['ip']}:8765"
            client = WebSocketClient(uri)
            client.status_changed.connect(lambda status, code=device_code: self.update_device_status(code, status))
            client.start()
            self.ws_clients[device_code] = client
            print(f"{device_code} için WebSocket istemci başlatıldı")

    def update_device_status(self, device_code, status):
        self.devices[device_code]["connected"] = status
        self.update_device_table()

    def update_device_table(self):
        self.ui.device_table.setRowCount(0)
        for i, (device_code, info) in enumerate(self.devices.items()):
            self.ui.device_table.insertRow(i)
            self.ui.device_table.setItem(i, 0, QTableWidgetItem(device_code))
            self.ui.device_table.setItem(i, 1, QTableWidgetItem(info["status"]))
            self.ui.device_table.setItem(i, 2, QTableWidgetItem("Bağlantı Var" if info["connected"] else "Bağlantı Yok"))
            
            check_btn = QPushButton("Kontrol Et")
            check_btn.clicked.connect(lambda checked, code=device_code: self.check_device_status(code))
            self.ui.device_table.setCellWidget(i, 3, check_btn)
            
            watch_btn = QPushButton("İzle")
            watch_btn.clicked.connect(lambda checked, code=device_code: self.open_device_monitor(code))
            self.ui.device_table.setCellWidget(i, 4, watch_btn)

    def check_device_status(self, device_code):
        if device_code in self.ws_clients:
            print(f"{device_code} cihazının durumu kontrol edildi: {'Bağlantı Var' if self.devices[device_code]['connected'] else 'Bağlantı Yok'}")
        else:
            self.devices[device_code]["connected"] = True
            print(f"{device_code} yerel cihaz, durum: Bağlantı Var")
        self.update_device_table()

    def save_devices(self):
        with open("devices.json", "w") as f:
            json.dump({k: {"status": v["status"], "ip": v["ip"]} for k, v in self.devices.items()}, f)

    def load_devices(self):
        if os.path.exists("devices.json"):
            with open("devices.json", "r") as f:
                loaded = json.load(f)
                for code, info in loaded.items():
                    self.devices[code] = {"status": info["status"], "ip": info["ip"], "connected": False}

    def open_device_monitor(self, device_code):
        print(f"İzlemeye çalışılan cihaz: {device_code}")
        if device_code in self.devices:
            device_ip = self.devices[device_code].get("ip")
            print(f"IP: {device_ip}")
            self.monitor_window = MainWindow(device_code, device_ip)
            self.monitor_window.show()
        else:
            print(f"Hata: '{device_code}' cihazı bulunamadı!")

# Ana Ekran
class MainWindow(QMainWindow):
    def __init__(self, device_id, device_ip=None):
        super(MainWindow, self).__init__()
        self.device_id = device_id
        self.device_ip = device_ip
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.setWindowIcon(QIcon('icons/airplay.svg'))
        
        self.connection_status = "Bağlantı Var" if not device_ip else "Bağlantı Bekleniyor"
        self.update_window_title()
        
        self.ui.minimize_button.clicked.connect(lambda: self.showMinimized())
        self.ui.exit_button.clicked.connect(lambda: self.close())
        self.ui.window_restore_button.clicked.connect(lambda: self.restore_or_minimize())
        self.ui.cpu_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory))
        self.ui.battery_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))
        self.ui.info_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
        self.ui.activity_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activities))
        self.ui.disk_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))
        self.ui.network_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.networks))
        self.ui.sensor_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors))
        self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory)
        self.ui.MenuButton.clicked.connect(lambda: self.slideLeftMenu())
        
        for w in self.ui.menu_frame.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)

        def moveWindow(event):
            if not self.isMaximized():
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()
        self.ui.header_frame.mouseMoveEvent = moveWindow

        print(f"MainWindow başlatılıyor - Device ID: {self.device_id}, IP: {self.device_ip}")
        if self.device_ip:
            self.ws_client = WebSocketClient(f"ws://{self.device_ip}:8765")
            self.ws_client.data_received.connect(self.update_ui)
            self.ws_client.status_changed.connect(self.update_connection_status)
            self.ws_client.start()
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_local_data)
            self.timer.start(5000)  # Her 1 saniyede bir güncelle
        
        self.show()

    async def connect_websocket(self):
        try:
            self.websocket = await websockets.connect(f"ws://{self.device_ip}:8765")
            print(f"WebSocket bağlantısı kuruldu: {self.device_ip}")
        except Exception as e:
            print(f"WebSocket bağlantı hatası: {e}")

    async def send_command(self, pid, action):
        if hasattr(self, 'websocket') and self.websocket:
            command = json.dumps({'pid': pid, 'action': action})
            await self.websocket.send(command)

    def update_local_data(self):
        print("Yerel veri güncelleme çalışıyor")
        current_widget = self.ui.stackedWidget.currentWidget()
        
        try:
            # CPU ve RAM Sayfası
            if current_widget == self.ui.cpu_and_memory:
                cpuPer = psutil.cpu_percent()
                totalRam = psutil.virtual_memory().total / (1024 * 1024 * 1024)
                freeRam = psutil.virtual_memory().available / (1024 * 1024 * 1024)
                usedRam = psutil.virtual_memory().used / (1024 * 1024 * 1024)
                self.ui.cpu_per.setText(f"{cpuPer}%")
                self.ui.total_ram.setText(f"{totalRam:.2f} GB")
                self.ui.free_ram.setText(f"{freeRam:.2f} GB")
                self.ui.used_ram.setText(f"{usedRam:.2f} GB")
                self.ui.cpu_percentage.setValue(cpuPer)
                self.ui.ram_percentage.setValue((freeRam, usedRam, totalRam - usedRam - freeRam))
                print("CPU ve RAM güncellendi")

            # Süreçler (Activities) Sayfası
            elif current_widget == self.ui.activities:
                self.ui.tableWidget.setRowCount(0)
                for x in psutil.pids():
                    try:
                        process = psutil.Process(x)
                        rowPosition = self.ui.tableWidget.rowCount()
                        self.ui.tableWidget.insertRow(rowPosition)
                        
                        self.create_table_widget(rowPosition, 0, str(process.pid), "tableWidget")
                        self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                        self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                        self.create_table_widget(rowPosition, 3, str(datetime.datetime.fromtimestamp(process.create_time(), datetime.UTC).strftime('%Y-%m-%d %H:%M:%S')), "tableWidget")
                        
                        suspend_btn = QPushButton(self.ui.tableWidget)
                        suspend_btn.setText("Suspend")
                        suspend_btn.clicked.connect(lambda checked, pid=process.pid: self.suspend_process(pid))
                        suspend_btn.setStyleSheet("color:brown")
                        self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)
                        
                        resume_btn = QPushButton(self.ui.tableWidget)
                        resume_btn.setText("Resume")
                        resume_btn.clicked.connect(lambda checked, pid=process.pid: self.resume_process(pid))
                        resume_btn.setStyleSheet("color:green")
                        self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)
                        
                        terminate_btn = QPushButton(self.ui.tableWidget)
                        terminate_btn.setText("Terminate")
                        terminate_btn.clicked.connect(lambda checked, pid=process.pid: self.terminate_process(pid))
                        terminate_btn.setStyleSheet("color:red")
                        self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)
                        
                        kill_btn = QPushButton(self.ui.tableWidget)
                        kill_btn.setText("Kill")
                        kill_btn.clicked.connect(lambda checked, pid=process.pid: self.kill_process(pid))
                        kill_btn.setStyleSheet("color:red")
                        self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)
                    except Exception as e:
                        print(f"Process {x} hata verdi: {e}")
                print("Süreçler güncellendi")

            # Ağ (Networks) Sayfası
            elif current_widget == self.ui.networks:
                self.ui.net_stats_table.setRowCount(0)
                for x in psutil.net_if_stats():
                    z = psutil.net_if_stats()
                    rowPosition = self.ui.net_stats_table.rowCount()
                    self.ui.net_stats_table.insertRow(rowPosition)
                    self.create_table_widget(rowPosition, 0, x, "net_stats_table")
                    self.create_table_widget(rowPosition, 1, str(z[x].isup), "net_stats_table")
                    self.create_table_widget(rowPosition, 2, str(z[x].duplex), "net_stats_table")
                    self.create_table_widget(rowPosition, 3, str(z[x].speed), "net_stats_table")
                    self.create_table_widget(rowPosition, 4, str(z[x].mtu), "net_stats_table")

                self.ui.net_io_table.setRowCount(0)
                for x in psutil.net_io_counters(pernic=True):
                    z = psutil.net_io_counters(pernic=True)
                    rowPosition = self.ui.net_io_table.rowCount()
                    self.ui.net_io_table.insertRow(rowPosition)
                    self.create_table_widget(rowPosition, 0, x, "net_io_table")
                    self.create_table_widget(rowPosition, 1, str(z[x].bytes_sent), "net_io_table")
                    self.create_table_widget(rowPosition, 2, str(z[x].bytes_recv), "net_io_table")
                    self.create_table_widget(rowPosition, 3, str(z[x].packets_sent), "net_io_table")
                    self.create_table_widget(rowPosition, 4, str(z[x].packets_recv), "net_io_table")
                    self.create_table_widget(rowPosition, 5, str(z[x].errin), "net_io_table")
                    self.create_table_widget(rowPosition, 6, str(z[x].errout), "net_io_table")
                    self.create_table_widget(rowPosition, 7, str(z[x].dropin), "net_io_table")
                    self.create_table_widget(rowPosition, 8, str(z[x].dropout), "net_io_table")

                self.ui.net_addr_table.setRowCount(0)
                for x in psutil.net_if_addrs():
                    z = psutil.net_if_addrs()
                    for y in z[x]:
                        rowPosition = self.ui.net_addr_table.rowCount()
                        self.ui.net_addr_table.insertRow(rowPosition)
                        self.create_table_widget(rowPosition, 0, str(x), "net_addr_table")
                        self.create_table_widget(rowPosition, 1, str(y.family), "net_addr_table")
                        self.create_table_widget(rowPosition, 2, str(y.address), "net_addr_table")
                        self.create_table_widget(rowPosition, 3, str(y.netmask), "net_addr_table")
                        self.create_table_widget(rowPosition, 4, str(y.broadcast), "net_addr_table")
                        self.create_table_widget(rowPosition, 5, str(y.ptp), "net_addr_table")

                self.ui.net_conn_table.setRowCount(0)
                for x in psutil.net_connections():
                    rowPosition = self.ui.net_conn_table.rowCount()
                    self.ui.net_conn_table.insertRow(rowPosition)
                    self.create_table_widget(rowPosition, 0, str(x.fd), "net_conn_table")
                    self.create_table_widget(rowPosition, 1, str(x.family), "net_conn_table")
                    self.create_table_widget(rowPosition, 2, str(x.type), "net_conn_table")
                    self.create_table_widget(rowPosition, 3, str(x.laddr), "net_conn_table")
                    self.create_table_widget(rowPosition, 4, str(x.raddr), "net_conn_table")
                    self.create_table_widget(rowPosition, 5, str(x.status), "net_conn_table")
                    self.create_table_widget(rowPosition, 6, str(x.pid), "net_conn_table")
                print("Ağ verileri güncellendi")

            # Diğer sayfalar için bir şey yapmıyoruz (battery, system_info, storage, sensors)
            else:
                print(f"Geçerli sayfa: {current_widget.objectName()}, veri güncellenmedi")

        except Exception as e:
            print(f"Yerel veri güncelleme hatası: {e}")

    def update_ui(self, data):
        current_widget = self.ui.stackedWidget.currentWidget()

        # CPU ve RAM Sayfası
        if current_widget == self.ui.cpu_and_memory:
            self.ui.cpu_per.setText(f"{data['cpu_percent']}%")
            self.ui.ram_usage.setText(f"{data['memory_percent']}%")
            self.ui.total_ram.setText(f"{data['total_ram']:.2f} GB")
            self.ui.free_ram.setText(f"{data['free_ram']:.2f} GB")
            self.ui.used_ram.setText(f"{data['used_ram']:.2f} GB")
            self.ui.cpu_percentage.setValue(data['cpu_percent'])
            self.ui.ram_percentage.setValue((data['free_ram'], data['used_ram'], data['total_ram'] - data['used_rand'] - data['free_ram']))

        # Süreçler (Activities) Sayfası
        elif current_widget == self.ui.activities:
            self.ui.tableWidget.setRowCount(0)
            for process in data['processes']:
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)
                
                self.create_table_widget(rowPosition, 0, str(process['pid']), "tableWidget")
                self.create_table_widget(rowPosition, 1, process['name'], "tableWidget")
                self.create_table_widget(rowPosition, 2, process['status'], "tableWidget")
                self.create_table_widget(rowPosition, 3, process['create_time'], "tableWidget")
                
                suspend_btn = QPushButton(self.ui.tableWidget)
                suspend_btn.setText("Suspend")
                suspend_btn.clicked.connect(lambda checked, pid=process['pid']: asyncio.run(self.send_command(pid, 'suspend')))
                suspend_btn.setStyleSheet("color:brown")
                self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)
                
                resume_btn = QPushButton(self.ui.tableWidget)
                resume_btn.setText("Resume")
                resume_btn.clicked.connect(lambda checked, pid=process['pid']: asyncio.run(self.send_command(pid, 'resume')))
                resume_btn.setStyleSheet("color:green")
                self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)
                
                terminate_btn = QPushButton(self.ui.tableWidget)
                terminate_btn.setText("Terminate")
                terminate_btn.clicked.connect(lambda checked, pid=process['pid']: asyncio.run(self.send_command(pid, 'terminate')))
                terminate_btn.setStyleSheet("color:red")
                self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)
                
                kill_btn = QPushButton(self.ui.tableWidget)
                kill_btn.setText("Kill")
                kill_btn.clicked.connect(lambda checked, pid=process['pid']: asyncio.run(self.send_command(pid, 'kill')))
                kill_btn.setStyleSheet("color:red")
                self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)

        # Ağ (Networks) Sayfası
        elif current_widget == self.ui.networks:
            self.ui.net_stats_table.setRowCount(0)
            for interface, stats in data['net_stats'].items():
                rowPosition = self.ui.net_stats_table.rowCount()
                self.ui.net_stats_table.insertRow(rowPosition)
                self.create_table_widget(rowPosition, 0, interface, "net_stats_table")
                self.create_table_widget(rowPosition, 1, stats['isup'], "net_stats_table")
                self.create_table_widget(rowPosition, 2, stats['duplex'], "net_stats_table")
                self.create_table_widget(rowPosition, 3, stats['speed'], "net_stats_table")
                self.create_table_widget(rowPosition, 4, stats['mtu'], "net_stats_table")

            self.ui.net_io_table.setRowCount(0)
            for interface, io in data['net_io'].items():
                rowPosition = self.ui.net_io_table.rowCount()
                self.ui.net_io_table.insertRow(rowPosition)
                self.create_table_widget(rowPosition, 0, interface, "net_io_table")
                self.create_table_widget(rowPosition, 1, str(io['bytes_sent']), "net_io_table")
                self.create_table_widget(rowPosition, 2, str(io['bytes_recv']), "net_io_table")
                self.create_table_widget(rowPosition, 3, str(io['packets_sent']), "net_io_table")
                self.create_table_widget(rowPosition, 4, str(io['packets_recv']), "net_io_table")
                self.create_table_widget(rowPosition, 5, str(io['errin']), "net_io_table")
                self.create_table_widget(rowPosition, 6, str(io['errout']), "net_io_table")
                self.create_table_widget(rowPosition, 7, str(io['dropin']), "net_io_table")
                self.create_table_widget(rowPosition, 8, str(io['dropout']), "net_io_table")

            self.ui.net_addr_table.setRowCount(0)
            for interface, addrs in data['net_addrs'].items():
                for addr in addrs:
                    rowPosition = self.ui.net_addr_table.rowCount()
                    self.ui.net_addr_table.insertRow(rowPosition)
                    self.create_table_widget(rowPosition, 0, interface, "net_addr_table")
                    self.create_table_widget(rowPosition, 1, addr['family'], "net_addr_table")
                    self.create_table_widget(rowPosition, 2, addr['address'], "net_addr_table")
                    self.create_table_widget(rowPosition, 3, addr['netmask'], "net_addr_table")
                    self.create_table_widget(rowPosition, 4, addr['broadcast'], "net_addr_table")
                    self.create_table_widget(rowPosition, 5, addr['ptp'], "net_addr_table")

            self.ui.net_conn_table.setRowCount(0)
            for conn in data['net_conns']:
                rowPosition = self.ui.net_conn_table.rowCount()
                self.ui.net_conn_table.insertRow(rowPosition)
                self.create_table_widget(rowPosition, 0, conn['fd'], "net_conn_table")
                self.create_table_widget(rowPosition, 1, conn['family'], "net_conn_table")
                self.create_table_widget(rowPosition, 2, conn['type'], "net_conn_table")
                self.create_table_widget(rowPosition, 3, conn['laddr'], "net_conn_table")
                self.create_table_widget(rowPosition, 4, conn['raddr'], "net_conn_table")
                self.create_table_widget(rowPosition, 5, conn['status'], "net_conn_table")
                self.create_table_widget(rowPosition, 6, conn['pid'], "net_conn_table")

    def create_table_widget(self, rowPosition, columnPosition, text, tableWidget):
        qtablewidgetitem = QTableWidgetItem()
        getattr(self.ui, tableWidget).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem = getattr(self.ui, tableWidget).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)

    def suspend_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.suspend()
        except Exception as e:
            print(f"Suspend hatası: {e}")

    def resume_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.resume()
        except Exception as e:
            print(f"Resume hatası: {e}")

    def terminate_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
        except Exception as e:
            print(f"Terminate hatası: {e}")

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.kill()
        except Exception as e:
            print(f"Kill hatası: {e}")

    def update_connection_status(self, status):
        self.connection_status = "Bağlantı Var" if status else "Bağlantı Yok"
        self.update_window_title()

    def update_window_title(self):
        self.setWindowTitle(f"İzlenen Cihaz: {self.device_id} - {self.connection_status}")

    def slideLeftMenu(self):
        width = self.ui.left_menu_cont_frame.width()
        newWidth = 200 if width == 40 else 40
        self.animation = QPropertyAnimation(self.ui.left_menu_cont_frame, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def applyButtonStyle(self):
        for w in self.ui.menu_frame.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                w.setStyleSheet("border-bottom: none")
        self.sender().setStyleSheet("border-bottom: 2px solid")

    def restore_or_minimize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-maximize.svg'))
        else:
            self.showMaximized()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-restore.svg'))

if __name__ == "__main__":
    # WebSocket sunucuyu ayrı thread’de başlat
    server_thread = threading.Thread(target=run_websocket_server)
    server_thread.daemon = True
    server_thread.start()
    print("WebSocket sunucu thread’i başlatıldı")

    # GUI’yı ana thread’de çalıştır
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())