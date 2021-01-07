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


class AddUniversity(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add/Update University")
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
        self.addImg = QLabel()
        self.img = QPixmap('icons/adduni.png')
        self.addImg.setPixmap(self.img)
        self.addImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("")
        self.titleText.setAlignment(Qt.AlignCenter)
        ############widgets of bottom layout############
        self.addUniEnrty= QLineEdit()
        self.addUniEnrty.setPlaceholderText("Enter name of University")
        self.addUniAddressEntry=QLineEdit()
        self.addUniAddressEntry.setPlaceholderText("Enter address of university")
        self.nameCombo = QComboBox()
        self.nameCombo.currentIndexChanged.connect(self.changeComboValue)
        self.newNameEntry= QLineEdit()
        self.newNameEntry.setPlaceholderText("New name of university")
        self.newAddressEntry=QLineEdit()
        self.newAddressEntry.setPlaceholderText("New address of university")
        self.addBtn = QPushButton("Add")
        self.addBtn.clicked.connect(self.addUniversity)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateUniversity)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteUniversity)

        ############List of the nameCombo items############
        global university_id
        query1 = ("SELECT * From University")
        universities = cur.execute(query1).fetchall()
        for university in universities:
            self.nameCombo.addItem(university[1],university[0])


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Add")
        self.middleGroupBox = QGroupBox("Update/Delete")
        #############add widgets############
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addImg)
        self.topLayout.addRow(QLabel("University Name: "), self.addUniEnrty)
        self.topLayout.addRow(QLabel("Address"),self.addUniAddressEntry)
        self.topLayout.addRow(QLabel(""), self.addBtn)
        self.topGroupBox.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name: "), self.nameCombo)
        self.bottomLayout.addRow(QLabel("New Name: "), self.newNameEntry)
        self.bottomLayout.addRow(QLabel("New Address: "), self.newAddressEntry)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)

        self.middleGroupBox.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topGroupBox)
        self.mainLayout.addWidget(self.middleGroupBox)

        self.setLayout(self.mainLayout)

    def changeComboValue(self):
        global university_id
        university_id = self.nameCombo.currentData()

    def addUniversity(self):
        name=self.addUniEnrty.text()
        address=self.addUniAddressEntry.text()
        if(name and address !=""):
            try:
                query = "INSERT INTO University (Name,Address) VALUES (?,?)"
                cur.execute(query, (name,address))
                con.commit()
                QMessageBox.information(self, "Info", "University has been added")
                self.addUniEnrty.setText("")
                self.addUniAddressEntry.setText("")

            except:
                QMessageBox.information(self, "Info", "University has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields con not be empty!!!")


    def updateUniversity(self):
        global university_id
        newName=self.newNameEntry.text()
        newAddress=self.newAddressEntry.text()
        if (newName and newAddress!= ""):
            try:
                query = "UPDATE University set Name=?,Address=? WHERE UniversityID=?"
                cur.execute(query, (newName,newAddress,university_id))
                con.commit()
                QMessageBox.information(self, "Info", "University has been updated!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "University has not been updated!")
        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!!!")

    def deleteUniversity(self):
        global university_id

        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this university",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM University WHERE UniversityID=?", (university_id,))
                con.commit()
                QMessageBox.information(self, "Info", "University has been deleted!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "University has not been deleted!")
