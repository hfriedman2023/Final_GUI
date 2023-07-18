import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QVBoxLayout
from PyQt5.QtWidgets import (
    QWidget,
    QSlider,
    QLineEdit,
    QScrollArea,
    QHBoxLayout,
    QComboBox,
    QFrame,
)
from PyQt5.QtCore import Qt, QSize
from Ui_MainApp1 import Ui_MainWindow  # Import the generated UI code
from PyQt5.QtCore import QObject

# imports from the tkinter GUI
# import serial
# import bluetooth
import re
import time

# import os.path

# This class sets the X, Y, and Z position as shown in the GUI (not the ones that have the 'Moving' starting title)
# for the Manual


class MainWindow(QMainWindow):
    global deviceConnected
    deviceConnected = True

    def __init__(self):
        super(MainWindow, self).__init__()
        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set the initial page to the Home Page showing the UF ECE logo
        self.ui.stackedWidget.setCurrentIndex(0)
        # Set some main window's properties
        self.setFixedSize(1300, 550)
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint
        )
        # Bluetooth module parameters
        self.name = "HC-05"  # Device Name
        self.address = "98:D3:41:FD:78:64"  # Device Address
        self.port = 1  # RFCOMM port
        self.passkey = "1234"  # Passkey of the device
        # Position parameters
        self.numPulses = [400, 400, 400]
        self.maxRange = [500, 500, 200]
        self.sampleLocation = [0, 0, 0]
        # RPM parameters
        self.rpm = range(100, 1000, 1)

        # Connect button signals to slots:
        # When sidemenu button is clicked, the corresponding page is shown
        self.ui.connectDevice_btn.clicked.connect(self.connectDevice)
        self.ui.manuaOPE_btn.clicked.connect(self.showManualOPEPage)
        self.ui.setParameters_btn.clicked.connect(self.showSetParametersPage)
        self.ui.editProgram_btn.clicked.connect(self.showEditProgramPage)
        self.ui.about_btn.clicked.connect(self.showAboutDialog)

        #########################################################
        # Manual Operation Page #
        #########################################################

        # if deviceConnected is true and index for manual is selected enable the entry boxes, othewise disable the entry boxes.
        self.manual_init()
        if deviceConnected == False:
            self.ui.ConnectDevice_Label.setText("Device Not Connected")
            self.ui.ConnectDevice_Label.setStyleSheet("color: red")
            self.ui.ConnectDevice_Label.setFont(
                QtGui.QFont("Times", 10, QtGui.QFont.Bold)
            )

            self.ui.moveX_lineEdit.setEnabled(False)
            self.ui.moveY_lineEdit.setEnabled(False)
            self.ui.moveZ_lineEdit.setEnabled(False)
            self.ui.Xhome_btn.setEnabled(False)
            self.ui.Yhome_btn.setEnabled(False)
            self.ui.Zhome_btn.setEnabled(False)
            self.ui.STOPALL_MNLOPE_BTN.setEnabled(False)
            self.ui.HP1_Temp_lineEdit.setEnabled(False)
            self.ui.HP2_Temp_lineEdit.setEnabled(False)
            self.ui.HP1_StirSpeed_lineEdit.setEnabled(False)
            self.ui.HP2_StirSpeed_lineEdit.setEnabled(False)
            self.ui.HP1_Ramp_lineEdit.setEnabled(False)
            self.ui.HP2_Ramp_lineEdit.setEnabled(False)
            self.ui.manual_Voltage_lineEdit.setEnabled(False)
            self.ui.manual_Current_lineEdit.setEnabled(False)
            self.ui.SM_OUTPUT_btn.setEnabled(False)

        #########################################################
        # Set Parameter Page #
        #########################################################

        if deviceConnected == False:
            self.ui.ConnectDevice_Label.setText("Device Not Connected")
            self.ui.ConnectDevice_Label.setStyleSheet("color: red")
            self.ui.ConnectDevice_Label.setFont(
                QtGui.QFont("Times", 10, QtGui.QFont.Bold)
            )

            self.ui.POS1_X_lineEdit.setEnabled(False)
            self.ui.POS1_Y_lineEdit.setEnabled(False)
            self.ui.POS2_X_lineEdit.setEnabled(False)
            self.ui.POS2_Y_lineEdit.setEnabled(False)
            self.ui.POS3_X_lineEdit.setEnabled(False)
            self.ui.POS3_Y_lineEdit.setEnabled(False)
            self.ui.POS4_X_lineEdit.setEnabled(False)
            self.ui.POS4_Y_lineEdit.setEnabled(False)
            self.ui.POS5_X_lineEdit.setEnabled(False)
            self.ui.POS5_Y_lineEdit.setEnabled(False)
            self.ui.POS6_X_lineEdit.setEnabled(False)
            self.ui.POS6_Y_lineEdit.setEnabled(False)
            self.ui.PULSEnum_X_lineEdit.setEnabled(False)
            self.ui.PULSEnum_Y_lineEdit.setEnabled(False)
            self.ui.PULSEnum_Z_lineEdit.setEnabled(False)
            self.ui.MAXdist_X_lineEdit.setEnabled(False)
            self.ui.MAXdist_Y_lineEdit.setEnabled(False)
            self.ui.MAXdist_Z_lineEdit.setEnabled(False)
            self.ui.changeSpeed_lineEdit.setEnabled(False)

            self.ui.RESETparam_btn.setEnabled(False)
            self.ui.SETparam_btn.setEnabled(False)

        self.ui.RESETparam_btn.clicked.connect(self.setReset)
        self.ui.SETparam_btn.clicked.connect(self.setParaclick)

        #########################################################
        # Edit Program Page #
        #########################################################

        if deviceConnected == False:
            self.ui.ConnectDevice_Label.setText("Device Not Connected")
            self.ui.ConnectDevice_Label.setStyleSheet("color: red")
            self.ui.ConnectDevice_Label.setFont(
                QtGui.QFont("Times", 10, QtGui.QFont.Bold)
            )

            # self.ui.INSERTROW_btn.setEnabled(False)
            # self.ui.DELETEROW_btn.setEnabled(False)
            # self.ui.ROW_FRAME.setEnabled(False)
            self.ui.LOAD_PROGRAM_BTN.setEnabled(False)
            self.ui.RUN_PROGRAM_BTN.setEnabled(False)
            self.ui.LOAD_TXT_BTN.setEnabled(False)

        # self.frame_data = [] #stores the data of the frames
        self.line_edits = []  # stores the QLineEdit instances here
        self.combo_boxes = []  # stores the QComboBox instances here

        self.combo_boxes = []  # stores the QComboBox instances here
        self.addROW()
        self.ui.LOAD_PROGRAM_BTN.clicked.connect(self.getFrameData)
        # self.combo_box1.activated.connect(self.getFrameData)
        # self.ui.INSERTROW_btn.clicked.connect(self.addROW)
        # self.combo_box1.activated.connect(self.getCOMBOBOX1)

        #################### About Dialog ####################
        # Shows the About Dialog when the About button is clicked
        self.about_window = AboutDialog(self)

    # Define slots

    def showManualOPEPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showSetParametersPage(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def showEditProgramPage(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def showAboutDialog(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    #########################################################################################
    # Connect Device Button Method and Misc Methods #
    #########################################################################################
    # deviceConnected = False --> Placed it at the beginning of MainWindow class instead of here

    def connectDevice(self):
        global s
        global deviceConnected

        # Connect the HC-05 bluetooth module with Hotplates and Keithley Source Meter
        try:
            print("here")
            # Connect with the source meter
            # keithley = serial.Serial('COM4', 57600, timeout=1)
            s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            s.connect((self.address, self.port))

            self.ui.ConnectDevice_Label.setText("Device Connected")
            self.ui.ConnectDevice_Label.setStyleSheet("color: green")

            deviceConnected = True

            # Enable or disable UI elements as needed
            # xDataEn.setEnabled(True)
            # yDataEn.setEnabled(True)
            # zDataEn.setEnabled(True)
            self.ui.moveX_lineEdit.setEnabled(True)
            self.ui.moveY_lineEdit.setEnabled(True)
            self.ui.moveZ_lineEdit.setEnabled(True)
            # xHome.setEnabled(True)
            # yHome.setEnabled(True)
            # zHome.setEnabled(True)
            self.ui.Xhome_btn.setEnabled(True)
            self.ui.Yhome_btn.setEnabled(True)
            self.ui.Zhome_btn.setEnabled(True)
            # self.ui.stopAllButton.setEnabled(True)
            self.ui.STOPALL_MNLOPE_BTN.setEnabled(True)
            # tempEn1.setEnabled(True)
            # tempEn2.setEnabled(True)
            self.ui.HP1_Temp_lineEdit.setEnabled(True)
            self.ui.HP2_Temp_lineEdit.setEnabled(True)
            # rpmEn1.setEnabled(True)
            # rpmEn2.setEnabled(True)
            self.ui.HP1_StirSpeed_lineEdit.setEnabled(True)
            self.ui.HP2_StirSpeed_lineEdit.setEnabled(True)
            # rampEn1.setEnabled(True)
            # rampEn2.setEnabled(True)
            self.ui.HP1_Ramp_lineEdit.setEnabled(True)
            self.ui.HP2_Ramp_lineEdit.setEnabled(True)
            # LOAD_BTN.setEnabled(True)
            # RUN_BTN.setEnabled(True)
            self.ui.LOAD_PROGRAM_BTN.setEnabled(True)
            self.ui.RUN_PROGRAM_BTN.setEnabled(True)

            self.ui.moveX_lineEdit.setEnabled(True)
            self.ui.moveY_lineEdit.setEnabled(True)
            self.ui.moveZ_lineEdit.setEnabled(True)
            self.ui.Xhome_btn.setEnabled(True)
            self.ui.Yhome_btn.setEnabled(True)
            self.ui.Zhome_btn.setEnabled(True)
            self.ui.STOPALL_MNLOPE_BTN.setEnabled(True)
            self.ui.HP1_Temp_lineEdit.setEnabled(True)
            self.ui.HP2_Temp_lineEdit.setEnabled(True)
            self.ui.HP1_StirSpeed_lineEdit.setEnabled(True)
            self.ui.HP2_StirSpeed_lineEdit.setEnabled(True)
            self.ui.HP1_Ramp_lineEdit.setEnabled(True)
            self.ui.HP2_Ramp_lineEdit.setEnabled(True)
            self.ui.manual_Voltage_lineEdit.setEnabled(True)
            self.ui.manual_Current_lineEdit.setEnabled(True)
            self.ui.SM_OUTPUT_btn.setEnabled(True)
            self.ui.SM_OUTPUT_btn.clicked.connect(self.toggleButton)

            self.ui.POS1_X_lineEdit.setEnabled(True)
            self.ui.POS1_Y_lineEdit.setEnabled(True)
            self.ui.POS2_X_lineEdit.setEnabled(True)
            self.ui.POS2_Y_lineEdit.setEnabled(True)
            self.ui.POS3_X_lineEdit.setEnabled(True)
            self.ui.POS3_Y_lineEdit.setEnabled(True)
            self.ui.POS4_X_lineEdit.setEnabled(True)
            self.ui.POS4_Y_lineEdit.setEnabled(True)
            self.ui.POS5_X_lineEdit.setEnabled(True)
            self.ui.POS5_Y_lineEdit.setEnabled(True)
            self.ui.POS6_X_lineEdit.setEnabled(True)
            self.ui.POS6_Y_lineEdit.setEnabled(True)

            self.ui.PULSEnum_X_lineEdit.setEnabled(True)
            self.ui.PULSEnum_Y_lineEdit.setEnabled(True)
            self.ui.PULSEnum_Z_lineEdit.setEnabled(True)
            self.ui.MAXdist_X_lineEdit.setEnabled(True)
            self.ui.MAXdist_Y_lineEdit.setEnabled(True)
            self.ui.MAXdist_Z_lineEdit.setEnabled(True)
            self.ui.changeSpeed_lineEdit.setEnabled(True)

            self.ui.RESETparam_btn.setEnabled(True)
            self.ui.SETparam_btn.setEnabled(True)

            # keithley.write("*IDN?\n".encode())  # Turn on the Keithley source meter
            # Turn on the Keithley source meter
            self.keithley.write("*IDN?\n".encode())

            self.loadState()

            # response=keithley.readline().decode().strip()
            # if len(response) != 0:
            # currentEn.config(state="normal")
            # voltageEn.config(state="normal")
            # sourceOutButton.config(state="normal")
            # else:
            # currentEn.config(state="disable")
            # voltageEn.config(state="disable")
            # sourceOutButton.config(state="disable")

        except bluetooth.btcommon.BluetoothError as err:
            print("Bluetooth Error: ", err)
            pass

    def int_validate(self, value):
        if value.isdigit():
            return True
        else:
            return False

    def check_number(self, number):
        # Define the regex pattern
        pattern = r"^\d+\.\d{1}$"
        if re.match(pattern, number) or number.isdigit():
            return True
        else:
            return False

    #########################################################################################
    # Manual Operation Page Methods #
    #########################################################################################

    def manual_init(self):
        # When the home button is clicked, the corresponding axis is homed
        self.ui.moveX_lineEdit.returnPressed.connect(self.getX)
        self.ui.Xhome_btn.clicked.connect(lambda: self.Home("x"))

        self.ui.moveY_lineEdit.returnPressed.connect(self.getY)
        self.ui.Yhome_btn.clicked.connect(lambda: self.Home("y"))

        self.ui.moveZ_lineEdit.returnPressed.connect(self.getZ)
        self.ui.Zhome_btn.clicked.connect(lambda: self.Home("z"))

        self.ui.STOPALL_MNLOPE_BTN.clicked.connect(self.stopAll)

        # Manual OPE - Hot Plate 1 Parameters
        self.ui.HP1_Temp_lineEdit.returnPressed.connect(self.set_Temp1)
        self.ui.HP1_StirSpeed_lineEdit.returnPressed.connect(self.set_rpm1)
        self.ui.HP1_Ramp_lineEdit.returnPressed.connect(self.set_ramp1)

        # Manual OPE - Hot Plate 2 Parameters
        self.ui.HP2_Temp_lineEdit.returnPressed.connect(self.set_Temp2)
        self.ui.HP2_StirSpeed_lineEdit.returnPressed.connect(self.set_rpm2)
        self.ui.HP2_Ramp_lineEdit.returnPressed.connect(self.set_ramp2)

        # Manual OPE - Source Meter Parameters
        self.ui.manual_Voltage_lineEdit.returnPressed.connect(self.set_voltage)
        self.ui.manual_Current_lineEdit.returnPressed.connect(self.set_current)

    def getX(self):
        print("sfsf")
        # xRange=maxRange[0]
        # xRange=range(-xRange,xRange,1)
        # value = int(xDataEn.get())
        xRange = self.maxRange[0]
        xRange = range(-xRange, xRange, 1)
        value = int(self.ui.moveX_lineEdit.text())

        if value in xRange:
            data = "xData" + str(value)
            data = bytes(data, "utf-8")
            s.send(data)
            value = ""

            while True:
                data = s.recv(1)
                if len(data) > 0:
                    if data.decode("utf-8") == "\r":
                        print(value)
                        break
                    value = value + data.decode("utf-8")

            # sampleLocation[0]=int(value)
            # xValue.set(str(value))
            self.sampleLocation[0] = int(value)
            self.ui.XPOS_lineEdit.setText(str(value))

    def getY(self):
        # yRange=maxRange[1]
        # yRange=range(-yRange,yRange,1)
        # value = int(yDataEn.get())
        yRange = self.maxRange[1]
        yRange = range(-yRange, yRange, 1)
        value = int(self.ui.moveY_lineEdit.text())

        if value in yRange:
            data = "yData" + str(value)
            data = bytes(data, "utf-8")
            s.send(data)
            value = ""

            while True:
                data = s.recv(1)

                if len(data) > 0:
                    if data.decode("utf-8") == "\r":
                        print(value)
                        break
                    value = value + data.decode("utf-8")

            self.sampleLocation[1] = int(value)
            self.ui.YPOS_lineEdit.setText(str(value))

    def getZ(self):
        # zRange=maxRange[2]
        # zRange=range(-zRange,zRange,1)
        # value = int(zDataEn.get())
        zRange = self.maxRange[2]
        zRange = range(-zRange, zRange, 1)
        value = int(self.ui.moveZ_lineEdit.text())

        print(value)
        if value in zRange:
            data = "zData" + str(value)
            data = bytes(data, "utf-8")
            s.send(data)
            value = ""

            while True:
                data = s.recv(1)

                if len(data) > 0:
                    if data.decode("utf-8") == "\r":
                        print(value)
                        break
                    value = value + data.decode("utf-8")

            # sampleLocation[2]=int(value)
            # zValue.set(str(value))
            self.sampleLocation[2] = int(value)
            self.ui.ZPOS_lineEdit.setText(str(value))

    def Home(self, axis):
        # Send data through the serial port
        data = axis + "0\r\n"
        data = bytes(data, "utf-8")
        # ser.write(data)

    def stopAll(self):
        data = b"stp\r\n"
        s.send(data)

    def toggleButton(self):
        if self.ui.SM_OUTPUT_btn.text() == "ON":
            self.ui.SM_OUTPUT_btn.setText("OFF")
        else:
            self.ui.SM_OUTPUT_btn.setText("ON")

    # def set_output_ON_OFF(self):
    #     global keithley
    #     if sourceOutButton.cget('text')=="ON" :
    #         keithley.write(":OUTP:STAT ON\n".encode())
    #         sourceOutButton.config(text="OFF")
    #     else:
    #         keithley.write(":OUTP:STAT OFF\n".encode())
    #         sourceOutButton.config(text="ON")

    ############## MNL HP1 ##############

    def set_rpm1(self):
        data = self.ui.HP1_StirSpeed_lineEdit.text()
        if data.isdigit():
            data = "1rpm" + data + "\r\n"
            data = bytes(data, "utf-8")
            print(data)
            s.send(data)

    def set_ramp1(self):
        data = self.ui.HP1_Ramp_lineEdit.text()
        if data.isdigit():
            data = "1ramp" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)
            # ser.send(data)

    def set_Temp1(self):
        # data = tempEn1.get()
        data = self.ui.HP1_Temp_lineEdit.text()
        if data.isdigit():
            data = "1Te" + data + "\r\n"
            print(data)
            data = bytes(data, "utf-8")
            s.send(data)

    ############## MNL HP2 ##############
    def set_rpm2(self):
        data = self.ui.HP2_StirSpeed_lineEdit.text()
        if data.isdigit():
            if data in self.rpm:
                data = "2rpm" + data + "\r\n"
                data = bytes(data, "utf-8")
                s.send(data)
                print(data)

    def set_ramp2(self):
        data = self.ui.HP2_Ramp_lineEdit.text()
        if data.isdigit():
            data = "2ramp" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)
            print(data)

    def set_Temp2(self):
        data = self.ui.HP2_Temp_lineEdit.text()
        if data.isdigit():
            data = "2Te" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)
            print(data)
            # ser.write(data)

    ############## MNL Source Meter ##############
    def set_current(self):
        global keithley
        # data = currentEn.get()
        data = self.ui.manual_Current_lineEdit.text()

        # if check_number(data):
        if self.check_number(data):
            value = data
            data = ":SOUR:CURR:LEV " + str(value) + "\n"
            keithley.write(data.encode())

    def set_voltage(self):
        global keithley
        data = self.ui.manual_Voltage_lineEdit.text()
        # if check_number(data):
        if self.check_number(data):
            value = data
            data = ":SOUR:VOLT:LEV " + str(value) + "\n"
            keithley.write(data.encode())

    #########################################################################################
    # Set Parameters Page Methods #
    #########################################################################################

    def set_speed(self):
        data = self.ui.changeSpeed_lineEdit.text()
        print(data)
        if data.isdigit():
            data = "spe" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)
            # ser.write(data)

    def setMaxDist(self):
        # data = xMaxDistEn.get()
        data = self.ui.MAXdist_X_lineEdit.text()
        if data.isdigit():
            data = "xMax" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

        # data = yMaxDistEn.get()
        data = self.ui.MAXdist_Y_lineEdit.text()
        if data.isdigit():
            data = "yMax" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

        # data = zMaxDistEn.get()
        data = self.ui.MAXdist_Z_lineEdit.text()
        if data.isdigit():
            data = "zMax" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

    def setPulsNum(self):
        # data = xPulseNumberEn.get()
        data = self.ui.PULSEnum_X_lineEdit.text()
        if data.isdigit():
            data = "xPul" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

        # data = yPulseNumberEn.get()
        data = self.ui.PULSEnum_Y_lineEdit.text()
        if data.isdigit():
            data = "yPul" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

        # data = zPulseNumberEn.get()
        data = self.ui.PULSEnum_Z_lineEdit.text()
        if data.isdigit():
            data = "zPul" + data + "\r\n"
            data = bytes(data, "utf-8")
            s.send(data)

    def setParaclick(self):
        # maxRange[0]=int(xMaxDistEn.get())
        # maxRange[1]=int(yMaxDistEn.get())
        # maxRange[2]=int(zMaxDistEn.get())
        # numPulses[0]=int(xPulseNumberEn.get())
        # numPulses[1]=int(yPulseNumberEn.get())
        # numPulses[2]=int(zPulseNumberEn.get())
        self.maxRange[0] = int(self.ui.MAXdist_X_lineEdit.text())
        self.maxRange[2] = int(self.ui.MAXdist_Z_lineEdit.text())
        self.maxRange[1] = int(self.ui.MAXdist_Y_lineEdit.text())
        self.numPulses[0] = int(self.ui.PULSEnum_X_lineEdit.text())
        self.numPulses[1] = int(self.ui.PULSEnum_Y_lineEdit.text())
        self.numPulses[2] = int(self.ui.PULSEnum_Z_lineEdit.text())

        # data="xaxis,"+str(numPulses[0])+","+str(maxRange[0])+","+str(sampleLocation[0])+",\n"
        # f.write(data)
        data = (
            "xaxis,"
            + str(self.numPulses[0])
            + ","
            + str(self.maxRange[0])
            + ","
            + str(self.sampleLocation[0])
            + ",\n"
        )
        # s.write(data)
        print(data)

        data = (
            "yaxis,"
            + str(self.numPulses[1])
            + ","
            + str(self.maxRange[1])
            + ","
            + str(self.sampleLocation[1])
            + ",\n"
        )
        # s.write(data)
        print(data)

        data = (
            "zaxis,"
            + str(self.numPulses[2])
            + ","
            + str(self.maxRange[2])
            + ","
            + str(self.sampleLocation[2])
            + ",\n"
        )
        # s.write(data)
        print(data)

        # data="post1,"+xPosition1En.get()+","+yPosition1En.get()+",\n"
        # f.write(data)
        data = (
            "post1,"
            + self.ui.POS1_X_lineEdit.text()
            + ","
            + self.ui.POS1_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)

        data = (
            "post2,"
            + self.ui.POS2_X_lineEdit.text()
            + ","
            + self.ui.POS2_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)
        data = (
            "post3,"
            + self.ui.POS3_X_lineEdit.text()
            + ","
            + self.ui.POS3_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)
        data = (
            "post4,"
            + self.ui.POS4_X_lineEdit.text()
            + ","
            + self.ui.POS4_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)
        data = (
            "post5,"
            + self.ui.POS5_X_lineEdit.text()
            + ","
            + self.ui.POS5_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)
        data = (
            "post6,"
            + self.ui.POS6_X_lineEdit.text()
            + ","
            + self.ui.POS6_Y_lineEdit.text()
            + ",\n"
        )
        # s.write(data)
        print(data)
        data = "speed," + self.ui.changeSpeed_lineEdit.text() + ",0,0,\n"
        # s.write(data)
        print(data)

    def setReset(self):
        s.write("rts")

    #########################################################################################
    # Edit Program Page Methods #
    #########################################################################################

    def addROW(self):
        for num in range(400):
            # Create a new instance of the frame
            self.row_frame = QFrame()
            self.row_frame.setObjectName("ROW_FRAME")
            # create an index label for the row
            self.index_label = QLabel(self.row_frame)
            self.index_label.setObjectName("INDEX_LABEL")
            self.index_label.setText(str(num))
            self.index_label.setGeometry(0, 20, 30, 30)
            # Create the combo boxes and line edits
            self.combo_box1 = QComboBox(self.row_frame)
            self.combo_box2 = QComboBox(self.row_frame)
            self.line_edit1 = QLineEdit(self.row_frame)
            self.line_edit2 = QLineEdit(self.row_frame)
            self.line_edit3 = QLineEdit(self.row_frame)
            self.line_edit4 = QLineEdit(self.row_frame)
            self.combo_box1.setFixedSize(100, 30)
            self.combo_box2.setFixedSize(100, 30)
            self.line_edit1.setFixedSize(100, 30)
            self.line_edit2.setFixedSize(100, 30)
            self.line_edit3.setFixedSize(100, 30)
            self.line_edit4.setFixedSize(100, 30)

            self.combo_boxes.append((self.combo_box1, self.combo_box2))
            self.line_edits.append(
                (self.line_edit1, self.line_edit2, self.line_edit3, self.line_edit4)
            )

            # Add the combo boxes and line edits to the layout
            self.layout = QHBoxLayout(self.row_frame)
            self.layout.addWidget(self.combo_box1)
            self.layout.addWidget(self.combo_box2)
            self.layout.addWidget(self.line_edit1)
            self.layout.addWidget(self.line_edit2)
            self.layout.addWidget(self.line_edit3)
            self.layout.addWidget(self.line_edit4)
            # Add the dropdown options for combobox 1
            self.combo_box1.addItems(
                ["", "HP Set", "Sys OP", "SM", "position", "HP SysOp"]
            )
            # Set the layout of the row frame
            self.row_frame.setLayout(self.layout)
            # Get the scroll area and add the row frame to it
            self.scroll_area = self.ui.editPro_scrollArea
            self.scroll_area_widget = self.scroll_area.widget()
            # Create a layout for the scroll area widget if it doesn't have one
            if not self.scroll_area_widget.layout():
                self.scroll_area_widget.setLayout(QVBoxLayout())
            self.layout = self.scroll_area_widget.layout()
            self.layout.addWidget(self.row_frame)

    def getFrameData(self):
        combo_box1_value = ""
        combo_box2_value = ""
        line_edit1_value = ""
        line_edit2_value = ""
        line_edit3_value = ""
        line_edit4_value = ""
        self.frame = []
        for i in range(400):
            for j in range(1):
                combo_box1_value = (
                    self.combo_boxes[i][j].currentText() if self.combo_boxes else None
                )
                combo_box2_value = (
                    self.combo_boxes[i][j + 1].currentText()
                    if self.combo_boxes
                    else None
                )

            for k in range(1):
                line_edit1_value = (
                    self.line_edits[i][k].text() if self.line_edits else None
                )
                line_edit2_value = (
                    self.line_edits[i][k + 1].text() if self.line_edits else None
                )
                line_edit3_value = (
                    self.line_edits[i][k + 2].text() if self.line_edits else None
                )
                line_edit4_value = (
                    self.line_edits[i][k + 3].text() if self.line_edits else None
                )
            self.frame.append(
                (
                    combo_box1_value,
                    combo_box2_value,
                    line_edit1_value,
                    line_edit2_value,
                    line_edit3_value,
                    line_edit4_value,
                )
            )

        # Do something with the retrieved data
        for i in range(400):
            print(self.frame[i])
            # self.s.write(self.frame[i])

    # create a method that will generate different selection options for combo box 2
    def combo_box2_options(self):
        # Get the current text of combo box 1
        combo_box1_text = self.combo_box1.currentText()
        # Clear the current items in combo box 2
        self.combo_box2.clear()
        # Add the appropriate items to combo box 2
        if combo_box1_text == "HP Set":
            self.combo_box2.addItems(["HP1", "HP2"])
        elif combo_box1_text == "Sys OP":
            self.combo_box2.addItems(["Delay Time", "Stop All"])
        elif combo_box1_text == "SM":
            self.combo_box2.addItems(["DC Voltage", "DC Current"])
        elif combo_box1_text == "position":
            self.combo_box2.addItems(["pos1", "pos2", "pos3", "pos4", "pos5", "pos6", "pos7", "pos8", "pos9", "pos10"])
        elif combo_box1_text == "HP SysOp":
            self.combo_box2.addItems(["Match Temp", "Turn On/Off", "Stir On/Off", "HP1 Waiting", "HP2 Waiting"])
        

    def load_editpro(self):
        pass

    def deleteROW(self):
        pass

    def RUN_prog(self):
        pass

    def loadProg(self):
        global s
        row_count = 0
        with open("program.txt", "r") as file:
            for line in file:
                row_count += 1
        print(row_count)

        with open("program.txt") as f:
            for i in range(row_count):
                data = f.readline()
                print(data)
                if i > 0:
                    s.send(data)
                    time.sleep(0.1)

        # programlabel.config(text="Program Loaded",bg="green")
        self.ui.LOADPROGRAM_label.setText("Program Loaded")
        self.ui.LOADPROGRAM_label.setStyleSheet("background-color: green;")

    def runProg(self):
        s.send("runProg\r")
        # programlabel.config(text="Running Program",bg="green")
        self.ui.RUNPROGRAM_label.setText("Running Program")
        self.ui.RUNPROGRAM_label.setStyleSheet("background-color: green;")

    def read_serial(self):
        data = ""
        data = s.read().decode("utf-8")
        cmd = str(data)
        cmd = cmd.split(",")[0]

        if cmd == "curr":
            data = data.split(",")[1]

            if self.check_number(int(data)):
                data = ":SOUR:CURR:LEV " + data + "\n"
                self.keithley.write(data.encode())

            if cmd == "volt":
                data = data.split(",")[1]
                if self.check_number(int(data)):
                    data = ":SOUR:VOLT:LEV " + data + "\n"
                    keithley.write(data.encode())

            if cmd == "sourceON":
                keithley.write(":OUTP:STAT ON\n".encode())
                source = True

            if cmd == "sourceOFF":
                keithley.write(":OUTP:STAT ON\n".encode())

            if cmd == "Progcom":
                programlabel.config(text="Program Ended", bg="green")

        s.close()

    def loadState(self):
        global s
        row_count = 0
        with open("controllerVal.txt", "r") as file:
            for line in file:
                row_count += 1
            print(row_count)
        with open("controllerVal.txt") as f:
            for i in range(row_count):
                data = f.readline()
                if i > 0:
                    data = bytes(data, "utf-8")
                    print(data)
                    s.send(data)
                    time.sleep(0.1)

    # if deviceConnected:
    #     # window.after(100, read_serial)
    #     QTimer.singleShot(100, read_serial) #pyqt5 equivalent of window.after(100, read_serial)


#########################################################################################
# About Dialog Pop-up window #
#########################################################################################
class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle("About")
        self.resize(400, 300)
        layout = QVBoxLayout()
        label = QLabel("This is the About window.")
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    # Create an instance of the QApplication
    app = QApplication(sys.argv)
    window = MainWindow()  # Create an instance of the MainWindow class
    window.show()  # Show the window
    sys.exit(app.exec_())  # Start the event loop
