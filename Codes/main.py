import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

import add_group
import delete_group

import ast

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.groupsFile = open("Group List.txt", "r")
        self.groupsList = self.groupsFile.readlines()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 910)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(800, 910))
        MainWindow.setMaximumSize(QtCore.QSize(800, 910))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 811, 910))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.baslik = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.baslik.setFont(font)
        self.baslik.setAlignment(QtCore.Qt.AlignCenter)
        self.baslik.setObjectName("baslik")
        self.verticalLayout.addWidget(self.baslik)
        self.tablo = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tablo.setAutoFillBackground(False)
        self.tablo.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tablo.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tablo.setTabKeyNavigation(True)
        self.tablo.setAlternatingRowColors(True)
        self.tablo.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tablo.setTextElideMode(QtCore.Qt.ElideNone)
        self.tablo.setGridStyle(QtCore.Qt.SolidLine)
        self.tablo.setObjectName("tablo")
        self.tablo.setColumnCount(3)
        self.tablo.setRowCount(len(self.groupsList))
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tablo.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tablo.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tablo.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tablo.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tablo)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AddNewGroupButton = QtWidgets.QPushButton(self.verticalLayoutWidget, clicked = lambda:self.addNewGroupWindow(MainWindow))
        self.AddNewGroupButton.setMinimumSize(QtCore.QSize(400, 100))
        self.AddNewGroupButton.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.AddNewGroupButton.setFont(font)
        self.AddNewGroupButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.AddNewGroupButton.setObjectName("AddNewGroupButton")
        self.horizontalLayout.addWidget(self.AddNewGroupButton)
        self.DeleteGroupButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DeleteGroupButton.sizePolicy().hasHeightForWidth())
        self.DeleteGroupButton.setSizePolicy(sizePolicy)
        self.DeleteGroupButton.setMinimumSize(QtCore.QSize(400, 100))
        self.DeleteGroupButton.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.DeleteGroupButton.setFont(font)
        self.DeleteGroupButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.DeleteGroupButton.setObjectName("DeleteGroupButton")
        self.horizontalLayout.addWidget(self.DeleteGroupButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.MatchButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.MatchButton.setMinimumSize(QtCore.QSize(800, 100))
        self.MatchButton.setMaximumSize(QtCore.QSize(800, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.MatchButton.setFont(font)
        self.MatchButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.MatchButton.setObjectName("MatchButton")
        self.verticalLayout.addWidget(self.MatchButton)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AddAdvertisementButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.AddAdvertisementButton.setMinimumSize(QtCore.QSize(400, 100))
        self.AddAdvertisementButton.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.AddAdvertisementButton.setFont(font)
        self.AddAdvertisementButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.AddAdvertisementButton.setObjectName("AddAdvertisementButton")
        self.horizontalLayout_2.addWidget(self.AddAdvertisementButton)
        self.DeleteAdvertisementButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.DeleteAdvertisementButton.setMinimumSize(QtCore.QSize(400, 100))
        self.DeleteAdvertisementButton.setMaximumSize(QtCore.QSize(400, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.DeleteAdvertisementButton.setFont(font)
        self.DeleteAdvertisementButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.DeleteAdvertisementButton.setObjectName("DeleteAdvertisementButton")
        self.horizontalLayout_2.addWidget(self.DeleteAdvertisementButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.StartButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.StartButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.StartButton.setFont(font)
        self.StartButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.StartButton.setObjectName("StartButton")
        self.verticalLayout.addWidget(self.StartButton)
        self.StopButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.StopButton.setMinimumSize(QtCore.QSize(0, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.StopButton.setFont(font)
        self.StopButton.setStyleSheet("QPushButton {\n"
"  background-color: #229ED9;\n"
"  border: none;\n"
"  color: white;\n"
"  padding: 20px;\n"
"  text-align: center;\n"
"  text-decoration: none;\n"
"  display: inline-block;\n"
"  font-size: 16px;\n"
"  margin: 4px 2px;\n"
"  border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
" background-color: white;\n"
" color:#229ED9\n"
"}\n"
"")
        self.StopButton.setObjectName("StopButton")
        self.verticalLayout.addWidget(self.StopButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.tablo.setColumnWidth(0,400)
        self.tablo.setColumnWidth(1,200)
        self.tablo.setColumnWidth(2,180)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TAST TELEGRAM BOT"))
        self.baslik.setText(_translate("MainWindow", "MY TELEGRAM GROUPS"))

        item = self.tablo.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "TELEGRAM GROUPS"))
        item = self.tablo.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ADS"))
        item = self.tablo.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "STATUS"))
        self.AddNewGroupButton.setText(_translate("MainWindow", "Add a New Group"))
        self.DeleteGroupButton.setText(_translate("MainWindow", "Delete Group"))
        self.MatchButton.setText(_translate("MainWindow", "Match Groups-Advertisements"))
        self.AddAdvertisementButton.setText(_translate("MainWindow", "Add a New Advertisement"))
        self.DeleteAdvertisementButton.setText(_translate("MainWindow", "Delete Advertisement"))
        self.StartButton.setText(_translate("MainWindow", "START AD PUBLISHING"))
        self.StopButton.setText(_translate("MainWindow", "STOP AD PUBLISHING"))


    def addNewGroupWindow(self, MainWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = add_group.Ui_AddGroup()
        self.ui.setupUi(self.window, MainWindow)
        self.window.show()

    def deleteNewGroupWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = delete_group.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()


    def fillTable(self):
        groupsFile = open("Group List.txt", "r")
        groupsList = groupsFile.readlines()
        print("DFill Table")
        row = 0

        for dataSet in groupsList:
            convertedDict = ast.literal_eval(dataSet)  # String to dict
            self.tablo.setItem(row, 0, QtWidgets.QTableWidgetItem(convertedDict["Name"]))
            row = row + 1
        groupsFile.close()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.fillTable()
    MainWindow.show()
    sys.exit(app.exec_())
