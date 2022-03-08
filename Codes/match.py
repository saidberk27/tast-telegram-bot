from PyQt5 import QtCore, QtGui, QtWidgets
import ast
from PyQt5.QtWidgets import QListWidgetItem, QAbstractItemView
import os
import removeBlanks

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(650, 513)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(650, 513))
        MainWindow.setMaximumSize(QtCore.QSize(650, 513))
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 651, 511))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TitleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setStyleSheet("color:rgb(34, 158, 217)")
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout.addWidget(self.TitleLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupsLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto Black")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.groupsLabel.setFont(font)
        self.groupsLabel.setStyleSheet("border:3px solid rgb(34, 158, 217);\n"
"color:rgb(34, 158, 217)")
        self.groupsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.groupsLabel.setObjectName("groupsLabel")
        self.verticalLayout_2.addWidget(self.groupsLabel)
        self.groups_listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groups_listWidget.setFont(font)
        self.groups_listWidget.setStyleSheet("border:3px solid rgb(34, 158, 217);\n"
"color:rgb(34, 158, 217)")
        self.groups_listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.groups_listWidget.setObjectName("groups_listWidget")
        self.verticalLayout_2.addWidget(self.groups_listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.adsLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.adsLabel.setFont(font)
        self.adsLabel.setStyleSheet("border:3px solid rgb(34, 158, 217);\n"
"color:rgb(34, 158, 217)")
        self.adsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.adsLabel.setObjectName("adsLabel")
        self.verticalLayout_4.addWidget(self.adsLabel)
        self.ads_listWidget = QtWidgets.QListWidget(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.ads_listWidget.setFont(font)
        self.ads_listWidget.setStyleSheet("border:3px solid rgb(34, 158, 217);\n"
"color:rgb(34, 158, 217)")
        self.ads_listWidget.setObjectName("ads_listWidget")
        self.verticalLayout_4.addWidget(self.ads_listWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.listButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.listButton.setFont(font)
        self.listButton.setStyleSheet("QPushButton {\n"
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
        self.listButton.setObjectName("listButton")
        self.verticalLayout.addWidget(self.listButton)
        self.matchButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.matchButton.setFont(font)
        self.matchButton.setStyleSheet("QPushButton {\n"
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
        self.matchButton.setObjectName("matchButton")
        self.verticalLayout.addWidget(self.matchButton)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.listButton.clicked.connect(self.listAll)
        self.matchButton.clicked.connect(self.match)

        self.ads_listWidget.setSelectionMode(QAbstractItemView.MultiSelection)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TitleLabel.setText(_translate("MainWindow", "SELECT ONE GROUP AND MATCH WITH ADS"))
        self.groupsLabel.setText(_translate("MainWindow", "GROUPS"))
        self.adsLabel.setText(_translate("MainWindow", "ADS"))
        self.listButton.setText(_translate("MainWindow", "LIST ALL"))
        self.matchButton.setText(_translate("MainWindow", "MATCH"))

    def listAll(self):
        self.groups_listWidget.clear()
        self.ads_listWidget.clear()  # Ust uste binmesin diye temizliyoruz.

        groupsFile = open("Group List.txt", "r")
        groupsList = groupsFile.readlines()


        for dataSet in groupsList:
            convertedDict = ast.literal_eval(dataSet)  # String to dict

            listWidgetItem = QListWidgetItem(convertedDict["Name"])
            self.groups_listWidget.addItem(listWidgetItem)
        groupsFile.close()
#------------------------GRUP LISTELEME-------------------------------#
#------------------------AD LISTELEME-------------------------------#

        adCsvFiles = os.listdir("ads")

        for ad in adCsvFiles:
            listWidgetItem = QListWidgetItem(ad)
            self.ads_listWidget.addItem(listWidgetItem)

    def match(self):
        groupsFile = open("Group List.txt", "r")
        groupsList = groupsFile.readlines()

        selectedGroup = self.groups_listWidget.selectedItems()[0].data(0)#0'in amacini ben de cozemedim, int gerkeiyodu girdim.

        selectedAds = self.ads_listWidget.selectedItems()
        selectedAdsData = []

        for pureAd in selectedAds:
            selectedAdsData.append(pureAd.data(0)) #datayi almak icin.

        index = 0
        for dataSet in groupsList:
            convertedDict = ast.literal_eval(dataSet)
            if(convertedDict["Name"] == selectedGroup): #Secilen grup, group_list.txt icindeki bir grupla eslesiyorsa
                selectedAdsString = ','.join(map(str, selectedAdsData)) #reklamlar listeisni stringe cevir
                convertedDict.update( {'ADS' : selectedAdsString} ) #reklamlari eslesen grup dict'ine ekle
                groupsList[index] = str(convertedDict) #grup listesinden secilen grubu index vasitasiyla bul, reklam eklenmis dict'i listeye ekle
            index = index + 1

        groupsFile = open("Group List.txt", "w")#clean islemi
        groupsFile.write("") #clean islemi
        groupsFile.close()#clean islemi

        groupsFileAppend = open("Group List.txt", "a")
        for updatedListElements in groupsList:
            groupsFileAppend.write(updatedListElements + "\n")
        groupsFileAppend.close()

        removeBlanks.remove_blanks()#Groups List.txt tekrar kullanilabilir olmasi icin bosluklarindan arindiriyoruz.


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
