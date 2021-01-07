import sys
import pypyodbc
from PyQt5.QtWidgets import *
from PyQt5.QtGui  import *
from PyQt5.QtCore import Qt

import addauthor
import addensitute
import addlanguage
import addsupervisor
import addthesis
import adduniversity
import addsubject

###################Databese Connection###################333
con = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=DESKTOP-63U3JN8\SQLEXPRESS2019;'
    'Database=TermProject;'
    'Trusted_Connection=True;'
)
cur = con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Thesis Manager")
        self.setWindowIcon(QIcon('icons/list.png'))
        self.setGeometry(350,150,1500,750)

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayThesis()
        self.displayAuthor()

    def toolBar(self):
        self.tb=self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ############Toolbar Buttons############
        ############Add Thesis################
        self.addThesis=QAction(QIcon('icons/add.png'),"Add Thesis",self)
        self.tb.addAction(self.addThesis)
        self.addThesis.triggered.connect(self.funcAddThesis)
        self.tb.addSeparator()
        ############Add Author#################
        self.addAuthor = QAction(QIcon('icons/users.png'), "Add Author", self)
        self.tb.addAction(self.addAuthor)
        self.addAuthor.triggered.connect(self.funcAddAuthor)
        self.tb.addSeparator()
        ############Add Language#################
        self.addLanguage = QAction(QIcon('icons/addlanguage.png'), "Add Language", self)
        self.tb.addAction(self.addLanguage)
        self.addLanguage.triggered.connect(self.funcAddLanguage)
        self.tb.addSeparator()
        ############Add University#################
        self.addUniversity=QAction(QIcon('icons/adduni.png'),"Add University",self)
        self.tb.addAction(self.addUniversity)
        self.addUniversity.triggered.connect(self.funcAddUniversity)
        self.tb.addSeparator()
        ############Add Ensitute#################
        self.addEnstitute = QAction(QIcon('icons/addins.png'), "Add Enstitute", self)
        self.tb.addAction(self.addEnstitute)
        self.addEnstitute.triggered.connect(self.funcAddEnstitute)
        self.tb.addSeparator()
        ############Add Subject#################
        self.addSubject = QAction(QIcon('icons/addins.png'), "Add Subject", self)
        self.tb.addAction(self.addSubject)
        self.addSubject.triggered.connect(self.funcAddSubject)
        self.tb.addSeparator()
        ############Add Supervisor#################
        self.addSupervisor = QAction(QIcon('icons/users.png'), "Add Supervisor", self)
        self.tb.addAction(self.addSupervisor)
        self.addSupervisor.triggered.connect(self.funcAddSupervisor)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs=QTabWidget()
        self.setCentralWidget(self.tabs)#tab in ana ekranda gözükmesi için lazım olan kod
        self.tab1=QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Thesis")
        self.tabs.addTab(self.tab2, "Authors")

    def widgets(self):
        ##############Tab1 widgets##################
        #############Main left layout Widget##################
        self.thesisTable = QTableWidget()
        self.thesisTable.setColumnCount(15)
        self.thesisTable.setColumnHidden(0, True)
        self.thesisTable.setColumnHidden(13,True)
        self.thesisTable.setColumnHidden(14,True)
        self.thesisTable.setHorizontalHeaderItem(0, QTableWidgetItem("Thesis Id"))
        self.thesisTable.setHorizontalHeaderItem(1, QTableWidgetItem("Thesis Title"))
        self.thesisTable.setHorizontalHeaderItem(2, QTableWidgetItem("Author"))
        self.thesisTable.setHorizontalHeaderItem(3, QTableWidgetItem("Year"))
        self.thesisTable.setHorizontalHeaderItem(4, QTableWidgetItem("Type"))
        self.thesisTable.setHorizontalHeaderItem(5, QTableWidgetItem("University"))
        self.thesisTable.setHorizontalHeaderItem(6, QTableWidgetItem("Institute"))
        self.thesisTable.setHorizontalHeaderItem(7, QTableWidgetItem("Page No"))
        self.thesisTable.setHorizontalHeaderItem(8, QTableWidgetItem("Language"))
        self.thesisTable.setHorizontalHeaderItem(9, QTableWidgetItem("Subject"))
        self.thesisTable.setHorizontalHeaderItem(10, QTableWidgetItem("Supervisor"))
        self.thesisTable.setHorizontalHeaderItem(11,QTableWidgetItem("Co-supervisor"))
        self.thesisTable.setHorizontalHeaderItem(12, QTableWidgetItem("Keyword"))
        self.thesisTable.setHorizontalHeaderItem(13, QTableWidgetItem("Abstract"))
        self.thesisTable.setHorizontalHeaderItem(14, QTableWidgetItem("Content"))

        self.thesisTable.setEditTriggers(QTableWidget.NoEditTriggers)
        self.thesisTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.thesisTable.doubleClicked.connect(self.doubleClickEvent)
        #############Right Top  layout Widget##################
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search For Thesis")
        self.searchCombo=QComboBox()
        self.searchCombo.addItem("All")
        self.searchCombo.addItem("Thesis Title")
        self.searchCombo.addItem("Author")
        self.searchCombo.addItem("Supervisor")
        self.searchCombo.addItem("Subject")
        self.searchCombo.addItem("Abstract")
        self.searchCombo.addItem("Type")
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchThesis)
        self.refreshThesis=QPushButton("Refresh")
        self.refreshThesis.clicked.connect(self.refreshedThesis)
        ##############Tab2 widgets##################
        self.authorsTable = QTableWidget()
        self.authorsTable.setColumnCount(4)
        self.authorsTable.setColumnHidden(0,True)
        self.authorsTable.setHorizontalHeaderItem(0, QTableWidgetItem("Author ID"))
        self.authorsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Author Name"))
        self.authorsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Address"))
        self.authorsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Gender"))
        self.authorsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.authorsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.authorsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.authorsTable.doubleClicked.connect(self.selectedAuthor)
        self.refresh=QPushButton("Refresh")
        self.refresh.clicked.connect(self.refreshed)


    def layouts(self):
        ##############Tab1 Layout################
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QFormLayout()
        self.rightMiddleLayout = QFormLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.middleGroupBox = QGroupBox("List Box")
        ##############Add Widgets################
        ##############Left Main Layout Widgets################
        self.mainLeftLayout.addWidget(self.thesisTable)
        ##############Right Top Layout Widgets################
        self.rightTopLayout.addRow(self.searchText,self.searchEntry)
        self.rightTopLayout.addRow(QLabel(""),self.searchCombo)
        self.rightTopLayout.addRow(QLabel(""),self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)

        self.mainRightLayout.addWidget(self.refreshThesis)
        self.mainRightLayout.addWidget(self.topGroupBox)

        self.mainLayout.addLayout(self.mainLeftLayout, 70)
        self.mainLayout.addLayout(self.mainRightLayout, 30)
        self.tab1.setLayout(self.mainLayout)

        ##############Tab2 Layout################
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QHBoxLayout()
        self.memberRightLayout = QHBoxLayout()
        self.memberRightGroupBox = QGroupBox()
        self.memberRightGroupBox.setContentsMargins(10, 10, 10, 600)
        self.memberRightLayout.addWidget(self.refresh)

        self.memberRightGroupBox.setLayout(self.memberRightLayout)

        self.memberLeftLayout.addWidget(self.authorsTable)
        self.memberMainLayout.addLayout(self.memberLeftLayout, 70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox, 30)
        self.tab2.setLayout(self.memberMainLayout)

    def refreshedThesis(self):
        self.displayThesis()

    def refreshed(self):
        self.authorsTable.setFont(QFont("Arial", 12))
        for i in reversed(range(self.authorsTable.rowCount())):
            self.authorsTable.removeRow(i)

        authors = cur.execute("SELECT * FROM Author")
        for row_data in authors:
            row_number = self.authorsTable.rowCount()
            self.authorsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.authorsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.authorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def funcAddThesis(self):
        self.newThesis=addthesis.AddThesis()

    def funcAddAuthor(self):
        self.newAuthor=addauthor.AddAuthor()

    def funcAddUniversity(self):
        self.newUniversity=adduniversity.AddUniversity()

    def funcAddEnstitute(self):
        self.newEnstitute=addensitute.AddEnstitute()

    def funcAddLanguage(self):
        self.addLanguage=addlanguage.AddLanguage()

    def funcAddSubject(self):
        self.addSubject=addsubject.AddSubject()

    def funcAddSupervisor(self):
        self.addSupervisor=addsupervisor.AddSupervisor()

    def displayThesis(self):
        for i in reversed(range(self.thesisTable.rowCount())):
            self.thesisTable.removeRow(i)
        query =cur.execute('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
		From Thesis as T
		INNER JOIN University as U
		ON U.UniversityID=T.UniversityID
		INNER JOIN Author as A
		ON A.AuthorID=T.AuthorID
		INNER JOIN Institute as I
		ON I.InstituteID=T.InstituteID
		INNER JOIN Language as L
		ON L.LanguageID=T.LanguageID
		LEFT OUTER JOIN Supervisor as S
		ON S.SupervisorID=T.SupervisorID
		LEFT OUTER JOIN Supervisor as Co
		ON Co.SupervisorID=T.CosupervisorID
		INNER JOIN Subject as Sub
		ON Sub.SubjectID=T.SubjectID
	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')

        for row_data in query:
            row_number = self.thesisTable.rowCount()
            self.thesisTable.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.thesisTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def displayAuthor(self):
        self.authorsTable.setFont(QFont("Arial", 12))
        for i in reversed(range(self.authorsTable.rowCount())):
            self.authorsTable.removeRow(i)

        authors = cur.execute("SELECT * FROM Author")
        for row_data in authors:
            row_number = self.authorsTable.rowCount()
            self.authorsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.authorsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.authorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedAuthor(self):
        global authorId
        listAuthor = []
        for i in range(0, 4):
            listAuthor.append(self.authorsTable.item(self.authorsTable.currentRow(), i).text())

        authorId = listAuthor[0]
        self.displayAuthor = DisplayAuthor()
        self.displayAuthor.show()


    def searchThesis(self):
        value=self.searchEntry.text()
        comboValue=self.searchCombo.currentText()
        self.searchEntry.setText("")
        if value == "":
            QMessageBox.information(self, "Warning", "Search query cant be empty!")
        else:
            if(comboValue == "All"):
                query=('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
		From Thesis as T
		INNER JOIN University as U
		ON U.UniversityID=T.UniversityID
		INNER JOIN Author as A
		ON A.AuthorID=T.AuthorID
		INNER JOIN Institute as I
		ON I.InstituteID=T.InstituteID
		INNER JOIN Language as L
		ON L.LanguageID=T.LanguageID
		LEFT OUTER JOIN Supervisor as S
		ON S.SupervisorID=T.SupervisorID
		LEFT OUTER JOIN Supervisor as Co
		ON Co.SupervisorID=T.CosupervisorID
		INNER JOIN Subject as Sub
		ON Sub.SubjectID=T.SubjectID
		WHERE T.Title LIKE ? or A.Name LIKE ? or S.Name LIKE ? or Sub.Name LIKE ? or T.Abstract LIKE ?
	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results=cur.execute(query,('%' + value + '%','%' + value + '%','%' + value + '%','%' + value + '%','%' + value + '%')).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            elif(comboValue == "Thesis Title"):
                query=('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
		From Thesis as T
		INNER JOIN University as U
		ON U.UniversityID=T.UniversityID
		INNER JOIN Author as A
		ON A.AuthorID=T.AuthorID
		INNER JOIN Institute as I
		ON I.InstituteID=T.InstituteID
		INNER JOIN Language as L
		ON L.LanguageID=T.LanguageID
		LEFT OUTER JOIN Supervisor as S
		ON S.SupervisorID=T.SupervisorID
		LEFT OUTER JOIN Supervisor as Co
		ON Co.SupervisorID=T.CosupervisorID
		INNER JOIN Subject as Sub
		ON Sub.SubjectID=T.SubjectID
		WHERE T.Title LIKE ?
	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results=cur.execute(query,('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            elif (comboValue == "Thesis Title"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
            		From Thesis as T
            		INNER JOIN University as U
            		ON U.UniversityID=T.UniversityID
            		INNER JOIN Author as A
            		ON A.AuthorID=T.AuthorID
            		INNER JOIN Institute as I
            		ON I.InstituteID=T.InstituteID
            		INNER JOIN Language as L
            		ON L.LanguageID=T.LanguageID
            		LEFT OUTER JOIN Supervisor as S
            		ON S.SupervisorID=T.SupervisorID
            		LEFT OUTER JOIN Supervisor as Co
            		ON Co.SupervisorID=T.CosupervisorID
            		INNER JOIN Subject as Sub
            		ON Sub.SubjectID=T.SubjectID
            		WHERE T.Title LIKE ?
            	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            elif (comboValue == "Author"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
            		From Thesis as T
            		INNER JOIN University as U
            		ON U.UniversityID=T.UniversityID
            		INNER JOIN Author as A
            		ON A.AuthorID=T.AuthorID
            		INNER JOIN Institute as I
            		ON I.InstituteID=T.InstituteID
            		INNER JOIN Language as L
            		ON L.LanguageID=T.LanguageID
            		LEFT OUTER JOIN Supervisor as S
            		ON S.SupervisorID=T.SupervisorID
            		LEFT OUTER JOIN Supervisor as Co
            		ON Co.SupervisorID=T.CosupervisorID
            		INNER JOIN Subject as Sub
            		ON Sub.SubjectID=T.SubjectID
            		WHERE A.Name LIKE ?
            	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            elif (comboValue == "Supervisor"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
            		From Thesis as T
            		INNER JOIN University as U
            		ON U.UniversityID=T.UniversityID
            		INNER JOIN Author as A
            		ON A.AuthorID=T.AuthorID
            		INNER JOIN Institute as I
            		ON I.InstituteID=T.InstituteID
            		INNER JOIN Language as L
            		ON L.LanguageID=T.LanguageID
            		LEFT OUTER JOIN Supervisor as S
            		ON S.SupervisorID=T.SupervisorID
            		LEFT OUTER JOIN Supervisor as Co
            		ON Co.SupervisorID=T.CosupervisorID
            		INNER JOIN Subject as Sub
            		ON Sub.SubjectID=T.SubjectID
            		WHERE S.Name LIKE ?
            	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            elif (comboValue == "Subject"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
            		From Thesis as T
            		INNER JOIN University as U
            		ON U.UniversityID=T.UniversityID
            		INNER JOIN Author as A
            		ON A.AuthorID=T.AuthorID
            		INNER JOIN Institute as I
            		ON I.InstituteID=T.InstituteID
            		INNER JOIN Language as L
            		ON L.LanguageID=T.LanguageID
            		LEFT OUTER JOIN Supervisor as S
            		ON S.SupervisorID=T.SupervisorID
            		LEFT OUTER JOIN Supervisor as Co
            		ON Co.SupervisorID=T.CosupervisorID
            		INNER JOIN Subject as Sub
            		ON Sub.SubjectID=T.SubjectID
            		WHERE Sub.Name LIKE ?
            	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            elif (comboValue == "Abstract"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
            		From Thesis as T
            		INNER JOIN University as U
            		ON U.UniversityID=T.UniversityID
            		INNER JOIN Author as A
            		ON A.AuthorID=T.AuthorID
            		INNER JOIN Institute as I
            		ON I.InstituteID=T.InstituteID
            		INNER JOIN Language as L
            		ON L.LanguageID=T.LanguageID
            		LEFT OUTER JOIN Supervisor as S
            		ON S.SupervisorID=T.SupervisorID
            		LEFT OUTER JOIN Supervisor as Co
            		ON Co.SupervisorID=T.CosupervisorID
            		INNER JOIN Subject as Sub
            		ON Sub.SubjectID=T.SubjectID
            		WHERE T.Abstract LIKE ?
            	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
            		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            elif (comboValue == "Type"):
                query = ('''SELECT T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
                		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content
                		From Thesis as T
                		INNER JOIN University as U
                		ON U.UniversityID=T.UniversityID
                		INNER JOIN Author as A
                		ON A.AuthorID=T.AuthorID
                		INNER JOIN Institute as I
                		ON I.InstituteID=T.InstituteID
                		INNER JOIN Language as L
                		ON L.LanguageID=T.LanguageID
                		LEFT OUTER JOIN Supervisor as S
                		ON S.SupervisorID=T.SupervisorID
                		LEFT OUTER JOIN Supervisor as Co
                		ON Co.SupervisorID=T.CosupervisorID
                		INNER JOIN Subject as Sub
                		ON Sub.SubjectID=T.SubjectID
                		WHERE T.Type LIKE ?
                	GROUP BY T.ThesisNumber,T.Title,A.Name,T.Year,T.Type,U.Name,I.Name,T.NumberofPages,
                		L.Name,Sub.Name,S.Name,Co.Name,T.Keyword,T.Abstract,T.Content''')
                results = cur.execute(query, ('%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Warning", "There is no such a thesis")
                else:
                    for i in reversed(range(self.thesisTable.rowCount())):
                        self.thesisTable.removeRow(i)
                    for row_data in results:
                        row_number = self.thesisTable.rowCount()
                        self.thesisTable.insertRow(row_number)
                        for column_number, data in enumerate(row_data):
                            self.thesisTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def doubleClickEvent(self):
        global selected_abstract,selected_content,selected_id,selected_title
        list = []

        for i in range(0, 15):
            list.append(self.thesisTable.item(self.thesisTable.currentRow(), i).text())

        selected_abstract = list[13]
        selected_content = list[14]
        selected_title=list[1]
        selected_id=list[0]
        self.doubleClick=DoubleClick()
        self.doubleClick.show()

class DoubleClick(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Details")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1000,800)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        global selected_abstract,selected_content,selected_id
        ###################widgets of left layout##########
        self.abstractText=QTextEdit()
        self.abstractText.setText(selected_abstract)
        self.abstractText.setReadOnly(True)
        self.titleText=QTextEdit()
        self.titleText.setText(selected_title)
        self.titleText.setReadOnly(True)
        self.deletebtn=QPushButton("DELETE")
        self.deletebtn.clicked.connect(self.deleteThesis)
        self.spacerItem =QSpacerItem(20, 40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        #################widgets of right layot###########
        self.contentText=QTextEdit()
        self.contentText.setText(selected_content)
        self.contentText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.contentText.setReadOnly(True)



    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QHBoxLayout()
        self.leftFrame = QGroupBox("Title")
        self.rightFrame = QGroupBox("Content")
        self.rightFrame.setFont(QFont("Arial",12))
        ##################add widgets###################
        ###########widgets of toplayout##############
        self.leftLayout.addWidget(self.titleText)
        self.leftLayout.addWidget(QLabel("Abstract"))
        self.leftLayout.addWidget(self.abstractText)
        self.leftLayout.addItem(self.spacerItem)
        self.leftLayout.addWidget(self.deletebtn)
        self.leftFrame.setLayout(self.leftLayout)
        ###############Widgets of form layout##########
        self.rightLayout.addWidget(self.contentText)
        self.rightFrame.setLayout(self.rightLayout)

        self.mainLayout.addWidget(self.leftFrame,40)
        self.mainLayout.addWidget(self.rightFrame,60)
        self.setLayout(self.mainLayout)

    def deleteThesis(self):
        global selected_id

        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this Thesis",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM Thesis WHERE product_id=?", (selected_id,))
                con.commit()
                QMessageBox.information(self, "Info", "Thesis has been deleted!")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Thesis has not been deleted!")


class DisplayAuthor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Author Details")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 350, 600)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.authorDetails()
        self.widgets()
        self.layouts()

    def authorDetails(self):
        global authorId
        query = ("SELECT * FROM Author WHERE AuthorID=?")
        author = cur.execute(query, (authorId,)).fetchone()
        self.authorName = author[1]
        self.authorAddress= author[2]
        self.authorGender = author[3]

    def widgets(self):
        ###############Widgets of top layout############
        self.memberImg = QLabel()
        self.img = QPixmap('icons/members.png')
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display Member")
        self.titleText.setAlignment(Qt.AlignCenter)
        ###################widgets of bottom layout#########
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.authorName)
        self.addressEntry = QLineEdit()
        self.addressEntry.setText(self.authorAddress)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateAuthor)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteAuthor)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()

        self.bottomFrame = QFrame()

        ##############add widgets######3
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Address: "), self.addressEntry)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def deleteAuthor(self):
        global authorId
        mbox = QMessageBox.question(self, "Warning", "Are you sure to delete this author",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if mbox == QMessageBox.Yes:
            try:
                query = "DELETE FROM Author WHERE AuthorID=?"
                cur.execute(query, (authorId,))
                con.commit()
                QMessageBox.information(self, "Info", "Author has been deleted!")
            except:
                QMessageBox.information(self, "Info", "Author has not been deleted!")

    def updateAuthor(self):
        global authorId
        name = self.nameEntry.text()
        address = self.addressEntry.text()

        if (name and address != ""):
            try:
                query = "UPDATE Author set Name=?, Address=? WHERE authorId=?"
                cur.execute(query, (name, address, authorId))
                con.commit()
                QMessageBox.information(self, "Info", "Author has been updated!")

            except:
                QMessageBox.information(self, "Info", "Author has been updated!")

        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!")


def main():
    App=QApplication(sys.argv)
    window=Main()
    sys.exit(App.exec_())

if __name__=='__main__':
    main()