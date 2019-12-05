# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Cell_Voltage_Simulate_Tool.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!



import threading
import sys
import os
import struct
import random
from ctypes import *
import time
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QTimer,QDateTime

CANDeviceNameNumber = 4
CANBuffer = [0 for y in range(50)]#50帧的数据缓存
Data_RefreshTimer = QTimer()

Cell_Dict = {
    '电压':3.200,
    '电流':0,
    '温度':25.5,
    '容量':100,
    '电池类型':1,
    '剩余容量':0
}

S2V_Voltage_Charge = [2099	,
2184	,
2194	,
2203	,
2213	,
2223	,
2234	,
2243	,
2256	,
2267	,
2282	,
2299	,
2321	,
2344	,
2365	,
2403	,
2444	,
2477	,
2516	,
2576	,
2700	]
S2V_Voltage_Stand = [1920,
                     1935,
                     1950,
                     1960,
                     1970,
                     1985,
                     2000,
                     2010,
                     2020,
                     2025,
                     2030,
                     2040,
                     2050,
                     2060,
                     2070,
                     2080,
                     2090,
                     2100,
                     2110,
                     2115,
                     2130]
S2V_Voltage_Discharge = [1805	,
1827	,
1842	,
1858	,
1874	,
1890	,
1906	,
1922	,
1938	,
1954	,
1970	,
1985	,
2000	,
2015	,
2030	,
2045	,
2060	,
2075	,
2090	,
2105	,
2120]


S3200V_Voltage_Charge = [
3023 	,
3245 	,
3285 	,
3307 	,
3325 	,
3335 	,
3345 	,
3353 	,
3360 	,
3363 	,
3365 	,
3370 	,
3378 	,
3380 	,
3388 	,
3393 	,
3400 	,
3413 	,
3423 	,
3470 	,
3650
]
S3200V_Voltage_Stand = [
2925	,
3179	,
3208	,
3230	,
3253	,
3269	,
3281	,
3287	,
3288	,
3289	,
3291	,
3298	,
3310	,
3321	,
3325	,
3326	,
3330	,
3336	,
3339	,
3340	,
3353]
S3200V_Voltage_Discharge = [2500	,
2909	,
3067	,
3099	,
3134	,
3154	,
3172	,
3186	,
3201	,
3208	,
3212	,
3216	,
3219	,
3225	,
3234	,
3245	,
3250	,
3253	,
3254	,
3255	,
3267	]

S3600V_Voltage_Charge = [3023 	,
3385 	,
3515 	,
3547 	,
3582 	,
3621 	,
3652 	,
3674 	,
3695 	,
3722 	,
3749 	,
3777 	,
3805 	,
3852 	,
3900 	,
3949 	,
3999 	,
4054 	,
4108 	,
4148 	,
4210 ]
S3600V_Voltage_Stand = [3142 	,
3384 	,
3483 	,
3509 	,
3543 	,
3576 	,
3602 	,
3631 	,
3657 	,
3677 	,
3700 	,
3728 	,
3761 	,
3800 	,
3851 	,
3918 	,
3972 	,
4027 	,
4084 	,
4147 	,
4214]
S3600V_Voltage_Discharge = [2900	,
3285	,
3424	,
3461	,
3498	,
3528	,
3559	,
3583	,
3608	,
3632	,
3656	,
3693	,
3730	,
3768	,
3805	,
3857	,
3910	,
3971	,
4032	,
4096	,
4155	]


class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]

class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte * 8),
                ('Reserved', c_byte * 3)]

class StoppableThread(threading.Thread):
    def __init__(self, daemon=None):
        super(StoppableThread, self).__init__(daemon=daemon)
        self.__is_running = True
        self.daemon = daemon
    def terminate(self):
        self.__is_running = False
    def run(self):
        global Cell_Dict

        self.CAN_Connect()
        while self.__is_running:
            i = 0
            time.sleep(0.5)
            self.CAN_Pro()

    def CAN_Connect(self):
        global CANDeviceNameNumber

        vic = _VCI_INIT_CONFIG()
        vic.AccCode = 0x00000000
        vic.AccMask = 0xffffffff
        vic.Filter = 0
        vic.Timing0 = 0x01
        vic.Timing1 = 0x1C
        vic.Mode = 0

        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        returnFlag = canLib.VCI_OpenDevice(CANDeviceNameNumber, 0, 0)
        if returnFlag == -1:
            return -1  # returnFlag
        returnFlag = canLib.VCI_InitCAN(CANDeviceNameNumber, 0, 0, pointer(vic))
        if returnFlag == -1:
            return -2  # returnFlag
        returnFlag = canLib.VCI_StartCAN(CANDeviceNameNumber, 0, 0)
        if returnFlag == -1:
            return -3  # returnFlag

    def CAN_Pro(self):
        global CANDeviceNameNumber
        global CANBuffer

        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        Voc = _VCI_CAN_OBJ()
        Num = canLib.VCI_GetReceiveNum(CANDeviceNameNumber, 0, 0)
        for i in range(Num):
            if Num > 0 and Num < 50:
                ret = canLib.VCI_Receive(CANDeviceNameNumber, 0, 0, byref(Voc), 1, 0)
                CANBuffer[i] = Voc.ID
                # print(Voc.ID)
            else:
                break

        for i in range(50):
            if (CANBuffer[i] & 0xFF00) != 0x6400:
                if CANBuffer[i] & 0xFF0000 == 0x010000:  # 电压

                    CAN_ID = 0x18816400 + (CANBuffer[i] & 0xFF00) // 256
                    if CAN_ID == 0x18816464 or CAN_ID == 0x18826464:
                        pass
                    for k in range(6):
                        CAN_data = (0, k * 3 + 1,)
                        for j in range(3):
                            temp_random = int(Cell_Dict['电压'] * 1000 + random.randint(0, 10) - 5)
                            CAN_data = CAN_data + (temp_random // 256,)
                            CAN_data = CAN_data + (temp_random % 256,)
                        self.CAN_Send(CAN_ID, CAN_data)
                        time.sleep(0.01)
                elif CANBuffer[i] & 0xFF0000 == 0x020000:  # 温度
                    CAN_ID = 0x18826400 + (CANBuffer[i] & 0xFF00) // 256
                    for k in range(6):
                        CAN_data = (0, k * 3 + 1,)
                        for j in range(3):
                            temp_random = int(Cell_Dict['温度'] * 10 + 400 + random.randint(0, 20) - 10)
                            CAN_data = CAN_data + (temp_random // 256,)
                            CAN_data = CAN_data + (temp_random % 256,)
                        self.CAN_Send(CAN_ID, CAN_data)
                        time.sleep(0.01)
                else:
                    pass
        canLib.VCI_ClearBuffer(CANDeviceNameNumber, 0, 0)


    #CAN发送数据
    def CAN_Send(self, CAN_ID, Data):
        global CANDeviceNameNumber

        canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
        vco = _VCI_CAN_OBJ()
        vco.ID = CAN_ID
        vco.SendType = 0
        vco.RemoteFlag = 0
        vco.ExternFlag = 1
        vco.DataLen = 8
        vco.Data = Data
        ReturnFlag = canLib.VCI_Transmit(CANDeviceNameNumber, 0, 0,pointer(vco), 1)

class Ui_Cell_Voltage_Simulate_Tool(object):
    def setupUi(self, Cell_Voltage_Simulate_Tool):
        Cell_Voltage_Simulate_Tool.setObjectName("Cell_Voltage_Simulate_Tool")
        Cell_Voltage_Simulate_Tool.resize(716, 276)
        self.centralwidget = QtWidgets.QWidget(Cell_Voltage_Simulate_Tool)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_OpenCAN = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_OpenCAN.setGeometry(QtCore.QRect(130, 10, 91, 31))
        self.pushButton_OpenCAN.setObjectName("pushButton_OpenCAN")
        self.comboBox_CANType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_CANType.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.comboBox_CANType.setObjectName("comboBox_CANType")
        self.comboBox_CANType.addItem("")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 50, 821, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_StartSystem = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_StartSystem.setGeometry(QtCore.QRect(600, 10, 101, 41))
        self.pushButton_StartSystem.setObjectName("pushButton_StartSystem")
        self.comboBox_CellType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_CellType.setGeometry(QtCore.QRect(80, 80, 111, 31))
        self.comboBox_CellType.setObjectName("comboBox_CellType")
        self.comboBox_CellType.addItem("")
        self.comboBox_CellType.addItem("")
        self.comboBox_CellType.addItem("")
        self.comboBox_CellType.addItem("")
        self.label_CellType = QtWidgets.QLabel(self.centralwidget)
        self.label_CellType.setGeometry(QtCore.QRect(10, 90, 61, 16))
        self.label_CellType.setObjectName("label_CellType")
        self.label_CellVoltage = QtWidgets.QLabel(self.centralwidget)
        self.label_CellVoltage.setGeometry(QtCore.QRect(340, 140, 61, 16))
        self.label_CellVoltage.setObjectName("label_CellVoltage")
        self.lineEdit_CellVoltage = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellVoltage.setGeometry(QtCore.QRect(410, 130, 111, 31))
        self.lineEdit_CellVoltage.setObjectName("lineEdit_CellVoltage")
        self.label_CellTemp = QtWidgets.QLabel(self.centralwidget)
        self.label_CellTemp.setGeometry(QtCore.QRect(430, 90, 61, 16))
        self.label_CellTemp.setObjectName("label_CellTemp")
        self.lineEdit_CellTemp = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellTemp.setGeometry(QtCore.QRect(500, 80, 111, 31))
        self.lineEdit_CellTemp.setObjectName("lineEdit_CellTemp")
        self.label_CellCurrent = QtWidgets.QLabel(self.centralwidget)
        self.label_CellCurrent.setGeometry(QtCore.QRect(10, 140, 61, 16))
        self.label_CellCurrent.setObjectName("label_CellCurrent")
        self.lineEdit_CellCurrent = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellCurrent.setGeometry(QtCore.QRect(80, 130, 111, 31))
        self.lineEdit_CellCurrent.setObjectName("lineEdit_CellCurrent")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(-10, 170, 821, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_CellCAP = QtWidgets.QLabel(self.centralwidget)
        self.label_CellCAP.setGeometry(QtCore.QRect(220, 90, 61, 16))
        self.label_CellCAP.setObjectName("label_CellCAP")
        self.lineEdit_CellCAP = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellCAP.setGeometry(QtCore.QRect(290, 80, 111, 31))
        self.lineEdit_CellCAP.setObjectName("lineEdit_CellCAP")
        self.pushButton_CurSet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_CurSet.setGeometry(QtCore.QRect(220, 130, 71, 31))
        self.pushButton_CurSet.setObjectName("pushButton_CurSet")
        self.pushButton_VolSet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_VolSet.setGeometry(QtCore.QRect(540, 130, 71, 31))
        self.pushButton_VolSet.setObjectName("pushButton_VolSet")
        self.checkBox_AutoMode = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_AutoMode.setGeometry(QtCore.QRect(480, 20, 111, 21))
        self.checkBox_AutoMode.setObjectName("checkBox_AutoMode")
        self.label_CellVOL_NOW = QtWidgets.QLabel(self.centralwidget)
        self.label_CellVOL_NOW.setEnabled(False)
        self.label_CellVOL_NOW.setGeometry(QtCore.QRect(20, 210, 61, 16))
        self.label_CellVOL_NOW.setObjectName("label_CellVOL_NOW")
        self.lineEdit_CellVOL_NOW = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellVOL_NOW.setEnabled(False)
        self.lineEdit_CellVOL_NOW.setGeometry(QtCore.QRect(90, 200, 111, 31))
        self.lineEdit_CellVOL_NOW.setObjectName("lineEdit_CellVOL_NOW")
        self.label_CellCurrent_NOW = QtWidgets.QLabel(self.centralwidget)
        self.label_CellCurrent_NOW.setEnabled(False)
        self.label_CellCurrent_NOW.setGeometry(QtCore.QRect(220, 210, 61, 16))
        self.label_CellCurrent_NOW.setObjectName("label_CellCurrent_NOW")
        self.lineEdit_CellCurrent_NOW = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellCurrent_NOW.setEnabled(False)
        self.lineEdit_CellCurrent_NOW.setGeometry(QtCore.QRect(290, 200, 111, 31))
        self.lineEdit_CellCurrent_NOW.setObjectName("lineEdit_CellCurrent_NOW")
        self.label_CellCAP_NOW = QtWidgets.QLabel(self.centralwidget)
        self.label_CellCAP_NOW.setEnabled(False)
        self.label_CellCAP_NOW.setGeometry(QtCore.QRect(440, 210, 61, 16))
        self.label_CellCAP_NOW.setObjectName("label_CellCAP_NOW")
        self.lineEdit_CellCAP_NOW = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellCAP_NOW.setEnabled(False)
        self.lineEdit_CellCAP_NOW.setGeometry(QtCore.QRect(510, 200, 111, 31))
        self.lineEdit_CellCAP_NOW.setObjectName("lineEdit_CellCAP_NOW")
        Cell_Voltage_Simulate_Tool.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Cell_Voltage_Simulate_Tool)
        self.statusbar.setObjectName("statusbar")
        Cell_Voltage_Simulate_Tool.setStatusBar(self.statusbar)

        self.retranslateUi(Cell_Voltage_Simulate_Tool)
        self.pushButton_OpenCAN.clicked.connect(self.CAN_Connect)
        Data_RefreshTimer.timeout.connect(self.CAN_DataReflash)
        self.pushButton_CurSet.clicked.connect(self.Current_Set)
        self.pushButton_VolSet.clicked.connect(self.Voltage_Set)
        self.pushButton_StartSystem.clicked.connect(self.Tool_Start)
        QtCore.QMetaObject.connectSlotsByName(Cell_Voltage_Simulate_Tool)

    def CAN_Connect(self):
        global CANDeviceNameNumber

        temp = self.pushButton_OpenCAN.text()
        if temp == '打开CAN通讯':
            vic = _VCI_INIT_CONFIG()
            vic.AccCode = 0x00000000
            vic.AccMask = 0xffffffff
            vic.Filter = 0
            vic.Timing0 = 0x01
            vic.Timing1 = 0x1C
            vic.Mode = 0

            temp = self.comboBox_CANType.currentIndex()
            if temp == 0:
                CANDeviceNameNumber = 4
            elif temp == 1:
                CANDeviceNameNumber = 4

            canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
            returnFlag = canLib.VCI_OpenDevice(CANDeviceNameNumber, 0, 0)
            if returnFlag == -1:
                return -1#returnFlag
            returnFlag = canLib.VCI_InitCAN(CANDeviceNameNumber, 0, 0, pointer(vic))
            if returnFlag == -1:
                return -2#returnFlag
            returnFlag = canLib.VCI_StartCAN(CANDeviceNameNumber, 0, 0)
            if returnFlag == -1:
                return -3#returnFlag
            canLib.VCI_CloseDevice(CANDeviceNameNumber, 0)
            self.pushButton_OpenCAN.setText('关闭CAN通讯')
            self.comboBox_CANType.setEnabled(False)
        else:
            canLib = windll.LoadLibrary('.\DLL\ControlCAN.dll')
            canLib.VCI_CloseDevice(CANDeviceNameNumber, 0)
            self.pushButton_OpenCAN.setText('打开CAN通讯')
            self.comboBox_CANType.setEnabled(True)

    def Current_Set(self):
        global Cell_Dict

        temp = float(self.lineEdit_CellCurrent.text())
        Cell_Dict['电流'] = temp

    def Voltage_Set(self):
        global Cell_Dict

        temp = float(self.lineEdit_CellVoltage.text())
        Cell_Dict['电压'] = temp

    def Tool_Start(self):
        global S2V_Voltage_Stand
        global S3200V_Voltage_Stand
        global S3600V_Voltage_Stand
        global Cell_Dict

        text = self.pushButton_StartSystem.text()
        if text == '启动':
            temp = float(self.lineEdit_CellCAP.text())
            self.lineEdit_CellCAP.setEnabled(False)
            Cell_Dict['容量'] = temp
            temp = float(self.lineEdit_CellTemp.text())
            self.comboBox_CellType.setEnabled(False)
            Cell_Dict['温度'] = temp
            temp = self.comboBox_CellType.currentIndex()
            self.comboBox_CellType.setEnabled(False)
            Cell_Dict['电池类型'] = temp+1
            self.pushButton_StartSystem.setText('结束')
            Data_RefreshTimer.start(50)
            self.thread = StoppableThread()
            self.thread.daemon = True
            self.thread.start()
            if Cell_Dict['电池类型'] == 1:#6V铅酸
                for i in range(20):
                    if Cell_Dict['电压'] > S2V_Voltage_Stand[i]*3 and  Cell_Dict['电压'] < S2V_Voltage_Stand[i+1]*3:
                        Cell_Dict['剩余容量'] = Cell_Dict['容量'] * \
                                            ((i+1) / 20 + (Cell_Dict['电压'] - S2V_Voltage_Stand[i])/(S2V_Voltage_Stand[i+1] - S2V_Voltage_Stand[i])*0.05)
            elif Cell_Dict['电池类型'] == 2:#12V铅酸
                for i in range(20):
                    if Cell_Dict['电压'] > S2V_Voltage_Stand[i]*6 and  Cell_Dict['电压'] < S2V_Voltage_Stand[i+1]*6:
                        Cell_Dict['剩余容量'] = Cell_Dict['容量'] * \
                                            ((i+1) / 20 + (Cell_Dict['电压'] - S2V_Voltage_Stand[i])/(S2V_Voltage_Stand[i+1] - S2V_Voltage_Stand[i])*0.05)
            elif Cell_Dict['电池类型'] == 3:#另算铁力
                for i in range(20):
                    if Cell_Dict['电压'] > S3200V_Voltage_Stand[i]*3 and  Cell_Dict['电压'] < S3200V_Voltage_Stand[i+1]*3:
                        Cell_Dict['剩余容量'] = Cell_Dict['容量'] * \
                                            ((i+1) / 20 + (Cell_Dict['电压'] - S3200V_Voltage_Stand[i])/(S3200V_Voltage_Stand[i+1] - S3200V_Voltage_Stand[i])*0.05)
            elif Cell_Dict['电池类型'] == 4:#三元
                for i in range(20):
                    if Cell_Dict['电压'] > S3600V_Voltage_Stand[i]*3 and  Cell_Dict['电压'] < S3600V_Voltage_Stand[i+1]*3:
                        Cell_Dict['剩余容量'] = Cell_Dict['容量'] * \
                                            ((i+1) / 20 + (Cell_Dict['电压'] - S3600V_Voltage_Stand[i])/(S3600V_Voltage_Stand[i+1] - S3600V_Voltage_Stand[i])*0.05)
        else:
            self.lineEdit_CellCAP.setEnabled(True)
            self.lineEdit_CellTemp.setEnabled(True)
            self.comboBox_CellType.setEnabled(True)
            Data_RefreshTimer.stop()
            self.thread.terminate()
            self.pushButton_StartSystem.setText('启动')

    def CAN_DataReflash(self):
        global Cell_Dict

        self.lineEdit_CellVOL_NOW.setText(str(Cell_Dict['电压']))
        self.lineEdit_CellCurrent_NOW.setText(str(Cell_Dict['电流']))
        self.lineEdit_CellCAP_NOW.setText(str(Cell_Dict['剩余容量']))

    def Data_Reflash(self):
        i = 0


    def retranslateUi(self, Cell_Voltage_Simulate_Tool):
        global Cell_Dict
        _translate = QtCore.QCoreApplication.translate
        Cell_Voltage_Simulate_Tool.setWindowTitle(
            _translate("Cell_Voltage_Simulate_Tool", "Cell_Voltage_Simulate_Tool"))
        self.pushButton_OpenCAN.setText(_translate("Cell_Voltage_Simulate_Tool", "打开CAN通讯"))
        self.comboBox_CANType.setItemText(0, _translate("Cell_Voltage_Simulate_Tool", "USB-CAN-II"))
        self.pushButton_StartSystem.setText(_translate("Cell_Voltage_Simulate_Tool", "启动"))
        self.comboBox_CellType.setItemText(0, _translate("Cell_Voltage_Simulate_Tool", "铅酸6V"))
        self.comboBox_CellType.setItemText(1, _translate("Cell_Voltage_Simulate_Tool", "铅酸12V"))
        self.comboBox_CellType.setItemText(2, _translate("Cell_Voltage_Simulate_Tool", "磷酸铁锂"))
        self.comboBox_CellType.setItemText(3, _translate("Cell_Voltage_Simulate_Tool", "三元锂"))
        self.label_CellType.setText(_translate("Cell_Voltage_Simulate_Tool", "电池类型"))
        self.label_CellVoltage.setText(_translate("Cell_Voltage_Simulate_Tool", "电池电压"))
        self.label_CellTemp.setText(_translate("Cell_Voltage_Simulate_Tool", "电池温度"))
        self.label_CellCurrent.setText(_translate("Cell_Voltage_Simulate_Tool", "电池电流"))
        self.label_CellCAP.setText(_translate("Cell_Voltage_Simulate_Tool", "电池容量"))
        self.pushButton_CurSet.setText(_translate("Cell_Voltage_Simulate_Tool", "设置"))
        self.pushButton_VolSet.setText(_translate("Cell_Voltage_Simulate_Tool", "设置"))
        self.checkBox_AutoMode.setText(_translate("Cell_Voltage_Simulate_Tool", "自动充放电循环"))
        self.label_CellVOL_NOW.setText(_translate("Cell_Voltage_Simulate_Tool", "当前电压"))
        self.label_CellCurrent_NOW.setText(_translate("Cell_Voltage_Simulate_Tool", "当前电流"))
        self.label_CellCAP_NOW.setText(_translate("Cell_Voltage_Simulate_Tool", "剩余容量"))
        self.lineEdit_CellTemp.setText(str(Cell_Dict['温度']))
        self.lineEdit_CellVoltage.setText(str(Cell_Dict['电压']))
        self.lineEdit_CellCurrent.setText(str(Cell_Dict['电流']))
        self.lineEdit_CellCAP.setText(str(Cell_Dict['容量']))

class Main(QMainWindow, Ui_Cell_Voltage_Simulate_Tool):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)

if __name__ == "__main__":
    COM_Status = 0
    app = QApplication(sys.argv)
    MainWindows = Main()

    MainWindows.show()

    sys.exit(app.exec_())