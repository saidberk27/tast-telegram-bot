from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DeleteGroupWindow(object):
    def setupUi(self, DeleteGroupWindow, MainWindow):
        DeleteGroupWindow.setObjectName("Delete Group")
        DeleteGroupWindow.resize(746, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeleteGroupWindow.sizePolicy().hasHeightForWidth())
        DeleteGroupWindow.setSizePolicy(sizePolicy)
        DeleteGroupWindow.setMinimumSize(QtCore.QSize(746, 400))
        DeleteGroupWindow.setMaximumSize(QtCore.QSize(746, 400))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../Downloads/telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DeleteGroupWindow.setWindowIcon(icon)
        DeleteGroupWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(DeleteGroupWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(90, 80, 591, 231))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(20, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(250, 100))
        self.label.setMaximumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(34, 158, 217);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.groupName_lineedit = QtWidgets.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupName_lineedit.sizePolicy().hasHeightForWidth())
        self.groupName_lineedit.setSizePolicy(sizePolicy)
        self.groupName_lineedit.setMinimumSize(QtCore.QSize(200, 100))
        self.groupName_lineedit.setMaximumSize(QtCore.QSize(300, 100))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.groupName_lineedit.setFont(font)
        self.groupName_lineedit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.groupName_lineedit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.groupName_lineedit.setStyleSheet("\n"
"QLineEdit{\n"
"border: 2px solid rgb(34, 158, 217);\n"
"border-radius: 10px; \n"
"padding: 0 8px; \n"
"selection-background-color: darkgray; \n"
"font-size: 16px;\n"
"}\n"
"\n"
"")
        self.groupName_lineedit.setText("")
        self.groupName_lineedit.setAlignment(QtCore.Qt.AlignCenter)
        self.groupName_lineedit.setObjectName("groupName_lineedit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.groupName_lineedit)
        self.deleteGroupButton = QtWidgets.QPushButton(self.formLayoutWidget, clicked = lambda: self.deleteGroup(MainWindow))
        self.deleteGroupButton.setMaximumSize(QtCore.QSize(16777215, 300))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.deleteGroupButton.setFont(font)
        self.deleteGroupButton.setStyleSheet("QPushButton {\n"
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
        self.deleteGroupButton.setObjectName("deleteGroupButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.deleteGroupButton)
        self.bilgi_label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.bilgi_label.setFont(font)
        self.bilgi_label.setStyleSheet("color: rgb(0, 170, 255);")
        self.bilgi_label.setText("")
        self.bilgi_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bilgi_label.setObjectName("bilgi_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.bilgi_label)
        DeleteGroupWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DeleteGroupWindow)
        self.statusbar.setObjectName("statusbar")
        DeleteGroupWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DeleteGroupWindow)
        QtCore.QMetaObject.connectSlotsByName(DeleteGroupWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("Delete Group")
        self.label.setText(_translate("MainWindow", "GROUP NAME:  "))
        self.deleteGroupButton.setText(_translate("MainWindow", "DELETE GROUP"))

    def deleteGroup(self,m_window):
        import ast
        print("Deleted")
        groupsFile = open("Group List.txt", "r")
        groupsList = groupsFile.readlines()
        print(groupsList)
        groupsFile.close()

        for dataSet in groupsList:
            convertedDict = ast.literal_eval(dataSet)  # String to dict
            groupName = convertedDict["Name"]
            if(groupName == self.groupName_lineedit.text()):
                groupsList.remove(dataSet)

        groupsFileClear = open("Group List.txt", "w")
        groupsFileClear.write("")
        groupsFileClear.close()

        groupsFileAppend = open("Group List.txt", "a")
        for i in groupsList:
            groupsFileAppend.write(i)
        groupsFileAppend.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_DeleteGroupWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
