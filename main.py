import asyncio
import json
import os
import wmi
import sys
import uuid
import hashlib
import websockets
from tkinter.ttk import Sizegrip
import psutil
import PySide6
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QProgressBar
from PySide6.QtCore import *
from PySideExtn import *
from qt_material import apply_stylesheet
from multiprocessing import cpu_count
import datetime
import platform
import shutil
from time import sleep
import traceback

from ui_untitled import *

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

def generate_unique_id():
    mac = uuid.getnode()
    unique_id = hashlib.md5(str(mac).encode()).hexdigest()[:12]
    config_file = "device_id.txt"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read()
    else:
        with open(config_file, "w") as f:
            f.write(unique_id)
async def send_system_info(websocket, path):
    while True: 
        processes = []
        for x in psutil.pids():
            try:
                p = psutil.Process(x)
                processes.append({
                    'pid': p.pid,
                    'name': p.name(),
                    'status': p.status(),
                    'create_time': datetime.datetime.utcfromtimestamp(p.create_time()).strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                continue


        data = {
            'cpu_count': psutil.cpu_count(),
            'cpu_main_core': psutil.cpu_count(logical=False),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'total_ram': psutil.virtual_memory().total / (1024 ** 3),
            'used_ram': psutil.virtual_memory().used / (1024 ** 3),
            'free_ram': psutil.virtual_memory().available / (1024 ** 3),
            'system_time': datetime.datetime.now().strftime("%I:%M:%S %p"),
            'system_date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'machine': platform.machine(),
            'version': platform.version(),
            'platform': platform.platform(),
            'system': platform.system(),
            'processor': platform.processor(),
            'battery': psutil.sensors_battery().percent if hasattr(psutil, "sensors_battery") else "Not available",
            'batt_plugged': psutil.sensors_battery().power_plugged ,
            'batt_time' : psutil.sensors_battery().secsleft,
            'processes': processes
        }
        await websocket.send(json.dumps(data))

        try:
            command = await asyncio.wait_for(websocket.recv(), timeout=0.1)
            command_data = json.loads(command)
            pid = command_data.get('pid')
            action = command_data.get('action')
            if pid and action:
                p = psutil.Process(pid)
                if action == "suspend":
                    p.suspend()
                elif action == "resume":
                    p.resume()
                elif action == "terminate":
                    p.terminate()
                elif action == "kill":
                    p.kill()
        except asyncio.TimeoutError:
            pass
        await asyncio.sleep(1)

platforms = {
    'linux': 'Linux',
    'linux1': 'Linux',
    'linux2': 'Linux',
    'darwin': 'OS X',
    'win32': 'Windows'
}
class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs['process_callback'] = self.signals.progress

        
    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
##main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
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
        self.setWindowTitle('System Monitoring Application')
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


        self.threadpool = QThreadPool()


        def moveWindow(event):
            if self.isMaximized() == False: # if the window is not maximized:
                # Move the window only when window is normal size
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.clickPosition)
                    self.clickPosition = event.globalPos()
                    event.accept()

        self.ui.header_frame.mouseMoveEvent = moveWindow

        

        self.show()
        #self.battery()
        #self.cpu_ram()
        self.system_info()
        self.processes()
        self.storage()
        self.sensors()
        self.networks()
        self.psutil_thread()
    
    

    def psutil_thread(self):
        worker = Worker(self.cpu_ram)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(worker)

        battery_worker = Worker(self.battery)

        battery_worker.signals.result.connect(self.print_output)
        battery_worker.signals.finished.connect(self.thread_complete)
        battery_worker.signals.progress.connect(self.progress_fn)

        self.threadpool.start(battery_worker)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def progress_fn(self, n):
        print("%d%% done" % n)

    def networks(self):
        for x in psutil.net_if_stats():
            z= psutil.net_if_stats()
            rowPosition = self.ui.net_stats_table.rowCount()
            self.ui.net_stats_table.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, x, "net_stats_table")
            self.create_table_widget(rowPosition, 1, str(z[x].isup), "net_stats_table")
            self.create_table_widget(rowPosition, 2, str(z[x].duplex), "net_stats_table")
            self.create_table_widget(rowPosition, 3, str(z[x].speed), "net_stats_table")
            self.create_table_widget(rowPosition, 4, str(z[x].mtu), "net_stats_table")
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
        for x in psutil.net_connections():
            z = psutil.net_connections()
            rowPosition = self.ui.net_conn_table.rowCount()
            self.ui.net_conn_table.insertRow(rowPosition)
            self.create_table_widget(rowPosition, 0, str(x.fd), "net_conn_table")
            self.create_table_widget(rowPosition, 1, str(x.family), "net_conn_table")
            self.create_table_widget(rowPosition, 2, str(x.type), "net_conn_table")
            self.create_table_widget(rowPosition, 3, str(x.laddr), "net_conn_table")
            self.create_table_widget(rowPosition, 4, str(x.raddr), "net_conn_table")
            self.create_table_widget(rowPosition, 5, str(x.status), "net_conn_table")
            self.create_table_widget(rowPosition, 6, str(x.pid), "net_conn_table")



    ##############################
    ## Windows için sensor okumayı eklemeyi unutma aynı zamanda storagete de o tarzdan bişiler vardı
    ##############################
    def sensors(self):
        if sys.platform == 'linux' or sys.platform == 'linux1' or sys.platform == 'linux2':
            for x in psutil.sensors_temperatures():
                for y in psutil.sensor_temperatures()[x]:
                    rowPosition = self.ui.sensorsTable.rowCount()
                    self.ui.sensorsTable.insertRow(rowPosition)

                    self.create_table_widget(rowPosition, 0, x, "sensorsTable")
                    self.create_table_widget(rowPosition, 1, y.label, "sensorsTable")
                    self.create_table_widget(rowPosition, 2, str(y.current), "sensorsTable")
                    self.create_table_widget(rowPosition, 3, str(y.high), "sensorsTable")
                    self.create_table_widget(rowPosition, 4, str(y.critical), "sensorsTable")

                    temp_per = (y.current/y.high)*100
                    progressBar = QProgressBar(self.ui.sensorsTable)
                    progressBar.setObjectName(u"progressBar")
                    progressBar.setValue(temp_per)
                    self.ui.sensorsTable.setCellWidget(rowPosition, 5, progressBar)
        elif sys.platform == 'win32':
            w = wmi.WMI()
            for sensor in w.Win32_TemperatureProbe():
                rowPosition = self.ui.sensorsTable.rowCount()
                self.ui.sensorsTable.insertRow(rowPosition)

                self.create_table_widget(rowPosition, 0, "TemperatureProbe", "sensorsTable")
                self.create_table_widget(rowPosition, 2, str(sensor.CurrentReading), "sensorsTable")
        else:
            global platforms
            rowPosition = self.ui.sensorsTable.rowCount()
            self.ui.sensorsTable.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, "Function not available on this platform", "sensorsTable")
            self.create_table_widget(rowPosition, 1, "Function not available on this platform", "sensorsTable")
            self.create_table_widget(rowPosition, 2, "Function not available on this platform", "sensorsTable")
            self.create_table_widget(rowPosition, 3, "Function not available on this platform", "sensorsTable")
            self.create_table_widget(rowPosition, 4, "Function not available on this platform", "sensorsTable")
            self.create_table_widget(rowPosition, 5, "Function not available on this platform", "sensorsTable")

    def storage(self):
        storage_device = psutil.disk_partitions(all=False)
        z=0
        for x in storage_device:
            rowPosition = self.ui.storageTable.rowCount()
            self.ui.storageTable.insertRow(rowPosition)

            self.create_table_widget(rowPosition, 0, x.device, "storageTable")
            self.create_table_widget(rowPosition, 1, x.mountpoint, "storageTable")
            self.create_table_widget(rowPosition, 2, x.fstype, "storageTable")
            self.create_table_widget(rowPosition, 3, x.opts, "storageTable")

            if sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'linux2':
                self.create_table_widget(rowPosition, 4, str(x.maxfile),"storageTable")
                self.create_table_widget(rowPosition, 5, str(x.maxpath),"storageTable")
            else:
                self.create_table_widget(rowPosition, 4, "Function not available on this platform","storageTable")
                self.create_table_widget(rowPosition, 5, "Function not available on this platform", "storageTable")
            disk_usage = shutil.disk_usage(x.mountpoint)

            self.create_table_widget(rowPosition, 6, str((disk_usage.total/(1024*1024*1024)))+" GB","storageTable")
            self.create_table_widget(rowPosition, 7, str((disk_usage.used/(1024*1024*1024)))+" GB","storageTable")
            self.create_table_widget(rowPosition, 8, str((disk_usage.free/(1024*1024*1024)))+" GB","storageTable")
            
            full_disk = (disk_usage.used/disk_usage.total)*100
            progressBar = QProgressBar(self.ui.storageTable)
            progressBar.setObjectName("progressBar")
            progressBar.setValue(full_disk)
            self.ui.storageTable.setCellWidget(rowPosition, 9, progressBar)


    def create_table_widget(self, rowPosition, columnPosition, text, tableWidget):
        qtablewidgetitem= QTableWidgetItem()
        getattr(self.ui, tableWidget).setItem(rowPosition, columnPosition, qtablewidgetitem)
        qtablewidgetitem=getattr(self.ui, tableWidget).item(rowPosition, columnPosition)
        qtablewidgetitem.setText(text)

    def processes(self):
        self.ui.tableWidget.setRowCount(0)  # Önce tabloyu temizle

        for x in psutil.pids():
            try:
                process = psutil.Process(x)

                # Hata yoksa satır ekleyelim
                rowPosition = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(rowPosition)

                self.create_table_widget(rowPosition, 0, str(process.pid), "tableWidget")
                self.create_table_widget(rowPosition, 1, process.name(), "tableWidget")
                self.create_table_widget(rowPosition, 2, process.status(), "tableWidget")
                self.create_table_widget(rowPosition, 3, str(datetime.datetime.utcfromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')), "tableWidget")

                suspend_btn = QPushButton(self.ui.tableWidget)
                suspend_btn.setText("Suspend")
                suspend_btn.setStyleSheet("color:brown")
                self.ui.tableWidget.setCellWidget(rowPosition, 4, suspend_btn)

                resume_btn = QPushButton(self.ui.tableWidget)
                resume_btn.setText("Resume")
                resume_btn.setStyleSheet("color:green")
                self.ui.tableWidget.setCellWidget(rowPosition, 5, resume_btn)

                terminate_btn = QPushButton(self.ui.tableWidget)
                terminate_btn.setText("Terminate")
                terminate_btn.setStyleSheet("color:red")
                self.ui.tableWidget.setCellWidget(rowPosition, 6, terminate_btn)

                kill_btn = QPushButton(self.ui.tableWidget)
                kill_btn.setText("Kill")
                kill_btn.setStyleSheet("color:red")
                self.ui.tableWidget.setCellWidget(rowPosition, 7, kill_btn)

            except Exception as e:
                print(f"Process {x} hata verdi: {e}")  # Hangi PID’nin hata verdiğini göster

        self.ui.activity_search.textChanged.connect(self.findName)


    def findName(self):
        name= self.ui.activity_search.text().lower()
        for row in range(self.ui.tableWidget.rowCount()):
            item=self.ui.tableWidget.item(row, 1)
            self.ui.tableWidget.setRowHidden(row, name not in item.text().lower())

    def system_info(self):
        time = datetime.datetime.now().strftime("%I:%M:%S %p")
        self.ui.system_time.setText(str(time))
        date= datetime.datetime.now().strftime("%Y-%m-%d")
        self.ui.system_date.setText(str(date))

        self.ui.system_machine.setText(platform.machine())
        self.ui.system_version.setText(platform.version())
        self.ui.system_platform.setText(platform.platform())
        self.ui.system_system.setText(platform.system())
        self.ui.system_processor.setText(platform.processor())


    def cpu_ram(self,process_callback):
        while True:
            totalRam= 1.0
            totalRam= psutil.virtual_memory()[0]*totalRam
            totalRam= totalRam/(1024*1024*1024)
            self.ui.total_ram.setText(str("{:.4f}".format(totalRam) +" GB"))

            availRam = 1.0
            availRam = psutil.virtual_memory()[1]*availRam
            availRam = availRam/(1024*1024*1024)
            self.ui.avail_ram.setText(str("{:.4f}".format(availRam) +" GB"))

            ramUsed= 1.0
            ramUsed= psutil.virtual_memory()[3]*ramUsed
            ramUsed= ramUsed/(1024*1024*1024)
            self.ui.used_ram.setText(str("{:.4f}".format(ramUsed) +" GB"))

            ramFree= 1.0
            ramFree= psutil.virtual_memory()[4]*ramFree
            ramFree= ramFree/(1024*1024*1024)
            self.ui.free_ram.setText(str("{:.4f}".format(ramFree) +" GB"))

            ramUsages= str(psutil.virtual_memory()[2]) + "%"
            self.ui.ram_usage.setText(str("{:.4f}".format(totalRam)+" GB"))

            core=cpu_count()
            self.ui.cpu_count.setText(str(core))

            cpuPer= psutil.cpu_percent()
            self.ui.cpu_per.setText(str(cpuPer) + "%")

            cpuMainCore = psutil.cpu_count(logical=False)
            self.ui.cpu_main_core.setText(str(cpuMainCore))

            self.ui.cpu_percentage.setMaximumValue(100)
            self.ui.cpu_percentage.setValue(cpuPer)
            self.ui.cpu_percentage.setBarStyle('Line')
            self.ui.cpu_percentage.setLineColor(QColor(51, 187, 232))
            self.ui.cpu_percentage.setTextColor(QColor(255, 255, 255))
            self.ui.cpu_percentage.setPieColor(QColor(16, 92, 117))
            self.ui.cpu_percentage.setInitialPos(('North'))
            self.ui.cpu_percentage.setTextFormat('Percentage')
            self.ui.cpu_percentage.setLineWidth(15)
            self.ui.cpu_percentage.setPathWidth(15)
            self.ui.cpu_percentage.setLineCap('RoundCap')
            #ram spiral  
            
            self.ui.ram_percentage.setMinimumValue((0,0,0))      
            self.ui.ram_percentage.setMaximumValue((totalRam, totalRam, totalRam))
            self.ui.ram_percentage.setValue((availRam, ramUsed, ramFree))
            self.ui.ram_percentage.setLineColor((QColor(6, 233, 38), QColor(6, 201, 233), QColor(233, 6, 201)))
            self.ui.ram_percentage.setInitialPos(('North', 'North', 'North'))
            self.ui.ram_percentage.setLineWidth(15)
            self.ui.ram_percentage.setPathHidden(True)
            self.ui.ram_percentage.setLineCap(('RoundCap','RoundCap','RoundCap'))
            self.ui.ram_percentage.setLineStyle(('SolidLine','SolidLine','SolidLine'))
            sleep(1)








    def slideLeftMenu(self):
        width = self.ui.left_menu_cont_frame.width()
        if width == 40:
            newWidth = 200
        else:
            newWidth = 40
        self.animation = QPropertyAnimation(self.ui.left_menu_cont_frame, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()

    def battery(self, process_callback):
        while True:
            try:
                if not hasattr(psutil, "sensors_battery"):
                    self.ui.battery_status.setText("Platform not supported")
                    return
            
                batt = psutil.sensors_battery()
                if batt is None:
                    self.ui.battery_status.setText("Battery not available")
                    return

            # Pil durumunu güncelle
                self.ui.battery_charge.setText(f"{round(batt.percent, 2)}%")
            
                if batt.power_plugged:
                    self.ui.battery_time_left.setText("N/A")
                    self.ui.battery_status.setText("Charging" if batt.percent < 100 else "Fully Charged")
                    self.ui.battery_plugged.setText("Plugged In")
                else:
                    if batt.secsleft in [psutil.POWER_TIME_UNLIMITED, None] or batt.secsleft <= 0:
                        self.ui.battery_time_left.setText("Calculating...")
                    else:
                        hours = batt.secsleft // 3600
                        minutes = (batt.secsleft % 3600) // 60
                        self.ui.battery_time_left.setText(f"{hours}h {minutes}m")
                
                    self.ui.battery_status.setText("Discharging" if batt.percent < 100 else "Fully Charged")
                    self.ui.battery_plugged.setText("Not Plugged In")

            # RoundProgressBar ayarları
                self.ui.battery_usage.setMaximumValue(100)
                self.ui.battery_usage.setValue(batt.percent)
                self.ui.battery_usage.setBarStyle('Donet')
                self.ui.battery_usage.setLineColor(QColor(51, 187, 232))
                self.ui.battery_usage.setTextColor(QColor(255, 255, 255))
                self.ui.battery_usage.setPieColor(QColor(16, 92, 117))
                self.ui.battery_usage.setInitialPos('West')
                self.ui.battery_usage.setTextFormat('Percentage')
                self.ui.battery_usage.setLineWidth(15)
                self.ui.battery_usage.setPathWidth(15)
                self.ui.battery_usage.setLineCap('RoundCap')
                sleep(1)
            except Exception as e:
                self.ui.battery_status.setText(f"Error: {str(e)}")
            
        
            


    def mousePressEvent(self, event):
            self.clickPosition = event.globalPos()

    #Side Menu Button Style Function
    def applyButtonStyle(self):
        for w in self.ui.menu_frame.findChildren(QPushButton):
            if w.objectName() != self.sender().objectName():
                w.setStyleSheet("border-bottom: none")
        self.sender().setStyleSheet("border-bottom: 2px solid ") 
        return   

    def restore_or_minimize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-maximize.svg'))
        else:
            self.showMaximized()
            self.ui.window_restore_button.setIcon(QIcon('icons/svg/free/cil-window-restore.svg'))

##execute app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec()) 