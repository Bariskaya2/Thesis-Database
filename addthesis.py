import datetime
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
defaultImg="store.png"

class AddThesis(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Thesis")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1200,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ###################widgets of top layout##########
        self.addThesisImg = QLabel()
        self.img = QPixmap('icons/add.png')
        self.addThesisImg.setPixmap(self.img)
        self.titleText = QLabel("Add Thesis")
        #################widgets of bottom layot###########
        self.titleEntry = QLineEdit()
        self.titleEntry.setPlaceholderText("Enter title")
        self.authorCombo=QComboBox()
        self.authorCombo.currentIndexChanged.connect(self.changeComboValueAuthor)
        self.abstractEntry= QTextEdit()
        self.abstractEntry.setPlaceholderText("Write abstract")
        self.abstractEntry.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.keywordEntry= QTextEdit()
        self.keywordEntry.setPlaceholderText("Please put commas between keywords")
        self.keywordEntry.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.typeCombo = QComboBox()
        self.typeCombo.addItem("Master")
        self.typeCombo.addItem("Doctoret")
        self.typeCombo.addItem("Specialization In Medicine")
        self.typeCombo.addItem("Proficiency In Art")
        self.uniCombo=QComboBox()
        self.uniCombo.currentIndexChanged.connect(self.changeComboValue)
        self.instituteCombo=QComboBox()
        self.numberOfPage=QComboBox()
        for i in reversed(range(0,201)):
            self.numberOfPage.addItem(str(i))
        self.languageCombo=QComboBox()
        self.languageCombo.currentIndexChanged.connect(self.changeComboValueLanguage)
        self.subjectCombo=QComboBox()
        self.subjectCombo.currentIndexChanged.connect(self.changeComboValueSubject)
        self.supervisorCombo=QComboBox()
        self.supervisorCombo.currentIndexChanged.connect(self.changeComboValueSupervisor)
        self.cosupervisor=QComboBox()
        self.cosupervisor.addItem("")
        self.cosupervisor.addItem("-",None)
        self.cosupervisor.currentIndexChanged.connect(self.changeComboValueCosupervisor)
        self.uploadPdf = QPushButton("Upload")
        self.addBtn = QPushButton("Add")
        self.addBtn.clicked.connect(self.addThesis)

        self.content=QTextEdit()
        self.content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.content.setPlaceholderText("Write Thesis")

        queryauthor = ("SELECT * FROM Author")
        authors = cur.execute(queryauthor).fetchall()
        for author in authors:
            self.authorCombo.addItem(author[1], author[0])

        global university_id
        query1 = ("SELECT * From University")
        universities = cur.execute(query1).fetchall()
        for university in universities:
            self.uniCombo.addItem(university[1], university[0])


        query2 = ("SELECT * FROM Institute")
        institutes = cur.execute(query2).fetchall()
        for institute_name in institutes:
            self.instituteCombo.addItem(institute_name[2], institute_name[0])

        querySubject=("SELECT * FROM Subject")
        subjects=cur.execute(querySubject).fetchall()
        for subject in subjects:
            self.subjectCombo.addItem(subject[1],subject[0])

        querysupervisor=("SELECT * FROM Supervisor")
        supervisors=cur.execute(querysupervisor).fetchall()
        for supervisor in supervisors:
            self.supervisorCombo.addItem(supervisor[1],supervisor[0])
            self.cosupervisor.addItem(supervisor[1],supervisor[0])

        querylanguage = ("SELECT * From Language")
        languages = cur.execute(querylanguage).fetchall()
        for language in languages:
            self.languageCombo.addItem(language[1], language[0])

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout=QVBoxLayout()
        self.mainRightLayout=QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()
        ##################add widgets###################
        ###########widgets of toplayout##############
        self.topLayout.addWidget(self.addThesisImg)
        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)
        ###############Widgets of form layout##########
        self.bottomLayout.addRow(QLabel("Title: "), self.titleEntry)
        self.bottomLayout.addRow(QLabel("Author: "), self.authorCombo)
        self.bottomLayout.addRow(QLabel("Type: "), self.typeCombo)
        self.bottomLayout.addRow(QLabel("Universtiy"), self.uniCombo)
        self.bottomLayout.addRow(QLabel("Enstitute"), self.instituteCombo)
        self.bottomLayout.addRow(QLabel("Page No: "), self.numberOfPage)
        self.bottomLayout.addRow(QLabel("Language: "), self.languageCombo)
        self.bottomLayout.addRow(QLabel("Subject"), self.subjectCombo)
        self.bottomLayout.addRow(QLabel("Supervisor"), self.supervisorCombo)
        self.bottomLayout.addRow(QLabel("Co-Supervisor"), self.cosupervisor)
        self.bottomLayout.addRow(QLabel("Keyword: "), self.keywordEntry)
        self.bottomLayout.addRow(QLabel("Abstract: "), self.abstractEntry)
        self.bottomLayout.addRow(QLabel(""),self.addBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLeftLayout.addWidget(self.topFrame)
        self.mainLeftLayout.addWidget(self.bottomFrame)
        self.mainRightLayout.addWidget(self.content)
        self.mainLayout.addLayout(self.mainLeftLayout,40)
        self.mainLayout.addLayout(self.mainRightLayout,60)
        self.setLayout(self.mainLayout)

    def changeComboValueAuthor(self):
        global author_id
        author_id=self.authorCombo.currentData()

    def changeComboValue(self):
        global university_id
        self.instituteCombo.clear()
        university_id = self.uniCombo.currentData()
        query = ("SELECT Name,InstituteID FROM Institute WHERE UniversityID=?")
        comboNameList =(cur.execute(query, (university_id,)).fetchall())
        for comboName in comboNameList:
            self.instituteCombo.addItem(comboName[0],comboName[1])

    def changeComboValueSubject(self):
        global subject_id
        subject_id=self.subjectCombo.currentData()

    def changeComboValueSupervisor(self):
        global supervisor_id

        supervisor_id=self.supervisorCombo.currentData()
    def changeComboValueCosupervisor(self):
        global cosupervisor_id
        cosupervisor_id=self.cosupervisor.currentData()


    def changeComboValueLanguage(self):
        global language_id
        language_id = self.languageCombo.currentData()


    def addThesis(self):
        global university_id, subject_id, supervisor_id, cosupervisor_id, language_id, author_id
        text=self.cosupervisor.currentText()
        institute_id = self.instituteCombo.currentData()
        title = self.titleEntry.text()
        Tcontent = self.content.toPlainText()
        pageNo = self.numberOfPage.currentText()
        abstract = self.abstractEntry.toPlainText()
        keyword = self.keywordEntry.toPlainText()
        type = self.typeCombo.currentText()
        submissionDate = (datetime.datetime.now()).date()
        year= datetime.datetime.now().year
        ###-------------------this statement for who have same thesis type------------------------###
        #If an author tries to enter the same type of thesis
        query = "SELECT AuthorID FROM Author WHERE AuthorID IN (SELECT AuthorID FROM Thesis WHERE Type=?)"
        masterid = cur.execute(query,(type,)).fetchall()
        acceptable = []
        accept=False
        for i in masterid:
            i = str(i)
            b = i[1:2]
            acceptable.append(b)
        for i in acceptable:
            if (author_id == int(i)):
                accept=True
        ###------------------------------------------------------------------###
        if(title and abstract and Tcontent != ""):
            if (accept == False):#value of false it means selected author already have a same type of thesis
                if (text != ""):
                    if (supervisor_id != cosupervisor_id):
                        try:
                            query = '''INSERT INTO Thesis (Title,Abstract,AuthorID,Year,Type,UniversityID,InstituteID,NumberofPages,LanguageID,SubmissionDate,SupervisorID,SubjectID,CosupervisorID,Keyword,[Content])
                                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                            cur.execute(query, (
                            title, abstract, author_id, year, type, university_id, institute_id, pageNo, language_id,
                            submissionDate, supervisor_id, subject_id, cosupervisor_id, keyword, Tcontent))
                            con.commit()
                            QMessageBox.information(self, "Info", "Thesis has been added")
                            self.close()
                        except:
                            QMessageBox.information(self, "Info", "Thesis has not been added")

                    else:
                        QMessageBox.information(self, "Warning", "Supervisor and Co-supervisor can not be the same")

                else:
                    QMessageBox.information(self, "Warning", "If co-supervisor is not found please select '-'")

            else:
                QMessageBox.information(self, "Warning", "Auther already have same type of thesis")
        else:
            QMessageBox.information(self, "Warning", "Fields can not be empty")















