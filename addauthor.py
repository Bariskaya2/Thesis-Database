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


class AddAuthor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Author")
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
        self.img = QPixmap('icons/addmember.png')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Author")
        self.titleText.setAlignment(Qt.AlignCenter)
        ############widgets of bottom layout############
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter name")
        self.addressEntry=QLineEdit()
        self.addressEntry.setPlaceholderText("Enter address")
        self.genderCombo=QComboBox()
        self.genderCombo.addItem("Male")
        self.genderCombo.addItem("Female")
        self.addBtn=QPushButton("Add")
        self.addBtn.clicked.connect(self.addAuthor)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Add")
        self.middleGroupBox = QGroupBox()
        #############add widgets############
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topGroupBox.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Adress: "), self.addressEntry)
        self.bottomLayout.addRow(QLabel("Gender: "), self.genderCombo)
        self.bottomLayout.addRow(QLabel(""), self.addBtn)
        self.middleGroupBox.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topGroupBox)
        self.mainLayout.addWidget(self.middleGroupBox)

        self.setLayout(self.mainLayout)

    def addAuthor(self):
        name=self.nameEntry.text()
        address=self.addressEntry.text()
        gender=self.genderCombo.currentText()
        if (name and address and gender != ""):
            try:
                query = "INSERT INTO Author (Name,Address,Gender) VALUES (?,?,?)"
                cur.execute(query, (name, address,gender))
                con.commit()
                QMessageBox.information(self, "Info", "Author has been added")
                self.nameEntry.setText("")
                self.addressEntry.setText("")

            except:
                QMessageBox.information(self, "Info", "Author has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields con not be empty!!!")

