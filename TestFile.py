import re
import io
from Database import *

# jesli lang = "" to z pliku, jak nie to source stanowi tekst do przetworzenia
def test_file(source, lang=""):
    if lang == "":
        t = source.split('.')
        file = open(source, 'r')
    else:
        t = [0, lang]

    db = Database()
    occurs = []
    for vuln in db.getVulnerabilities(t[1]):
        if lang == "":
            file.seek(0)
        else:
            file = io.StringIO(source)
        counter = 0
        where = []
        index = 0
        for line in file:
            index += 1

            if vuln.get('regexp') in line:
                counter += 1
                where.append(index)
            else:
                pattern = re.compile(vuln.get('regexp'))
                if pattern.match(line):
                    counter += 1
                    where.append(index)

        if counter > 0:
            occurs.append([where, vuln.get('regexp'), vuln.get('reason'), vuln.get('solution')])

    output = ''
    for o in occurs:
        output += "Line(s):"
        for l in o[0]:
            output += ' ' + str(l) + ','
        output += " found: " + o[1] + ", \n\tnote: " + o[2] + ", \n\tsolution:"
        for r in o[3]:
            output += ' ' + r + ';'
        output += '\n'
    if lang == "":
        file.close()
    return output