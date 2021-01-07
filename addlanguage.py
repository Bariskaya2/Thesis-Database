import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui  import *
from PyQt5.QtCore import Qt
import pypyodbc
from PIL import Image

con = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-63U3JN8\SQLEXPRESS2019;'
    'Database=TermProject;'
    'Trusted_Connection=True;'
)
cur = con.cursor()


class AddLanguage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Language")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        #############widgets of top layout###########
        self.addMemberImg = QLabel()
        self.img = QPixmap('icons/addlanguage.png')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Language")
        self.titleText.setAlignment(Qt.AlignCenter)
        ############widgets of bottom layout############
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name")
        self.addBtn=QPushButton("Add")
        self.addBtn.clicked.connect(self.addLanguage)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Add")
        self.middleGroupBox = QGroupBox()
        #############add widgets############
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.topLayout.addRow(QLabel(""), self.addBtn)
        self.topGroupBox.setLayout(self.topLayout)
        self.middleGroupBox.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topGroupBox)
        self.mainLayout.addWidget(self.middleGroupBox)

        self.setLayout(self.mainLayout)

    def addLanguage(self):
        name=self.nameEntry.text()

        if (name != ""):
            try:
                query = "INSERT INTO Language (Name) VALUES (?)"
                cur.execute(query, (name,))
                con.commit()
                QMessageBox.information(self, "Info", "Language has been added")
                self.nameEntry.setText("")


            except:
                QMessageBox.information(self, "Info", "Language has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields con not be empty!!!")

