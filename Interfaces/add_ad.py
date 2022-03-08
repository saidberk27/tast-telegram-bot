from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QListWidgetItem


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(784, 599)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(784, 599))
        MainWindow.setMaximumSize(QtCore.QSize(784, 599))
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(784, 599))
        self.centralwidget.setMaximumSize(QtCore.QSize(784, 599))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 781, 581))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.textEdit.setStyleSheet("border:3px solid rgb(34, 158, 217);")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.adNameLineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.adNameLineEdit.setFont(font)
        self.adNameLineEdit.setStyleSheet("border:3px solid rgb(34, 158, 217);\n"
"color:rgb(34, 158, 217)")
        self.adNameLineEdit.setText("")
        self.adNameLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.adNameLineEdit.setObjectName("adNameLineEdit")
        self.verticalLayout.addWidget(self.adNameLineEdit)
        self.addMediaButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.addMediaButton.setFont(font)
        self.addMediaButton.setStyleSheet("QPushButton {\n"
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
        self.addMediaButton.setObjectName("addMediaButton")
        self.verticalLayout.addWidget(self.addMediaButton)
        self.Saveaad_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Saveaad_button.setFont(font)
        self.Saveaad_button.setStyleSheet("QPushButton {\n"
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
        self.Saveaad_button.setObjectName("Saveaad_button")
        self.verticalLayout.addWidget(self.Saveaad_button)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, 0, 0, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:  rgb(34, 158, 217);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("border:3px solid rgb(34, 158, 217);")
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setItemAlignment(QtCore.Qt.AlignCenter)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.Saveaad_button.clicked.connect(self.saveAd)
        self.addMediaButton.clicked.connect(self.browseFiles)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ADD ADVERTISEMENT"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "YOUR AD TEXT..."))
        self.adNameLineEdit.setPlaceholderText(_translate("MainWindow", "PLEASE ENTER YOUR AD NAME"))
        self.addMediaButton.setText(_translate("MainWindow", "Add Media"))
        self.Saveaad_button.setText(_translate("MainWindow", "Save Ad"))
        self.label.setText(_translate("MainWindow", "MY ADS"))

    def browseFiles(self):
        self.fname = QFileDialog.getOpenFileName(None, 'Open file', filter='Images (*.png, *.xmp *.jpg)')

    def saveAd(self):
        adName = self.adNameLineEdit.text()
        adCsvFile = open("ads/{}.csv".format(adName), "w")

        textAd = self.textEdit.toPlainText()
        textMedia = self.fname[0]
        adCsvFile.write(textAd + "," + textMedia + "\n")

        adCsvFile.close()

        self.fillListWidget()

    def fillListWidget(self):
        self.listWidget.clear()  # Ust uste binmesin diye temizliyoruz.
        adCsvFiles = open("Advertisement Information.csv", "r")
        adCsvFilesList = adCsvFiles.readlines()
        for ad in adCsvFileList:
            print(ad)
            listWidgetItem = QListWidgetItem(ad)
            self.listWidget.addItem(listWidgetItem)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
