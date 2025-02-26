# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledbhjkXJ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QStackedWidget,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

from PySideExtn.RoundProgressBar import RoundProgressBar
from PySideExtn.SpiralProgressBar import SpiralProgressBar

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(820, 576)
        MainWindow.setStyleSheet(u"*{\n"
"	\n"
"	background-color: rgb(145, 145, 145);\n"
"	color: rgb(0, 0, 0);\n"
"	border:none;\n"
"}\n"
"QProgressBar{\n"
"background-color:rgb(20,30,43);\n"
"border-style:none;\n"
"border-radius: 10px;\n"
"text-align:center;\n"
"color: rgb(255,0,0)\n"
"}\n"
"QProgressBar::chunk{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0,x2:1,y2:0,stop:0 rgba(0,136,255,255),stop:1 rgba(255,255,255,255));\n"
"border-radius:10px;\n"
"}")
        MainWindow.setDocumentMode(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.header_left_frame = QFrame(self.header_frame)
        self.header_left_frame.setObjectName(u"header_left_frame")
        self.header_left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.header_left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.header_left_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.MenuButton = QPushButton(self.header_left_frame)
        self.MenuButton.setObjectName(u"MenuButton")
        font = QFont()
        font.setBold(True)
        self.MenuButton.setFont(font)
        icon = QIcon()
        icon.addFile(u"icons/menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.MenuButton.setIcon(icon)
        self.MenuButton.setIconSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.MenuButton)


        self.horizontalLayout.addWidget(self.header_left_frame, 0, Qt.AlignmentFlag.AlignLeft)

        self.header_middle_frame = QFrame(self.header_frame)
        self.header_middle_frame.setObjectName(u"header_middle_frame")
        font1 = QFont()
        font1.setPointSize(14)
        self.header_middle_frame.setFont(font1)
        self.header_middle_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.header_middle_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.header_middle_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.header_middle_frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setPixmap(QPixmap(u"icons/airplay.svg"))

        self.horizontalLayout_3.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignRight)

        self.label = QLabel(self.header_middle_frame)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        font2.setItalic(False)
        font2.setUnderline(False)
        font2.setStrikeOut(False)
        self.label.setFont(font2)

        self.horizontalLayout_3.addWidget(self.label)


        self.horizontalLayout.addWidget(self.header_middle_frame)

        self.header_right_frame = QFrame(self.header_frame)
        self.header_right_frame.setObjectName(u"header_right_frame")
        self.header_right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.header_right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header_right_frame)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimize_button = QPushButton(self.header_right_frame)
        self.minimize_button.setObjectName(u"minimize_button")
        icon1 = QIcon()
        icon1.addFile(u"icons/svg/free/cil-window-minimize.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimize_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.minimize_button)

        self.window_restore_button = QPushButton(self.header_right_frame)
        self.window_restore_button.setObjectName(u"window_restore_button")
        icon2 = QIcon()
        icon2.addFile(u"icons/svg/free/cil-window-restore.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.window_restore_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.window_restore_button)

        self.exit_button = QPushButton(self.header_right_frame)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setEnabled(True)
        icon3 = QIcon()
        icon3.addFile(u"icons/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exit_button.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.exit_button)


        self.horizontalLayout.addWidget(self.header_right_frame, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout.addWidget(self.header_frame, 0, Qt.AlignmentFlag.AlignTop)

        self.main_body_frame = QFrame(self.centralwidget)
        self.main_body_frame.setObjectName(u"main_body_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_body_frame.sizePolicy().hasHeightForWidth())
        self.main_body_frame.setSizePolicy(sizePolicy)
        self.main_body_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.main_body_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.main_body_contents = QFrame(self.main_body_frame)
        self.main_body_contents.setObjectName(u"main_body_contents")
        self.main_body_contents.setStyleSheet(u"")
        self.main_body_contents.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body_contents.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.main_body_contents)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.left_menu_cont_frame = QFrame(self.main_body_contents)
        self.left_menu_cont_frame.setObjectName(u"left_menu_cont_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left_menu_cont_frame.sizePolicy().hasHeightForWidth())
        self.left_menu_cont_frame.setSizePolicy(sizePolicy1)
        self.left_menu_cont_frame.setMinimumSize(QSize(40, 0))
        self.left_menu_cont_frame.setMaximumSize(QSize(20, 16777215))
        self.left_menu_cont_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_menu_cont_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.left_menu_cont_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.menu_frame = QFrame(self.left_menu_cont_frame)
        self.menu_frame.setObjectName(u"menu_frame")
        self.menu_frame.setMinimumSize(QSize(200, 0))
        self.menu_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.menu_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.menu_frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.network_button = QPushButton(self.menu_frame)
        self.network_button.setObjectName(u"network_button")
        icon4 = QIcon()
        icon4.addFile(u"icons/wifi.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.network_button.setIcon(icon4)
        self.network_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.network_button, 6, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.battery_button = QPushButton(self.menu_frame)
        self.battery_button.setObjectName(u"battery_button")
        icon5 = QIcon()
        icon5.addFile(u"icons/battery-charging.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.battery_button.setIcon(icon5)
        self.battery_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.battery_button, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.info_button = QPushButton(self.menu_frame)
        self.info_button.setObjectName(u"info_button")
        icon6 = QIcon()
        icon6.addFile(u"icons/monitor.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.info_button.setIcon(icon6)
        self.info_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.info_button, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.sensor_button = QPushButton(self.menu_frame)
        self.sensor_button.setObjectName(u"sensor_button")
        icon7 = QIcon()
        icon7.addFile(u"icons/thermometer.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.sensor_button.setIcon(icon7)
        self.sensor_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.sensor_button, 5, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.activity_button = QPushButton(self.menu_frame)
        self.activity_button.setObjectName(u"activity_button")
        icon8 = QIcon()
        icon8.addFile(u"icons/activity.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.activity_button.setIcon(icon8)
        self.activity_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.activity_button, 3, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.cpu_button = QPushButton(self.menu_frame)
        self.cpu_button.setObjectName(u"cpu_button")
        icon9 = QIcon()
        icon9.addFile(u"icons/cpu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cpu_button.setIcon(icon9)
        self.cpu_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.cpu_button, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.disk_button = QPushButton(self.menu_frame)
        self.disk_button.setObjectName(u"disk_button")
        icon10 = QIcon()
        icon10.addFile(u"icons/hard-drive.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.disk_button.setIcon(icon10)
        self.disk_button.setIconSize(QSize(32, 32))

        self.gridLayout.addWidget(self.disk_button, 4, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_4 = QLabel(self.menu_frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMargin(5)

        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_5 = QLabel(self.menu_frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMargin(5)

        self.gridLayout.addWidget(self.label_5, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_6 = QLabel(self.menu_frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMargin(5)

        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_7 = QLabel(self.menu_frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMargin(5)

        self.gridLayout.addWidget(self.label_7, 3, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_8 = QLabel(self.menu_frame)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMargin(5)

        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_9 = QLabel(self.menu_frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMargin(5)

        self.gridLayout.addWidget(self.label_9, 5, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.label_10 = QLabel(self.menu_frame)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMargin(5)

        self.gridLayout.addWidget(self.label_10, 6, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)


        self.verticalLayout_3.addWidget(self.menu_frame, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_6.addWidget(self.left_menu_cont_frame)

        self.stackedWidget = QStackedWidget(self.main_body_contents)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.cpu_and_memory = QWidget()
        self.cpu_and_memory.setObjectName(u"cpu_and_memory")
        self.gridLayout_5 = QGridLayout(self.cpu_and_memory)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.cpu_info_frame = QFrame(self.cpu_and_memory)
        self.cpu_info_frame.setObjectName(u"cpu_info_frame")
        self.cpu_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cpu_info_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.cpu_info_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.cpu_main_core = QLabel(self.cpu_info_frame)
        self.cpu_main_core.setObjectName(u"cpu_main_core")

        self.gridLayout_2.addWidget(self.cpu_main_core, 2, 1, 1, 1)

        self.label_11 = QLabel(self.cpu_info_frame)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)

        self.label_13 = QLabel(self.cpu_info_frame)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_2.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_15 = QLabel(self.cpu_info_frame)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_2.addWidget(self.label_15, 1, 0, 1, 1)

        self.cpu_count = QLabel(self.cpu_info_frame)
        self.cpu_count.setObjectName(u"cpu_count")

        self.gridLayout_2.addWidget(self.cpu_count, 0, 1, 1, 1)

        self.cpu_per = QLabel(self.cpu_info_frame)
        self.cpu_per.setObjectName(u"cpu_per")

        self.gridLayout_2.addWidget(self.cpu_per, 1, 1, 1, 1)

        self.cpu_percentage = RoundProgressBar(self.cpu_info_frame)
        self.cpu_percentage.setObjectName(u"cpu_percentage")
        self.cpu_percentage.setMinimumSize(QSize(150, 150))
        self.cpu_percentage.setMaximumSize(QSize(150, 150))

        self.gridLayout_2.addWidget(self.cpu_percentage, 0, 2, 3, 1)


        self.gridLayout_5.addWidget(self.cpu_info_frame, 0, 0, 1, 1)

        self.ram_info_frame = QFrame(self.cpu_and_memory)
        self.ram_info_frame.setObjectName(u"ram_info_frame")
        self.ram_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ram_info_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.ram_info_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_17 = QLabel(self.ram_info_frame)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 2, 0, 1, 1)

        self.ram_usage = QLabel(self.ram_info_frame)
        self.ram_usage.setObjectName(u"ram_usage")

        self.gridLayout_3.addWidget(self.ram_usage, 4, 1, 1, 1)

        self.label_20 = QLabel(self.ram_info_frame)
        self.label_20.setObjectName(u"label_20")

        self.gridLayout_3.addWidget(self.label_20, 4, 0, 1, 1)

        self.used_ram = QLabel(self.ram_info_frame)
        self.used_ram.setObjectName(u"used_ram")

        self.gridLayout_3.addWidget(self.used_ram, 2, 1, 1, 1)

        self.label_19 = QLabel(self.ram_info_frame)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 0, 0, 1, 1)

        self.avail_ram = QLabel(self.ram_info_frame)
        self.avail_ram.setObjectName(u"avail_ram")

        self.gridLayout_3.addWidget(self.avail_ram, 1, 1, 1, 1)

        self.total_ram = QLabel(self.ram_info_frame)
        self.total_ram.setObjectName(u"total_ram")

        self.gridLayout_3.addWidget(self.total_ram, 0, 1, 1, 1)

        self.free_ram = QLabel(self.ram_info_frame)
        self.free_ram.setObjectName(u"free_ram")

        self.gridLayout_3.addWidget(self.free_ram, 3, 1, 1, 1)

        self.label_22 = QLabel(self.ram_info_frame)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_3.addWidget(self.label_22, 1, 0, 1, 1)

        self.label_18 = QLabel(self.ram_info_frame)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 3, 0, 1, 1)

        self.ram_percentage = SpiralProgressBar(self.ram_info_frame)
        self.ram_percentage.setObjectName(u"ram_percentage")
        self.ram_percentage.setMinimumSize(QSize(150, 150))
        self.ram_percentage.setMaximumSize(QSize(150, 150))

        self.gridLayout_3.addWidget(self.ram_percentage, 0, 2, 5, 1)


        self.gridLayout_5.addWidget(self.ram_info_frame, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.cpu_and_memory)
        self.battery = QWidget()
        self.battery.setObjectName(u"battery")
        self.verticalLayout_4 = QVBoxLayout(self.battery)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_27 = QLabel(self.battery)
        self.label_27.setObjectName(u"label_27")
        font3 = QFont()
        font3.setBold(True)
        font3.setUnderline(False)
        self.label_27.setFont(font3)

        self.verticalLayout_4.addWidget(self.label_27, 0, Qt.AlignmentFlag.AlignBottom)

        self.frame = QFrame(self.battery)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_30 = QLabel(self.frame)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_4.addWidget(self.label_30, 2, 0, 1, 1)

        self.label_31 = QLabel(self.frame)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_4.addWidget(self.label_31, 3, 0, 1, 1)

        self.battery_charge = QLabel(self.frame)
        self.battery_charge.setObjectName(u"battery_charge")

        self.gridLayout_4.addWidget(self.battery_charge, 1, 1, 1, 1)

        self.label_28 = QLabel(self.frame)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_4.addWidget(self.label_28, 0, 0, 1, 1)

        self.battery_plugged = QLabel(self.frame)
        self.battery_plugged.setObjectName(u"battery_plugged")

        self.gridLayout_4.addWidget(self.battery_plugged, 3, 1, 1, 1)

        self.label_29 = QLabel(self.frame)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_4.addWidget(self.label_29, 1, 0, 1, 1)

        self.battery_time_left = QLabel(self.frame)
        self.battery_time_left.setObjectName(u"battery_time_left")

        self.gridLayout_4.addWidget(self.battery_time_left, 2, 1, 1, 1)

        self.battery_status = QLabel(self.frame)
        self.battery_status.setObjectName(u"battery_status")

        self.gridLayout_4.addWidget(self.battery_status, 0, 1, 1, 1)

        self.battery_usage = RoundProgressBar(self.frame)
        self.battery_usage.setObjectName(u"battery_usage")
        self.battery_usage.setMinimumSize(QSize(150, 150))
        self.battery_usage.setMaximumSize(QSize(150, 150))

        self.gridLayout_4.addWidget(self.battery_usage, 1, 2, 2, 1)


        self.verticalLayout_4.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignTop)

        self.stackedWidget.addWidget(self.battery)
        self.system_info = QWidget()
        self.system_info.setObjectName(u"system_info")
        self.verticalLayout_5 = QVBoxLayout(self.system_info)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_2 = QFrame(self.system_info)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_39 = QLabel(self.frame_2)
        self.label_39.setObjectName(u"label_39")
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.label_39.setFont(font4)

        self.gridLayout_6.addWidget(self.label_39, 3, 0, 1, 1)

        self.system_system = QLabel(self.frame_2)
        self.system_system.setObjectName(u"system_system")
        self.system_system.setFont(font4)

        self.gridLayout_6.addWidget(self.system_system, 1, 0, 1, 1)

        self.label_40 = QLabel(self.frame_2)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setFont(font4)

        self.gridLayout_6.addWidget(self.label_40, 4, 0, 1, 1)

        self.system_platform = QLabel(self.frame_2)
        self.system_platform.setObjectName(u"system_platform")

        self.gridLayout_6.addWidget(self.system_platform, 2, 1, 1, 1)

        self.label_44 = QLabel(self.frame_2)
        self.label_44.setObjectName(u"label_44")
        self.label_44.setFont(font4)

        self.gridLayout_6.addWidget(self.label_44, 2, 2, 1, 1)

        self.label_45 = QLabel(self.frame_2)
        self.label_45.setObjectName(u"label_45")
        self.label_45.setFont(font4)

        self.gridLayout_6.addWidget(self.label_45, 3, 2, 1, 1)

        self.label_38 = QLabel(self.frame_2)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font4)

        self.gridLayout_6.addWidget(self.label_38, 2, 0, 1, 1)

        self.label_46 = QLabel(self.frame_2)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setFont(font4)

        self.gridLayout_6.addWidget(self.label_46, 4, 2, 1, 1)

        self.system_date = QLabel(self.frame_2)
        self.system_date.setObjectName(u"system_date")

        self.gridLayout_6.addWidget(self.system_date, 4, 1, 1, 1)

        self.label_36 = QLabel(self.frame_2)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font4)

        self.gridLayout_6.addWidget(self.label_36, 0, 0, 1, 1, Qt.AlignmentFlag.AlignTop)

        self.system_version = QLabel(self.frame_2)
        self.system_version.setObjectName(u"system_version")

        self.gridLayout_6.addWidget(self.system_version, 3, 1, 1, 1)

        self.system_processor = QLabel(self.frame_2)
        self.system_processor.setObjectName(u"system_processor")

        self.gridLayout_6.addWidget(self.system_processor, 2, 3, 1, 1)

        self.system_machine = QLabel(self.frame_2)
        self.system_machine.setObjectName(u"system_machine")

        self.gridLayout_6.addWidget(self.system_machine, 3, 3, 1, 1)

        self.system_time = QLabel(self.frame_2)
        self.system_time.setObjectName(u"system_time")

        self.gridLayout_6.addWidget(self.system_time, 4, 3, 1, 1)


        self.verticalLayout_5.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignTop)

        self.stackedWidget.addWidget(self.system_info)
        self.activities = QWidget()
        self.activities.setObjectName(u"activities")
        self.verticalLayout_6 = QVBoxLayout(self.activities)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.frame_3 = QFrame(self.activities)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_50 = QLabel(self.frame_3)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font4)

        self.horizontalLayout_7.addWidget(self.label_50, 0, Qt.AlignmentFlag.AlignLeft)

        self.frame_6 = QFrame(self.frame_3)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMaximumSize(QSize(133, 16777215))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_6.setLineWidth(1)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(10, -1, 10, 0)
        self.activity_search = QLineEdit(self.frame_6)
        self.activity_search.setObjectName(u"activity_search")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.activity_search.sizePolicy().hasHeightForWidth())
        self.activity_search.setSizePolicy(sizePolicy2)
        self.activity_search.setStyleSheet(u"*{\n"
"	\n"
"	background-color: rgb(106, 106, 106);\n"
"}")
        self.activity_search.setMaxLength(32767)
        self.activity_search.setClearButtonEnabled(False)

        self.horizontalLayout_8.addWidget(self.activity_search)

        self.pushButton = QPushButton(self.frame_6)
        self.pushButton.setObjectName(u"pushButton")
        icon11 = QIcon()
        icon11.addFile(u"icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon11)

        self.horizontalLayout_8.addWidget(self.pushButton)


        self.horizontalLayout_7.addWidget(self.frame_6, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.activities)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tableWidget = QTableWidget(self.frame_4)
        if (self.tableWidget.columnCount() < 8):
            self.tableWidget.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_7.addWidget(self.tableWidget)


        self.verticalLayout_6.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.activities)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton_2 = QPushButton(self.frame_5)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_9.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame_5)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_9.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame_5)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_9.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.frame_5)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_9.addWidget(self.pushButton_5)


        self.verticalLayout_6.addWidget(self.frame_5, 0, Qt.AlignmentFlag.AlignBottom)

        self.stackedWidget.addWidget(self.activities)
        self.storage = QWidget()
        self.storage.setObjectName(u"storage")
        self.verticalLayout_8 = QVBoxLayout(self.storage)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_51 = QLabel(self.storage)
        self.label_51.setObjectName(u"label_51")
        font5 = QFont()
        font5.setPointSize(12)
        font5.setBold(True)
        self.label_51.setFont(font5)

        self.verticalLayout_8.addWidget(self.label_51)

        self.storageTable = QTableWidget(self.storage)
        if (self.storageTable.columnCount() < 10):
            self.storageTable.setColumnCount(10)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(1, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(2, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(3, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(4, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(5, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(6, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(7, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(8, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.storageTable.setHorizontalHeaderItem(9, __qtablewidgetitem17)
        self.storageTable.setObjectName(u"storageTable")

        self.verticalLayout_8.addWidget(self.storageTable)

        self.stackedWidget.addWidget(self.storage)
        self.sensors = QWidget()
        self.sensors.setObjectName(u"sensors")
        self.verticalLayout_9 = QVBoxLayout(self.sensors)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_52 = QLabel(self.sensors)
        self.label_52.setObjectName(u"label_52")
        self.label_52.setFont(font5)

        self.verticalLayout_9.addWidget(self.label_52)

        self.sensorsTable = QTableWidget(self.sensors)
        if (self.sensorsTable.columnCount() < 6):
            self.sensorsTable.setColumnCount(6)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(1, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(2, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(3, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(4, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.sensorsTable.setHorizontalHeaderItem(5, __qtablewidgetitem23)
        self.sensorsTable.setObjectName(u"sensorsTable")

        self.verticalLayout_9.addWidget(self.sensorsTable)

        self.stackedWidget.addWidget(self.sensors)
        self.networks = QWidget()
        self.networks.setObjectName(u"networks")
        self.horizontalLayout_10 = QHBoxLayout(self.networks)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.scrollArea = QScrollArea(self.networks)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 708, 907))
        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(-1, -1, -1, 100)
        self.frame_7 = QFrame(self.scrollAreaWidgetContents)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_7)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_53 = QLabel(self.frame_7)
        self.label_53.setObjectName(u"label_53")
        self.label_53.setFont(font5)

        self.verticalLayout_11.addWidget(self.label_53)

        self.net_stats_table = QTableWidget(self.frame_7)
        if (self.net_stats_table.columnCount() < 5):
            self.net_stats_table.setColumnCount(5)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.net_stats_table.setHorizontalHeaderItem(0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.net_stats_table.setHorizontalHeaderItem(1, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.net_stats_table.setHorizontalHeaderItem(2, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.net_stats_table.setHorizontalHeaderItem(3, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.net_stats_table.setHorizontalHeaderItem(4, __qtablewidgetitem28)
        self.net_stats_table.setObjectName(u"net_stats_table")
        self.net_stats_table.setMinimumSize(QSize(0, 150))

        self.verticalLayout_11.addWidget(self.net_stats_table)


        self.verticalLayout_10.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.scrollAreaWidgetContents)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_8)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_54 = QLabel(self.frame_8)
        self.label_54.setObjectName(u"label_54")
        self.label_54.setFont(font5)

        self.verticalLayout_12.addWidget(self.label_54)

        self.net_io_table = QTableWidget(self.frame_8)
        if (self.net_io_table.columnCount() < 9):
            self.net_io_table.setColumnCount(9)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(1, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(2, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(3, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(4, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(5, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(6, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(7, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.net_io_table.setHorizontalHeaderItem(8, __qtablewidgetitem37)
        self.net_io_table.setObjectName(u"net_io_table")
        self.net_io_table.setMinimumSize(QSize(0, 150))

        self.verticalLayout_12.addWidget(self.net_io_table)


        self.verticalLayout_10.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.scrollAreaWidgetContents)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_9)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_55 = QLabel(self.frame_9)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setFont(font5)

        self.verticalLayout_13.addWidget(self.label_55)

        self.net_addr_table = QTableWidget(self.frame_9)
        if (self.net_addr_table.columnCount() < 6):
            self.net_addr_table.setColumnCount(6)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(0, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(1, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(2, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(3, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(4, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.net_addr_table.setHorizontalHeaderItem(5, __qtablewidgetitem43)
        self.net_addr_table.setObjectName(u"net_addr_table")
        self.net_addr_table.setMinimumSize(QSize(0, 150))

        self.verticalLayout_13.addWidget(self.net_addr_table)


        self.verticalLayout_10.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.scrollAreaWidgetContents)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_10)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_56 = QLabel(self.frame_10)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setFont(font5)

        self.verticalLayout_14.addWidget(self.label_56)

        self.net_conn_table = QTableWidget(self.frame_10)
        if (self.net_conn_table.columnCount() < 7):
            self.net_conn_table.setColumnCount(7)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(0, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(1, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(2, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(3, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(4, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(5, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.net_conn_table.setHorizontalHeaderItem(6, __qtablewidgetitem50)
        self.net_conn_table.setObjectName(u"net_conn_table")
        self.net_conn_table.setMinimumSize(QSize(0, 150))

        self.verticalLayout_14.addWidget(self.net_conn_table)


        self.verticalLayout_10.addWidget(self.frame_10)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_10.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.networks)

        self.horizontalLayout_6.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.main_body_contents)


        self.verticalLayout.addWidget(self.main_body_frame)

        self.footer_frame = QFrame(self.centralwidget)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(250, 34))
        self.footer_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.footer_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.footer_frame)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)


        self.verticalLayout.addWidget(self.footer_frame, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.MenuButton.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.label_2.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"System Monitoring Application", None))
        self.minimize_button.setText("")
        self.window_restore_button.setText("")
        self.exit_button.setText("")
        self.network_button.setText("")
        self.battery_button.setText("")
        self.info_button.setText("")
        self.sensor_button.setText("")
        self.activity_button.setText("")
        self.cpu_button.setText("")
        self.disk_button.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"CPU", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Battery", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"System \u0130nformation", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Storage", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Network", None))
        self.cpu_main_core.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"CPU Count", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"CPU Main Core", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"CPU %", None))
        self.cpu_count.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.cpu_per.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Used RAM", None))
        self.ram_usage.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Ram Usage", None))
        self.used_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Total RAM", None))
        self.avail_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.total_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.free_ram.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Available RAM", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Free RAM", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Battery Information", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Plugged In", None))
        self.battery_charge.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.battery_plugged.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Charge", None))
        self.battery_time_left.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.battery_status.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.system_system.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"System Date", None))
        self.system_platform.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_44.setText(QCoreApplication.translate("MainWindow", u"Processor", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"Machine", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Platform", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"System Time", None))
        self.system_date.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"System Information", None))
        self.system_version.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_processor.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_machine.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.system_time.setText(QCoreApplication.translate("MainWindow", u"N/A", None))
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"Activities", None))
        self.activity_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search Processes", None))
        self.pushButton.setText("")
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Process ID", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Process Name", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Process Status", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Started", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Suspend", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Resume", None));
        ___qtablewidgetitem6 = self.tableWidget.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Terminate", None));
        ___qtablewidgetitem7 = self.tableWidget.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Kill", None));
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Suspend", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Terminate", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Kill", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Disk Partition", None))
        ___qtablewidgetitem8 = self.storageTable.horizontalHeaderItem(0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Device", None));
        ___qtablewidgetitem9 = self.storageTable.horizontalHeaderItem(1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Mount Point", None));
        ___qtablewidgetitem10 = self.storageTable.horizontalHeaderItem(2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"OPTS", None));
        ___qtablewidgetitem11 = self.storageTable.horizontalHeaderItem(3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"MAX", None));
        ___qtablewidgetitem12 = self.storageTable.horizontalHeaderItem(4)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Max File", None));
        ___qtablewidgetitem13 = self.storageTable.horizontalHeaderItem(5)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Max Path", None));
        ___qtablewidgetitem14 = self.storageTable.horizontalHeaderItem(6)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Total Storage", None));
        ___qtablewidgetitem15 = self.storageTable.horizontalHeaderItem(7)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Used Storage", None));
        ___qtablewidgetitem16 = self.storageTable.horizontalHeaderItem(8)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Free Storage", None));
        self.label_52.setText(QCoreApplication.translate("MainWindow", u"Sensors", None))
        ___qtablewidgetitem17 = self.sensorsTable.horizontalHeaderItem(0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"Sensor", None));
        ___qtablewidgetitem18 = self.sensorsTable.horizontalHeaderItem(1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Label", None));
        ___qtablewidgetitem19 = self.sensorsTable.horizontalHeaderItem(2)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Current", None));
        ___qtablewidgetitem20 = self.sensorsTable.horizontalHeaderItem(3)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"High", None));
        ___qtablewidgetitem21 = self.sensorsTable.horizontalHeaderItem(4)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Critical", None));
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"Stats", None))
        ___qtablewidgetitem22 = self.net_stats_table.horizontalHeaderItem(1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"ISUP", None));
        ___qtablewidgetitem23 = self.net_stats_table.horizontalHeaderItem(2)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Duplex", None));
        ___qtablewidgetitem24 = self.net_stats_table.horizontalHeaderItem(3)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"Speed", None));
        ___qtablewidgetitem25 = self.net_stats_table.horizontalHeaderItem(4)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"MTU", None));
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Network IO Counters", None))
        ___qtablewidgetitem26 = self.net_io_table.horizontalHeaderItem(0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"IO", None));
        ___qtablewidgetitem27 = self.net_io_table.horizontalHeaderItem(1)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"Bytes Sent", None));
        ___qtablewidgetitem28 = self.net_io_table.horizontalHeaderItem(2)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"Bytes Received", None));
        ___qtablewidgetitem29 = self.net_io_table.horizontalHeaderItem(3)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"Packets Sent", None));
        ___qtablewidgetitem30 = self.net_io_table.horizontalHeaderItem(4)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"Packets Received", None));
        ___qtablewidgetitem31 = self.net_io_table.horizontalHeaderItem(5)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"ERR IN", None));
        ___qtablewidgetitem32 = self.net_io_table.horizontalHeaderItem(6)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"ERR OUT", None));
        ___qtablewidgetitem33 = self.net_io_table.horizontalHeaderItem(7)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"Drop In", None));
        ___qtablewidgetitem34 = self.net_io_table.horizontalHeaderItem(8)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"Drop Out", None));
        self.label_55.setText(QCoreApplication.translate("MainWindow", u"Network Adresses", None))
        ___qtablewidgetitem35 = self.net_addr_table.horizontalHeaderItem(1)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"Family", None));
        ___qtablewidgetitem36 = self.net_addr_table.horizontalHeaderItem(2)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"Address", None));
        ___qtablewidgetitem37 = self.net_addr_table.horizontalHeaderItem(3)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"Netmask", None));
        ___qtablewidgetitem38 = self.net_addr_table.horizontalHeaderItem(4)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"Broadcast", None));
        ___qtablewidgetitem39 = self.net_addr_table.horizontalHeaderItem(5)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"PTP", None));
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"Network Connections", None))
        ___qtablewidgetitem40 = self.net_conn_table.horizontalHeaderItem(0)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"FD", None));
        ___qtablewidgetitem41 = self.net_conn_table.horizontalHeaderItem(1)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"Family", None));
        ___qtablewidgetitem42 = self.net_conn_table.horizontalHeaderItem(2)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"Family", None));
        ___qtablewidgetitem43 = self.net_conn_table.horizontalHeaderItem(3)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"LADDR", None));
        ___qtablewidgetitem44 = self.net_conn_table.horizontalHeaderItem(4)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"RADDR", None));
        ___qtablewidgetitem45 = self.net_conn_table.horizontalHeaderItem(5)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem46 = self.net_conn_table.horizontalHeaderItem(6)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"PID", None));
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Version 0.1  | Ahmet Eren Erkek - 2110213015", None))
    # retranslateUi

