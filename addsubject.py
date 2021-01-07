import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui  import *
from PyQt5.QtCore import Qt
import pypyodbc


con = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-63U3JN8\SQLEXPRESS2019;'
    'Database=TermProject;'
    'Trusted_Connection=True;'
)
cur = con.cursor()


class AddSubject(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Subject")
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
        self.img = QPixmap('icons/list.png')
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Subject")
        self.titleText.setAlignment(Qt.AlignCenter)
        ############widgets of bottom layout############
        self.subjectEntry=QLineEdit()
        self.addBtn=QPushButton("Add")
        self.addBtn.clicked.connect(self.addSubject)

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
        self.bottomLayout.addRow(QLabel("Name: "), self.subjectEntry)
        self.bottomLayout.addRow(QLabel(""), self.addBtn)
        self.middleGroupBox.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topGroupBox)
        self.mainLayout.addWidget(self.middleGroupBox)

        self.setLayout(self.mainLayout)

    def addSubject(self):
        subject=self.subjectEntry.text()

        if (subject != ""):
            try:
                query = "INSERT INTO Subject (Name) VALUES (?)"
                cur.execute(query, (subject,))
                con.commit()
                QMessageBox.information(self, "Info", "Subject has been added")
                self.subjectEntry.setText("")

            except:
                QMessageBox.information(self, "Info", "Subject has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields con not be empty!!!")

