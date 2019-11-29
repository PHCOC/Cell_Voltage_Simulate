# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Cell_Voltage_Simulate_Tool.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Cell_Voltage_Simulate_Tool(object):
    def setupUi(self, Cell_Voltage_Simulate_Tool):
        Cell_Voltage_Simulate_Tool.setObjectName("Cell_Voltage_Simulate_Tool")
        Cell_Voltage_Simulate_Tool.resize(711, 432)
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
        self.label_CellVoltage.setGeometry(QtCore.QRect(430, 140, 61, 16))
        self.label_CellVoltage.setObjectName("label_CellVoltage")
        self.lineEdit_CellVoltage = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellVoltage.setGeometry(QtCore.QRect(500, 130, 111, 31))
        self.lineEdit_CellVoltage.setObjectName("lineEdit_CellVoltage")
        self.label_CellTemp = QtWidgets.QLabel(self.centralwidget)
        self.label_CellTemp.setGeometry(QtCore.QRect(10, 140, 61, 16))
        self.label_CellTemp.setObjectName("label_CellTemp")
        self.lineEdit_CellTemp = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellTemp.setGeometry(QtCore.QRect(80, 130, 111, 31))
        self.lineEdit_CellTemp.setObjectName("lineEdit_CellTemp")
        self.label_CellCurrent = QtWidgets.QLabel(self.centralwidget)
        self.label_CellCurrent.setGeometry(QtCore.QRect(430, 90, 61, 16))
        self.label_CellCurrent.setObjectName("label_CellCurrent")
        self.lineEdit_CellCurrent = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CellCurrent.setGeometry(QtCore.QRect(500, 80, 111, 31))
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
        self.pushButton_CurSet.setGeometry(QtCore.QRect(630, 80, 71, 31))
        self.pushButton_CurSet.setObjectName("pushButton_CurSet")
        self.pushButton_VolSet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_VolSet.setGeometry(QtCore.QRect(630, 130, 71, 31))
        self.pushButton_VolSet.setObjectName("pushButton_VolSet")
        self.Graph = QtWidgets.QTabWidget(self.centralwidget)
        self.Graph.setGeometry(QtCore.QRect(10, 200, 411, 192))
        self.Graph.setObjectName("Graph")
        self.Voltage = QtWidgets.QWidget()
        self.Voltage.setObjectName("Voltage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.Voltage)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.Graph.addTab(self.Voltage, "")
        self.Current = QtWidgets.QWidget()
        self.Current.setObjectName("Current")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Current)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Graph.addTab(self.Current, "")
        self.RemainCAP = QtWidgets.QWidget()
        self.RemainCAP.setObjectName("RemainCAP")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.RemainCAP)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Graph.addTab(self.RemainCAP, "")
        self.graphicsView_Cell = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_Cell.setGeometry(QtCore.QRect(460, 200, 241, 161))
        self.graphicsView_Cell.setObjectName("graphicsView_Cell")
        self.checkBox_AutoMode = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_AutoMode.setGeometry(QtCore.QRect(480, 20, 111, 21))
        self.checkBox_AutoMode.setObjectName("checkBox_AutoMode")
        self.checkBox_SaveData = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_SaveData.setGeometry(QtCore.QRect(620, 370, 81, 21))
        self.checkBox_SaveData.setObjectName("checkBox_SaveData")
        Cell_Voltage_Simulate_Tool.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Cell_Voltage_Simulate_Tool)
        self.statusbar.setObjectName("statusbar")
        Cell_Voltage_Simulate_Tool.setStatusBar(self.statusbar)

        self.retranslateUi(Cell_Voltage_Simulate_Tool)
        self.Graph.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Cell_Voltage_Simulate_Tool)

    def retranslateUi(self, Cell_Voltage_Simulate_Tool):
        _translate = QtCore.QCoreApplication.translate
        Cell_Voltage_Simulate_Tool.setWindowTitle(_translate("Cell_Voltage_Simulate_Tool", "Cell_Voltage_Simulate_Tool"))
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
        self.Graph.setTabText(self.Graph.indexOf(self.Voltage), _translate("Cell_Voltage_Simulate_Tool", "电压"))
        self.Graph.setTabText(self.Graph.indexOf(self.Current), _translate("Cell_Voltage_Simulate_Tool", "电流"))
        self.Graph.setTabText(self.Graph.indexOf(self.RemainCAP), _translate("Cell_Voltage_Simulate_Tool", "剩余容量"))
        self.checkBox_AutoMode.setText(_translate("Cell_Voltage_Simulate_Tool", "自动充放电循环"))
        self.checkBox_SaveData.setText(_translate("Cell_Voltage_Simulate_Tool", "保存数据"))