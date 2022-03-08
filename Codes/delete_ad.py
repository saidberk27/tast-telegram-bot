from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(513, 606)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(513, 606))
        MainWindow.setMaximumSize(QtCore.QSize(513, 606))
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 511, 601))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setStyleSheet("border:3px solid rgb(34, 158, 217);")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.listAdsButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.listAdsButton.setFont(font)
        self.listAdsButton.setStyleSheet("QPushButton {\n"
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
        self.listAdsButton.setObjectName("listAdsButton")
        self.verticalLayout.addWidget(self.listAdsButton)
        self.deleteAdButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteAdButton.sizePolicy().hasHeightForWidth())
        self.deleteAdButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.deleteAdButton.setFont(font)
        self.deleteAdButton.setStyleSheet("QPushButton {\n"
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
        self.deleteAdButton.setObjectName("deleteAdButton")
        self.verticalLayout.addWidget(self.deleteAdButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.listAdsButton.clicked.connect(self.listAds)
        self.deleteAdButton.clicked.connect(self.deleteSelectedAd)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DELETE AD"))
        self.listAdsButton.setText(_translate("MainWindow", "LIST ALL ADS"))
        self.deleteAdButton.setText(_translate("MainWindow", "DELETE SELECTED AD"))

    def listAds(self):
        self.listWidget.clear()  # Ust uste binmesin diye temizliyoruz.
        adCsvFiles = os.listdir("ads")

        for ad in adCsvFiles:
            listWidgetItem = QListWidgetItem(ad)
            self.listWidget.addItem(listWidgetItem)


    def deleteSelectedAd(self):
            currentRow = self.listWidget.currentRow()
            self.listWidget.takeItem(currentRow)
            adCsvFiles = os.listdir("ads")

            os.system("cd ads")
            os.system("del ads\{}".format(adCsvFiles[currentRow]))
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
