import asyncio
import json
import os
import sys
import uuid
import hashlib
import websockets
import threading
import psutil
import PySide6
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from qt_material import apply_stylesheet
import datetime
import platform
import socket
from time import sleep
import logging
from logging.handlers import RotatingFileHandler

from ui_untitled import *

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            'app.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Yerel IP adresini alma
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

# Cihaz erişilebilirlik kontrolü
def is_device_reachable(ip):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = f"ping {param} 1 {ip}"
    return os.system(command) == 0

# Süreç kontrol fonksiyonları
def manage_process(pid, action):
    try:
        p = psutil.Process(pid)
        actions = {
            "suspend": p.suspend,
            "resume": p.resume,
            "terminate": p.terminate,
            "kill": p.kill
        }
        actions[action]()
        logger.info(f"Süreç {pid} için {action} işlemi başarılı")
    except Exception as e:
        logger.error(f"Süreç {pid} için {action} hatası: {e}")

# Benzersiz cihaz ID oluşturma
def generate_unique_id():
    config_file = "device_id.txt"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read()
    unique_id = hashlib.md5(str(uuid.getnode()).encode()).hexdigest()[:12]
    with open(config_file, "w") as f:
        f.write(unique_id)
    return unique_id

# Cihaz bilgisi yayınlama
def broadcast_device_info(device_id, local_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = json.dumps({"device_id": device_id, "ip": local_ip}).encode("utf-8")
    while True:
        try:
            sock.sendto(message, ("255.255.255.255", 12345))
            logger.info(f"Broadcast gönderildi: {device_id} - {local_ip}")
        except Exception as e:
            logger.error(f"Broadcast hatası: {e}")
        sleep(5)

# Ortak Veri Toplama Fonksiyonu
def gather_system_data(full=False):
    try:
        data = {
            'cpu_percent': psutil.cpu_percent(),
            'cpu_count': psutil.cpu_count(),
            'cpu_main_core': psutil.cpu_count(logical=False),
            'total_ram': psutil.virtual_memory().total / (1024 ** 3),
            'used_ram': psutil.virtual_memory().used / (1024 ** 3),
            'free_ram': psutil.virtual_memory().free / (1024 ** 3),
            'avail_ram': psutil.virtual_memory().available / (1024 ** 3),
            'memory_percent': psutil.virtual_memory().percent,
            'system_time': datetime.datetime.now().strftime("%I:%M:%S %p"),
            'system_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'machine': platform.machine() or 'Bilinmiyor',
            'version': platform.version() or 'Bilinmiyor',
            'platform': platform.platform() or 'Bilinmiyor',
            'system': platform.system() or 'Bilinmiyor',
            'processor': platform.processor() or 'Bilinmiyor',
        }

        if full:
            data.update({
                'processes': [
                    {'pid': p.pid, 'name': p.name(), 'status': p.status(), 'create_time': datetime.datetime.utcfromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')}
                    for p in psutil.process_iter(['pid', 'name', 'status', 'create_time'])
                ],
                'net_stats': {x: {'isup': str(y.isup), 'duplex': str(y.duplex), 'speed': str(y.speed), 'mtu': str(y.mtu)} for x, y in psutil.net_if_stats().items()},
                'net_io': {x: {'bytes_sent': str(y.bytes_sent), 'bytes_recv': str(y.bytes_recv), 'packets_sent': str(y.packets_sent), 'packets_recv': str(y.packets_recv), 'errin': str(y.errin), 'errout': str(y.errout), 'dropin': str(y.dropin), 'dropout': str(y.dropout)} for x, y in psutil.net_io_counters(pernic=True).items()},
                'net_addrs': {x: [{'family': str(y.family), 'address': str(y.address), 'netmask': str(y.netmask), 'broadcast': str(y.broadcast), 'ptp': str(y.ptp)} for y in psutil.net_if_addrs()[x]] for x in psutil.net_if_addrs()},
                'net_conns': [],
                'disk_partitions': []
            })

            # Ağ bağlantılarını topla
            try:
                connections = psutil.net_connections(kind='all')
                data['net_conns'] = [
                    {
                        'fd': str(x.fd) if x.fd is not None else 'N/A',
                        'family': str(x.family),
                        'type': str(x.type),
                        'laddr': str(x.laddr) if x.laddr else 'N/A',
                        'raddr': str(x.raddr) if x.raddr else 'N/A',
                        'status': str(x.status),
                        'pid': str(x.pid) if x.pid is not None else 'N/A'
                    } for x in connections
                ]
                logger.info(f"Ağ bağlantıları toplandı: {len(data['net_conns'])} bağlantı bulundu")
            except psutil.AccessDenied as e:
                logger.error(f"Ağ bağlantıları alınamadı, erişim izni hatası: {e}")
                data['net_conns'] = []
            except Exception as e:
                logger.error(f"Ağ bağlantıları alınırken hata: {e}")
                data['net_conns'] = []

            # Disk bölümleri
            logger.debug("Disk bölümleri toplanıyor")
            for p in psutil.disk_partitions(all=False):
                try:
                    disk_usage = psutil.disk_usage(p.mountpoint)
                    partition = {
                        'device': p.device,
                        'mountpoint': p.mountpoint,
                        'opts': p.opts or 'N/A',
                        'total': disk_usage.total / (1024 ** 3),
                        'used': disk_usage.used / (1024 ** 3),
                        'free': disk_usage.free / (1024 ** 3),
                        'percent': disk_usage.percent,
                        'MAX': 'N/A',
                        'max_file': 'N/A',
                        'max_path': 'N/A'
                    }
                    if platform.system().lower() != 'windows':
                        try:
                            stat = os.statvfs(p.mountpoint)
                            partition['MAX'] = stat.f_blocks * stat.f_frsize / (1024 ** 3)
                            partition['max_file'] = stat.f_files
                            partition['max_path'] = stat.f_namemax
                        except Exception as e:
                            logger.warning(f"statvfs hatası ({p.mountpoint}): {e}")
                    data['disk_partitions'].append(partition)
                    logger.debug(f"Disk partition verisi eklendi: {partition}")
                except PermissionError as e:
                    logger.warning(f"Disk partition izni hatası ({p.mountpoint}): {e}")
                except OSError as e:
                    logger.warning(f"Disk partition sistem hatası ({p.mountpoint}): {e}")
                except Exception as e:
                    logger.error(f"Disk partition beklenmeyen hata ({p.mountpoint}): {type(e).__name__} - {str(e)}")

            # Sıcaklık verileri
            try:
                if hasattr(psutil, "sensors_temperatures"):
                    temps = psutil.sensors_temperatures()
                    if temps:
                        data['temperatures'] = {
                            sensor: [
                                {
                                    'label': t.label or f"Sensör {i}",
                                    'current': t.current,
                                    'high': t.high if t.high is not None else 'N/A',
                                    'critical': t.critical if t.critical is not None else 'N/A'
                                } for i, t in enumerate(values)
                            ] for sensor, values in temps.items()
                        }
                        logger.info(f"Sıcaklık verisi toplandı: {len(temps)} sensör bulundu")
                    else:
                        data['temperatures'] = {}
                        logger.info("Sıcaklık sensörü bulunamadı")
                else:
                    data['temperatures'] = {}
                    logger.info("psutil.sensors_temperatures desteklenmiyor")
            except Exception as e:
                data['temperatures'] = {}
                logger.error(f"Sıcaklık verisi alınırken hata: {type(e).__name__} - {str(e)}")

        return data
    except Exception as e:
        logger.error(f"Veri toplama hatası: {e}")
        return {}

# WebSocket veri gönderme
async def send_system_info(websocket, path):
    cached_data = {"processes": [], "net_stats": {}, "net_io": {}, "net_addrs": {}, "net_conns": [], "disk_partitions": [], "temperatures": {}}
    update_counter = 0
    while True:
        try:
            data = gather_system_data(full=(update_counter % 5 == 0))
            if update_counter % 5 == 0:
                cached_data.update(data)
            else:
                cached_data.update({k: v for k, v in data.items() if k not in cached_data})
            await websocket.send(json.dumps(cached_data))

            try:
                command = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                command_data = json.loads(command)
                pid = command_data.get('pid')
                action = command_data.get('action')
                if pid and action:
                    manage_process(pid, action)
            except asyncio.TimeoutError:
                pass
            update_counter += 1
            await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket bağlantısı kapandı")
            break
        except Exception as e:
            logger.error(f"send_system_info hatası: {e}")
            await asyncio.sleep(1)

# WebSocket sunucusu
async def send_websocket_server():
    async with websockets.serve(send_system_info, '0.0.0.0', 8765):
        await asyncio.Future()

def run_websocket_server():
    device_id = generate_unique_id()
    local_ip = get_local_ip()
    broadcast_thread = threading.Thread(target=broadcast_device_info, args=(device_id, local_ip))
    broadcast_thread.daemon = True
    broadcast_thread.start()
    asyncio.run(send_websocket_server())

# WebSocket istemcisi
class WebSocketClient(QThread):
    data_received = Signal(dict)
    status_changed = Signal(bool)

    def __init__(self, uri, loop=None):
        super().__init__()
        self.uri = uri
        self.loop = loop or asyncio.get_event_loop()
        self.connected = False

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.uri) as websocket:
                    self.connected = True
                    self.status_changed.emit(True)
                    self.websocket = websocket
                    while True:
                        try:
                            data = await websocket.recv()
                            self.data_received.emit(json.loads(data))
                        except websockets.exceptions.ConnectionClosed:
                            break
            except Exception as e:
                self.connected = False
                self.status_changed.emit(False)
                logger.error(f"WebSocket bağlantı hatası: {e}")
                await asyncio.sleep(2)

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())

# Cihaz keşfi
class DeviceDiscovery(QThread):
    device_found = Signal(dict)

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            sock.bind(("", 12345))
            logger.info("12345 portunda dinleme başlatıldı")
        except Exception as e:
            logger.error(f"Port bağlama hatası: {e}")
            return
        while True:
            data, addr = sock.recvfrom(1024)
            try:
                device_info = json.loads(data.decode("utf-8"))
                self.device_found.emit(device_info)
                logger.info(f"Keşfedilen cihaz: {device_info}")
            except Exception as e:
                logger.error(f"Keşif hatası: {e}")

# Login penceresi
class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(600, 400)
        self.centralwidget = QWidget(LoginWindow)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.top_layout = QHBoxLayout()
        self.device_id_label = QLabel("Benim Kodum: Yükleniyor...")
        self.scan_button = QPushButton("Cihazları Tara")
        self.top_layout.addWidget(self.device_id_label)
        self.top_layout.addWidget(self.scan_button)
        self.verticalLayout.addLayout(self.top_layout)
        self.device_table = QTableWidget()
        self.device_table.setColumnCount(4)
        self.device_table.setHorizontalHeaderLabels(["Kod", "Durum", "Bağlantı", "İzle"])
        self.device_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.device_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.device_table.setAutoScroll(False)
        self.verticalLayout.addWidget(self.device_table)
        LoginWindow.setCentralWidget(self.centralwidget)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.device_id = generate_unique_id()
        self.ui.device_id_label.setText(f"Benim Kodum: {self.device_id}")
        self.devices = {self.device_id: {"status": "Yerel Bilgisayar", "ip": None, "connected": True}}
        self.ws_clients = {}
        self.load_devices()
        self.ui.scan_button.clicked.connect(self.start_device_discovery)
        self.start_monitoring()
        self.update_device_table()
        logger.info("LoginWindow başlatıldı")

    def start_device_discovery(self):
        if not hasattr(self, 'discovery'):
            self.discovery = DeviceDiscovery()
            self.discovery.device_found.connect(self.add_discovered_device)
            self.discovery.start()
        logger.info("Cihaz keşfi başlatıldı")

    def add_discovered_device(self, device_info):
        device_code = device_info["device_id"]
        device_ip = device_info["ip"]
        if device_code != self.device_id and device_code not in self.devices:
            self.devices[device_code] = {"status": "Uzak Bilgisayar", "ip": device_ip, "connected": False}
            self.start_monitoring_device(device_code)
            self.save_devices()
            self.update_device_table()
            logger.info(f"Keşfedilen cihaz: {device_code} - {device_ip}")

    def start_monitoring(self):
        for device_code, info in self.devices.items():
            if info["ip"]:
                self.start_monitoring_device(device_code)

    def start_monitoring_device(self, device_code):
        if device_code not in self.ws_clients:
            ip = self.devices[device_code]['ip']
            if is_device_reachable(ip):
                uri = f"ws://{ip}:8765"
                loop = asyncio.new_event_loop()
                client = WebSocketClient(uri, loop)
                client.status_changed.connect(lambda status, code=device_code: self.update_device_status(code, status))
                client.start()
                self.ws_clients[device_code] = client
                logger.info(f"{device_code} için WebSocket istemci başlatıldı")
            else:
                logger.warning(f"{ip} adresine ulaşılamıyor")

    def update_device_status(self, device_code, status):
        self.devices[device_code]["connected"] = status
        self.update_device_table()

    def update_device_table(self):
        scroll_pos = self.ui.device_table.verticalScrollBar().value()
        self.ui.device_table.setUpdatesEnabled(False)
        try:
            self.ui.device_table.setRowCount(0)
            for i, (device_code, info) in enumerate(self.devices.items()):
                self.ui.device_table.insertRow(i)
                self.ui.device_table.setItem(i, 0, QTableWidgetItem(device_code))
                self.ui.device_table.setItem(i, 1, QTableWidgetItem(info["status"]))
                self.ui.device_table.setItem(i, 2, QTableWidgetItem("Bağlantı Var" if info["connected"] else "Bağlantı Yok"))
                watch_btn = QPushButton("İzle")
                watch_btn.clicked.connect(lambda checked, code=device_code: self.open_device_monitor(code))
                self.ui.device_table.setCellWidget(i, 3, watch_btn)
        finally:
            self.ui.device_table.setUpdatesEnabled(True)
            self.ui.device_table.verticalScrollBar().setValue(scroll_pos)

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
        if device_code in self.devices:
            device_ip = self.devices[device_code].get("ip")
            self.monitor_window = MainWindow(device_code, device_ip)
            self.monitor_window.show()
        else:
            logger.error(f"Cihaz bulunamadı: {device_code}")
            QMessageBox.critical(self, "Hata", f"'{device_code}' cihazı bulunamadı!")

# Ana pencere
class MainWindow(QMainWindow):
    def __init__(self, device_id, device_ip=None):
        super().__init__()
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
        self.connection_status = "Bağlantı Var" if not device_ip else "Bağlantı Bekleniyor"
        self.update_window_title()

        for table in [self.ui.storageTable, self.ui.tableWidget, self.ui.net_stats_table, self.ui.net_io_table, self.ui.net_addr_table, self.ui.net_conn_table]:
            table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            table.setAutoScroll(False)

        self.ui.minimize_button.clicked.connect(self.showMinimized)
        self.ui.exit_button.clicked.connect(self.close)
        self.ui.window_restore_button.clicked.connect(self.restore_or_minimize)
        self.ui.cpu_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory))
        self.ui.battery_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.battery))
        self.ui.info_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.system_info))
        self.ui.activity_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.activities))
        self.ui.disk_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.storage))
        self.ui.network_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.networks))
        self.ui.sensor_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.sensors))
        self.ui.stackedWidget.setCurrentWidget(self.ui.cpu_and_memory)
        self.ui.MenuButton.clicked.connect(self.slideLeftMenu)
        for w in self.ui.menu_frame.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)

        def moveWindow(event):
            if not self.isMaximized() and event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()
        self.ui.header_frame.mouseMoveEvent = moveWindow

        self.cached_data = {}
        self.update_counter = 0
        if self.device_ip:
            loop = asyncio.new_event_loop()
            self.ws_client = WebSocketClient(f"ws://{self.device_ip}:8765", loop)
            self.ws_client.data_received.connect(self.handle_websocket_data)
            self.ws_client.status_changed.connect(self.update_connection_status)
            self.ws_client.start()
        else:
            self.collect_system_data(full=True)
            self.timer = QTimer(self)
            self.timer.timeout.connect(lambda: self.collect_system_data(full=(self.update_counter % 5 == 0)))
            self.timer.start(2000)

        self.show()

    def collect_system_data(self, full=False):
        self.update_counter += 1
        data = gather_system_data(full=full)
        if data:
            self.cached_data.update(data)
            self.update_widgets(self.cached_data, full=full)
            logger.info("Yerel veri toplandı ve arayüz güncellendi")
        else:
            logger.error("Yerel veri toplama başarısız")
            QMessageBox.critical(self, "Hata", "Veri toplama hatası")

    def update_widgets(self, data, full=False):
        current_widget = self.ui.stackedWidget.currentWidget()
        try:
            if full or current_widget == self.ui.cpu_and_memory:
                self.ui.cpu_per.setText(f"{data.get('cpu_percent', 0)}%")
                self.ui.cpu_count.setText(str(data.get('cpu_count', 'N/A')))
                self.ui.cpu_main_core.setText(str(data.get('cpu_main_core', 'N/A')))
                self.ui.total_ram.setText(f"{data.get('total_ram', 0):.2f} GB")
                self.ui.used_ram.setText(f"{data.get('used_ram', 0):.2f} GB")
                self.ui.free_ram.setText(f"{data.get('free_ram', 0):.2f} GB")
                self.ui.avail_ram.setText(f"{data.get('avail_ram', 0):.2f} GB")
                self.ui.ram_usage.setText(f"{data.get('memory_percent', 0)}%")
                self.ui.cpu_percentage.setValue(int(data.get('cpu_percent', 0)))
                self.ui.ram_percentage.setMaximumValue(data.get('total_ram', 1))
                self.ui.ram_percentage.setValue(data.get('avail_ram', 0))

            if full or current_widget == self.ui.activities:
                scroll_pos = self.ui.tableWidget.verticalScrollBar().value()
                self.ui.tableWidget.setUpdatesEnabled(False)
                try:
                    processes = data.get('processes', [])
                    current_pids = {self.ui.tableWidget.item(row, 0).text() for row in range(self.ui.tableWidget.rowCount()) if self.ui.tableWidget.item(row, 0)}
                    new_pids = {str(p['pid']) for p in processes}

                    for process in processes:
                        pid = str(process.get('pid', 'N/A'))
                        if pid not in current_pids:
                            row = self.ui.tableWidget.rowCount()
                            self.ui.tableWidget.insertRow(row)
                        else:
                            row = next(r for r in range(self.ui.tableWidget.rowCount()) if self.ui.tableWidget.item(r, 0).text() == pid)
                        self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(pid))
                        self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(process.get('name', 'N/A')))
                        self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(process.get('status', 'N/A')))
                        self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(process.get('create_time', 'N/A')))
                        for col, (text, action, color) in enumerate([
                            ("Suspend", "suspend", "brown"),
                            ("Resume", "resume", "green"),
                            ("Terminate", "terminate", "red"),
                            ("Kill", "kill", "red")
                        ]):
                            btn = QPushButton(text)
                            btn.clicked.connect(lambda checked, pid=process['pid'], act=action: manage_process(pid, act) if not self.device_ip else asyncio.run(self.send_command(pid, act)))
                            btn.setStyleSheet(f"color:{color}")
                            self.ui.tableWidget.setCellWidget(row, 4 + col, btn)

                    for row in range(self.ui.tableWidget.rowCount() - 1, -1, -1):
                        if self.ui.tableWidget.item(row, 0).text() not in new_pids:
                            self.ui.tableWidget.removeRow(row)
                finally:
                    self.ui.tableWidget.setUpdatesEnabled(True)
                    self.ui.tableWidget.verticalScrollBar().setValue(scroll_pos)

            if full or current_widget == self.ui.networks:
                for table, data_key, keys in [
                    (self.ui.net_stats_table, 'net_stats', ['isup', 'duplex', 'speed', 'mtu']),
                    (self.ui.net_io_table, 'net_io', ['bytes_sent', 'bytes_recv', 'packets_sent', 'packets_recv', 'errin', 'errout', 'dropin', 'dropout']),
                ]:
                    scroll_pos = table.verticalScrollBar().value()
                    table.setUpdatesEnabled(False)
                    try:
                        table.setRowCount(0)
                        for interface, stats in data.get(data_key, {}).items():
                            row = table.rowCount()
                            table.insertRow(row)
                            table.setItem(row, 0, QTableWidgetItem(interface))
                            for col, key in enumerate(keys):
                                table.setItem(row, col + 1, QTableWidgetItem(str(stats.get(key, 'N/A'))))
                    finally:
                        table.setUpdatesEnabled(True)
                        table.verticalScrollBar().setValue(scroll_pos)

                scroll_pos = self.ui.net_addr_table.verticalScrollBar().value()
                self.ui.net_addr_table.setUpdatesEnabled(False)
                try:
                    self.ui.net_addr_table.setRowCount(0)
                    for interface, addrs in data.get('net_addrs', {}).items():
                        for addr in addrs:
                            row = self.ui.net_addr_table.rowCount()
                            self.ui.net_addr_table.insertRow(row)
                            self.ui.net_addr_table.setItem(row, 0, QTableWidgetItem(interface))
                            for col, key in enumerate(['family', 'address', 'netmask', 'broadcast', 'ptp']):
                                self.ui.net_addr_table.setItem(row, col + 1, QTableWidgetItem(str(addr.get(key, 'N/A'))))
                finally:
                    self.ui.net_addr_table.setUpdatesEnabled(True)
                    self.ui.net_addr_table.verticalScrollBar().setValue(scroll_pos)

                scroll_pos = self.ui.net_conn_table.verticalScrollBar().value()
                self.ui.net_conn_table.setUpdatesEnabled(False)
                try:
                    self.ui.net_conn_table.setRowCount(0)
                    connections = data.get('net_conns', [])
                    logger.debug(f"Net connections tablosuna {len(connections)} bağlantı ekleniyor")
                    if not connections:
                        row = self.ui.net_conn_table.rowCount()
                        self.ui.net_conn_table.insertRow(row)
                        self.ui.net_conn_table.setItem(row, 0, QTableWidgetItem("Bağlantı bulunamadı"))
                        for col in range(1, 7):
                            self.ui.net_conn_table.setItem(row, col, QTableWidgetItem(""))
                    else:
                        for conn in connections:
                            row = self.ui.net_conn_table.rowCount()
                            self.ui.net_conn_table.insertRow(row)
                            for col, key in enumerate(['fd', 'family', 'type', 'laddr', 'raddr', 'status', 'pid']):
                                self.ui.net_conn_table.setItem(row, col, QTableWidgetItem(str(conn.get(key, 'N/A'))))
                finally:
                    self.ui.net_conn_table.setUpdatesEnabled(True)
                    self.ui.net_conn_table.verticalScrollBar().setValue(scroll_pos)

            if full or current_widget == self.ui.battery:
                if data.get('battery') != "Not available":
                    self.ui.battery_charge.setText(f"{data.get('battery', 0)}%")
                    self.ui.battery_plugged.setText("Takılı" if data.get('batt_plugged', False) else "Takılı Değil")
                    self.ui.battery_status.setText("Şarj Oluyor" if data.get('batt_plugged', False) and float(data.get('battery', 0)) < 100 else "Tamamen Şarj Oldu" if float(data.get('battery', 0)) == 100 else "Deşarj Oluyor")
                    if data.get('batt_plugged', False) or data.get('batt_time', 0) in [psutil.POWER_TIME_UNLIMITED, None, 0]:
                        self.ui.battery_time_left.setText("Yok" if data.get('batt_plugged', False) else "Hesaplanıyor...")
                    else:
                        hours = data.get('batt_time', 0) // 3600
                        minutes = (data.get('batt_time', 0) % 3600) // 60
                        self.ui.battery_time_left.setText(f"{hours}sa {minutes}dk")
                    self.ui.battery_usage.setValue(int(float(data.get('battery', 0))))
                else:
                    self.ui.battery_status.setText("Pil mevcut değil")

            if full or current_widget == self.ui.system_info:
                self.ui.cpu_count.setText(f" {data.get('cpu_count', 'N/A')}")
                self.ui.cpu_main_core.setText(f" {data.get('cpu_main_core', 'N/A')}")
                self.ui.system_time.setText(f" {data.get('system_time', 'N/A')}")
                self.ui.system_date.setText(f" {data.get('system_date', 'N/A')}")
                self.ui.system_machine.setText(f" {data.get('machine', 'N/A')}")
                self.ui.system_version.setText(f" {data.get('version', 'N/A')}")
                self.ui.system_platform.setText(f" {data.get('platform', 'N/A')}")
                self.ui.system_system.setText(f" {data.get('system', 'N/A')}")
                self.ui.system_processor.setText(f" {data.get('processor', 'N/A')}")

            if full or current_widget == self.ui.storage:
                scroll_pos = self.ui.storageTable.verticalScrollBar().value()
                self.ui.storageTable.setUpdatesEnabled(False)
                try:
                    partitions = data.get('disk_partitions', [])
                    current_devices = {self.ui.storageTable.item(row, 0).text() for row in range(self.ui.storageTable.rowCount()) if self.ui.storageTable.item(row, 0)}
                    new_devices = {p['device'] for p in partitions}

                    for partition in partitions:
                        device = partition.get('device', 'N/A')
                        if device not in current_devices:
                            row = self.ui.storageTable.rowCount()
                            self.ui.storageTable.insertRow(row)
                        else:
                            row = next(r for r in range(self.ui.storageTable.rowCount()) if self.ui.storageTable.item(r, 0).text() == device)
                        for col, key in enumerate(['device', 'mountpoint', 'opts', 'MAX', 'max_file', 'max_path', 'total', 'used', 'free', 'percent']):
                            value = partition.get(key, 'N/A')
                            if key in ['total', 'used', 'free', 'MAX']:
                                try:
                                    value = f"{float(value):.2f} GB"
                                except (ValueError, TypeError):
                                    value = 'N/A'
                            elif key == 'percent':
                                try:
                                    value = f"{float(value):.2f}%"
                                except (ValueError, TypeError):
                                    value = 'N/A'
                            else:
                                value = str(value)
                            self.ui.storageTable.setItem(row, col, QTableWidgetItem(value))
                            logger.debug(f"Storage table cell ({row}, {col}): {value}")

                    for row in range(self.ui.storageTable.rowCount() - 1, -1, -1):
                        if self.ui.storageTable.item(row, 0).text() not in new_devices:
                            self.ui.storageTable.removeRow(row)
                finally:
                    self.ui.storageTable.setUpdatesEnabled(True)
                    self.ui.storageTable.verticalScrollBar().setValue(scroll_pos)

            # Sensors sekmesi (DEĞİŞTİ)
            if full or current_widget == self.ui.sensors:
                scroll_pos = self.ui.sensorsTable.verticalScrollBar().value()
                self.ui.sensorsTable.setUpdatesEnabled(False)
                try:
                    self.ui.sensorsTable.setRowCount(0)
                    temps = data.get('temperatures', {})
                    logger.debug(f"Sensors tablosu güncelleniyor, temperatures: {temps}")
                    if temps:
                        for sensor, values in temps.items():
                            for temp in values:
                                row = self.ui.sensorsTable.rowCount()
                                self.ui.sensorsTable.insertRow(row)
                                self.ui.sensorsTable.setItem(row, 0, QTableWidgetItem(sensor))
                                self.ui.sensorsTable.setItem(row, 1, QTableWidgetItem(temp['label']))
                                self.ui.sensorsTable.setItem(row, 2, QTableWidgetItem(f"{temp['current']:.1f}°C"))
                                self.ui.sensorsTable.setItem(row, 3, QTableWidgetItem(str(temp['high']) if temp['high'] != 'N/A' else 'N/A'))
                                self.ui.sensorsTable.setItem(row, 4, QTableWidgetItem(str(temp['critical']) if temp['critical'] != 'N/A' else 'N/A'))
                    else:
                        row = self.ui.sensorsTable.rowCount()
                        self.ui.sensorsTable.insertRow(row)
                        self.ui.sensorsTable.setItem(row, 0, QTableWidgetItem("Sensör bulunamadı"))
                        for col in range(1, 5):
                            self.ui.sensorsTable.setItem(row, col, QTableWidgetItem(""))
                        logger.debug("Sensors tablosuna sensör bulunamadı mesajı eklendi")
                finally:
                    self.ui.sensorsTable.setUpdatesEnabled(True)
                    self.ui.sensorsTable.verticalScrollBar().setValue(scroll_pos)

        except Exception as e:
            logger.error(f"Arayüz güncelleme hatası: {e}")

    def handle_websocket_data(self, data):
        if not hasattr(self, 'initial_data_fetched'):
            self.initial_data_fetched = True
            self.update_widgets(data, full=True)
        else:
            self.update_widgets(data, full=(self.update_counter % 5 == 0))
        self.update_counter += 1

    async def send_command(self, pid, action):
        if hasattr(self, 'ws_client') and self.ws_client.websocket:
            command = json.dumps({'pid': pid, 'action': action})
            await self.ws_client.websocket.send(command)
            logger.info(f"Komut gönderildi: {pid} - {action}")

    def slideLeftMenu(self):
        width = self.ui.left_menu_cont_frame.width()
        newWidth = 200 if width == 40 else 40
        self.animation = QPropertyAnimation(self.ui.left_menu_cont_frame, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def update_connection_status(self, status):
        self.connection_status = "Bağlantı Var" if status else "Bağlantı Yok"
        self.update_window_title()

    def update_window_title(self):
        self.setWindowTitle(f"İzlenen Cihaz: {self.device_id} - {self.connection_status}")

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def applyButtonStyle(self):
        for w in self.ui.menu_frame.findChildren(QPushButton):
            w.setStyleSheet("border-bottom: none" if w != self.sender() else "border-bottom: 2px solid")

    def restore_or_minimize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-maximize.svg'))
        else:
            self.showMaximized()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-restore.svg'))

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_websocket_server)
    server_thread.daemon = True
    server_thread.start()
    logger.info("WebSocket sunucu thread’i başlatıldı")
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())