from Mongo import *


class Database:
    def __init__(self):
        database = getDatabase()
        self.vuln = database["vulnerability"]


    def getVulnerabilities(self, lang = None):
        # połączenie do bazy
        if lang:
            return self.vuln.find({"language": lang})  # zwraca rekordy dla danego języka
        else:
            return self.vuln.find()  # zwraca wszystkie rekordy z bazy

    def addVulnerability(self, wyrazenie, reason, solution, lang, lib = None):
        # tworzenie wiersza do wpisania do bazy
        if lib:
            row = dict([
                ('regexp', wyrazenie),
                ('reason', reason),
                ('solution', solution),
                ('language', lang),
                ('library', lib)
            ])
            # print(row)
            # wstawianie dokumentu do bazy
            self.vuln.insert_one(row)
        else:
            row = dict([
                ('regexp', wyrazenie),
                ('reason', reason),
                ('solution', solution),
                ('language', lang)
            ])
            # print(row)
            # wstawianie dokumentu do bazy
            self.vuln.insert_one(row)

