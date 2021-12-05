from __future__ import unicode_literals

from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import *
from PyQt5.uic.properties import QtCore

from DirectoryTest import *


#filename = input("Enter path: ")
#out = test_directory(filename)
#print(out)



class codeValidator(QDialog):
    def __init__(self):
        super(codeValidator, self).__init__()

        self.mode = QComboBox()
        self.mode.addItems(["Python", "Java", "C", "File", "Directory"])

        # tekst: wpisz kod
        enterCodeText = QLabel("Enter code to evaluate: ", self)
        ukladT = QGridLayout()
        ukladT.addWidget(enterCodeText, 0, 0)

        # okno wpisywania
        self.codeWindow = QTextEdit()
        self.codeWindow.resize(1200, 500)
        self.codeWindow.setPlaceholderText("Input here")
        # ^Ta metoda nie dziala, trzeba znalezc cos co zadziala
        # okno wyniku
        self.evaluationResultsWindow = QTextEdit()
        self.evaluationResultsWindow.resize(1200, 500)
        self.evaluationResultsWindow.setReadOnly(True)

        # ulozenie okien
        ukladT.addWidget(self.codeWindow, 1, 0)
        ukladT.addWidget(self.evaluationResultsWindow, 2, 0)
        # guziki
        evaluateButton = QPushButton("&Evaluate", self)
        evaluateButton.clicked.connect(self.evaluate)
        ukladH = QHBoxLayout()
        ukladH.addWidget(evaluateButton)

        ukladHH = QHBoxLayout()
        ukladHH.addWidget(self.mode)

        ukladT.addLayout(ukladH, 2, 1, 2, 2)
        ukladT.addLayout(ukladHH, 0, 1, 2, 2)
        self.setLayout(ukladT)
        self.setGeometry(20, 20, 300, 100)
        self.resize(1280, 900)
        self.setWindowTitle("CodeV")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.show()

    def evaluate(self):
        out ='NONE'
        if self.mode.currentText() == 'Python':
            out = test_file(self.codeWindow.toPlainText(), "py")
        elif self.mode.currentText() == 'Java':
            out = test_file(self.codeWindow.toPlainText(), "java")
        elif self.mode.currentText() == 'C':
            out = test_file(self.codeWindow.toPlainText(), "c")
        elif self.mode.currentText() == 'File':
            out = test_file(self.codeWindow.toPlainText())
        elif self.mode.currentText() == 'Directory':
            out = test_directory(self.codeWindow.toPlainText())
        self.evaluationResultsWindow.setText(out)


class mainMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()

    def interfejs(self):
        ukladT = QGridLayout()
        enterEvaluationButton = QPushButton("&Evaluate code", self)
        enterAddVulnerability = QPushButton("&Add new vulnerability", self)
        uklad1 = QHBoxLayout()
        uklad1.addWidget(enterEvaluationButton)
        uklad2 = QHBoxLayout()
        uklad2.addWidget(enterAddVulnerability)
        ukladT.addLayout(uklad1, 1, 1, 1, 1)
        ukladT.addLayout(uklad2, 2, 1, 1, 1)
        self.setLayout(ukladT)
        enterEvaluationButton.clicked.connect(self.onEnterEvaluate)
        enterAddVulnerability.clicked.connect(self.onEnterAddVulnerability)
        self.setGeometry(20, 20, 300, 100)
        self.resize(300, 100)
        self.setWindowTitle("CodeV")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.show()

    def onEnterEvaluate(self):
        self.window = codeValidator()
        self.window.show()
        self.close()

    def onEnterAddVulnerability(self):
        self.window2 = addVulnerability("Solution", [])
        self.window2.show()
        self.close()


class addVulnerability(QDialog):
    def __init__(self, name, proList=None):
        super(addVulnerability, self).__init__()

        self.name = name
        self.list = QListWidget()

        if proList is not None:
            self.list.addItems(proList)
            self.list.setCurrentRow(0)

        vbox = QVBoxLayout()

        for text, slot in (("Add", self.add),
                           ("Edit", self.edit),
                           ("Remove", self.remove),
                           ("Accept", self.accept)):
            button = QPushButton(text)

            vbox.addWidget(button)
            button.clicked.connect(slot)
        self.languagesList = QComboBox()
        self.languagesList.addItems(["Python", "Java", "C"])
        self.regexp = QLineEdit()
        self.regexp.setPlaceholderText("REGEXP")
        self.reason = QLineEdit()
        self.reason.setPlaceholderText("REASON")
        self.solution = QLabel("Solutions", self)
        ibox = QVBoxLayout()
        ibox.addWidget(self.languagesList)
        ibox.addWidget(self.regexp)
        ibox.addWidget(self.reason)
        hbox = QHBoxLayout()
        ibox.addWidget(self.solution)
        ibox.addWidget(self.list)
        hbox.addLayout(ibox)
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.setWindowTitle("CodeV")

        self.setWindowIcon(QtGui.QIcon("icon.png"))

    def add(self):
        row = self.list.currentRow()
        title = "Add {0}".format(self.name)
        string, ok = QInputDialog.getText(self, title, title)
        if ok and string is not None:
            self.list.insertItem(row, string)

    def edit(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is not None:
            title = "Edit {0}".format(self.name)
            string, ok = QInputDialog.getText(self, title, title,
                                              QLineEdit.Normal, item.text())
            if ok and string is not None:
                item.setText(string)

    def remove(self):
        row = self.list.currentRow()
        item = self.list.item(row)
        if item is None:
            return
        reply = QMessageBox.question(self, "Remove {0}".format(
            self.name), "Remove {0} `{1}'?".format(
            self.name, str(item.text())),
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.list.takeItem(row)
            del item

    def accept(self):
        db = Database()
        it = []
        for x in range(self.list.count()):
            it.append(self.list.item(x).text())
        langg = 'py'
        if self.languagesList.currentText() == 'Python': langg = 'py'
        elif self.languagesList.currentText() == 'Java': langg = 'java'
        elif self.languagesList.currentText() == 'C': langg = 'c'
        db.addVulnerability(self.regexp.text(), self.reason.text(), it, langg)
        self.list.clear()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = mainMenu()
    sys.exit(app.exec_())
