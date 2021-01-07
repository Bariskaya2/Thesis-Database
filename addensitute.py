import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import pypyodbc

con = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-63U3JN8\SQLEXPRESS2019;'
    'Database=TermProject;'
    'Trusted_Connection=True;'
)
cur = con.cursor()

class AddEnstitute(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Institute")
        self.setWindowIcon(QIcon('icons/list.png'))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        #############widgets of top layout###########
        self.addInstImg = QLabel()
        self.img = QPixmap('icons/list.png')
        self.addInstImg.setPixmap(self.img)
        self.addInstImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Institute")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.selectedUniCombo = QComboBox()
        self.selectedUniCombo.currentIndexChanged.connect(self.changeComboValue)
        self.addEnstituteEnrty = QLineEdit()
        self.addEnstituteEnrty.setPlaceholderText("Enter name of Institute")
        self.addEnstituteAddressEntry = QLineEdit()
        self.addEnstituteAddressEntry.setPlaceholderText("Enter Address of Institute")
        ############widgets of bottom layout############
        self.selectedUniCombo2 = QComboBox()
        self.selectedUniCombo2.currentIndexChanged.connect(self.changeComboValueUpdate)
        self.selectedEnstituteCombo = QComboBox()
        self.newEnstituteNameEntry=QLineEdit()
        self.newEnstituteNameEntry.setPlaceholderText("New name of Institute")
        self.newAddressEntry = QLineEdit()
        self.newAddressEntry.setPlaceholderText("New address of Institute")
        self.addBtn = QPushButton("Add")
        self.addBtn.clicked.connect(self.addEnstitute)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateInstitute)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteInstitute)

        query1 = ("SELECT * From University")
        universities = cur.execute(query1).fetchall()
        for university in universities:
            self.selectedUniCombo.addItem(university[1], university[0])
        query3 = ("SELECT * From University")
        universities2 = cur.execute(query3).fetchall()
        id=universities[0][0]
        query4=("SELECT Name From Institute WHERE UniversityID=?")
        a=cur.execute(query4,(id,)).fetchall()

        for university2 in universities2:
            self.selectedUniCombo2.addItem(university2[1], university2[0])


        global institute_id
        query2 = ("SELECT * FROM Institute")
        institutes = cur.execute(query2).fetchall()

        for institute_name in institutes:
            self.selectedEnstituteCombo.addItem(institute_name[2],institute_name[0])


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Add")
        self.bottomGroupBox = QGroupBox("Update/Delete")
        #############add widgets############
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addInstImg)
        self.topLayout.addRow(QLabel("University Name: "), self.selectedUniCombo)
        self.topLayout.addRow(QLabel("Institute Name:* "), self.addEnstituteEnrty)
        self.topLayout.addRow(QLabel("Address:* "), self.addEnstituteAddressEntry)
        self.topLayout.addRow(QLabel(""), self.addBtn)
        self.topGroupBox.setLayout(self.topLayout)
        #############bottom widgets############
        self.bottomLayout.addRow(QLabel("University: "), self.selectedUniCombo2)
        self.bottomLayout.addRow(QLabel("Institute: "), self.selectedEnstituteCombo)
        self.bottomLayout.addRow(QLabel("New Name: "), self.newEnstituteNameEntry)
        self.bottomLayout.addRow(QLabel("New Address: "), self.newAddressEntry)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomGroupBox.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topGroupBox)
        self.mainLayout.addWidget(self.bottomGroupBox)

        self.setLayout(self.mainLayout)

    def changeComboValue(self):
        global university_id
        university_id = self.selectedUniCombo.currentData()

    def changeComboValueUpdate(self):
        global university_id2
        self.selectedEnstituteCombo.clear()
        university_id2 = self.selectedUniCombo2.currentData()
        query = ("SELECT Name,InstituteID FROM Institute WHERE UniversityID=?")
        comboNameList =(cur.execute(query, (university_id2,)).fetchall())
        for comboName in comboNameList:
            self.selectedEnstituteCombo.addItem(comboName[0],comboName[1])
            #print(comboName)



    def addEnstitute(self):
        global university_id
        addName=self.addEnstituteEnrty.text()
        addAddress=self.addEnstituteAddressEntry.text()


        if (addName and addAddress != ""):

            try:
                query2 = ("INSERT INTO Institute(UniversityID,Name,Address) VALUES (?,?,?)")
                cur.execute(query2, (university_id,addName, addAddress))
                con.commit()
                QMessageBox.information(self, "Info", "Institute has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Institute has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields con not be empty!!!")

    def updateInstitute(self):
        global insitute_id
        insitute_id = self.selectedEnstituteCombo.currentData()

        newName=self.newEnstituteNameEntry.text()
        newAddress=self.newAddressEntry.text()
        selectedName=self.selectedEnstituteCombo.currentText()
        if (newName and newAddress!= ""):
            try:
                query = "UPDATE Institute set Name=?,Address=? WHERE Name=?"
                cur.execute(query, (newName,newAddress,selectedName))
                con.commit()
                QMessageBox.information(self, "Info", "Institute has been updated!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Institute has not been updated!")
        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!!!")

    def deleteInstitute(self):
        insitute_id = self.selectedEnstituteCombo.currentData()
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this Institute",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM Institute WHERE InstituteID=?", (insitute_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Institute has been deleted!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Institute has not been deleted!")


