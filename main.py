import re
import sys
import json
from os import system
import requests

url = 'https://orar.usv.ro/orar/vizualizare/orarSPG.php'
params = {
    'ID': '51',
    'mod': 'grupa',
    'mod2': 'vizual',
    'print': 'nu',
    'an': '24_25',
    'sem': '1',
    'back': ''
}
timetable = ''


def get_timetable():
    print('Se obține orarul...')
    response = requests.get(url, params=params)
    timetable = response.text
    with open('timetable.html', 'w') as f:
        f.write(timetable)
    system('clear')
    return timetable


def select_semigrupa():
    system('clear')
    global timetable
    group = input("Dati semigrupa: ")
    while len(group) != 5 or not group[:4].isnumeric() or not group[4].isalpha():
        group = input("Grupa introdusa este invalida, incercati din nou:")
    with open('semigrupe.json', 'r') as f:
        semigrupe = json.load(f)
        for s in semigrupe:
            if s['groupName'] == group[:4] and s['subgroupIndex'] == group[4]:
                params['ID'] = s['id']
                timetable = get_timetable()
                break


def display_menu(menu):
    """
    Display a menu where the key identifies the name of a function.
    :param menu: dictionary, key identifies a value which is a function name
    :return:
    """
    for k, function in menu.items():
        print(k, function.__name__)


def clear():
    input("\nApasă Enter pentru a continua\n")
    system('clear')  # clears stdout


def cursuri():
    matches = re.findall(
        r"cadru didactic: ([^<]+)[^,]+>([a-zA-Z0-9]+),curs", timetable)
    if matches:
        print("\nSemigrupa selectată are următoarele cursuri:")
        for m in matches:
            print(f"  • {m[1] + ', ' + m[0].strip()}")
    else:
        print("\nSemigrupa selectată nu are cursuri")

    clear()


def laboratoare():
    pattern = r"activitate cuprinsa intre [0-9]{2} si [0-9]{2}(, in saptamanile (impare|pare))?<li>disciplina: [^<]+<\/li><li>sala: [^<]+<\/li><li>cadru didactic: ([^<]+)[^,]+>([a-zA-Z0-9]+),lab"
    matches = re.findall(pattern, timetable)
    l_pare = []
    l_impare = []
    l = []
    for m in matches:
        if m[1] == 'impare':
            l_impare.append(m[3] + ', ' + m[2].strip())
        elif m[1] == 'pare':
            l_pare.append(m[3] + ', ' + m[2].strip())
        else:
            l.append(m[3] + ', ' + m[2].strip())
    if l_impare:
        print('\nLaboratoare în săptămâni impare:')
        for lab in l_impare:
            print(f"  • {lab}")
    else:
        print("\nSemigrupa selectată nu are laboratoare în săptămânile impare")

    if l_pare:
        print('\nLaboratoare în săptămâni pare:')
        for lab in l_pare:
            print(f"  • {lab}")
    else:
        print("\nSemigrupa selectată nu are laboratoare în săptămânile pare")
    if l:
        print('\nLaboratoare în toate săptămânile:')
        for lab in l:
            print(f"  • {lab}")
    else:
        print("\nSemigrupa selectată nu are laboratoare în toate săptămânile")

    clear()


def profesori():
    matches = re.findall(r"cadru didactic: ([^<]+)", timetable)
    matches = set(matches)

    if matches:
        print("\nSemigrupa selectată are următorii profesori:")
        for m in matches:
            print(f"  • {m.strip()}")
    else:
        print("\nSemigrupa selectată nu are profesori")
    clear()


def ore():
    pattern = r"activitate cuprinsa intre ([0-9]{2}) si ([0-9]{2})(, in saptamanile (impare|pare))?"
    matches = re.findall(pattern, timetable)
    ore_pare = 0
    ore_impare = 0
    ore = 0
    for m in matches:
        durata = int(m[1]) - int(m[0])
        if m[3] == 'impare':
            ore_impare += durata
        elif m[3] == 'pare':
            ore_pare += durata
        else:
            ore += durata
    print('Semigrupa introdusă trebuie să stea la facultate ' +
          str(ore + ore_impare) + ' ore în săptămânile impare')
    print('Semigrupa introdusă trebuie să stea la facultate ' +
          str(ore + ore_pare) + ' ore în săptămânile pare')
    clear()


def proiecte():
    matches = re.findall(
        r"cadru didactic: ([^<]+)[^,]+>([a-zA-Z0-9]+),pr", timetable)

    if matches:
        print("\nSemigrupa selectată are următoarele proiecte:")
        for m in matches:
            print(f"  • {m[1] + ', ' + m[0].strip()}")
    else:
        print("\nSemigrupa selectată nu are proiecte")
    clear()


def tutoriat():
    matches = re.findall(
        r"disciplina: Activitati de tutoriat[^<]+<\/li><li>sala: [^<]+<\/li><li>cadru didactic: ([^<]+).*AT", timetable)

    if matches:
        print("\nSemigrupa selectată are activități de tutoriat cu:")
        for m in matches:
            print(f"  • {m}")
    else:
        print("\nSemigrupa selectată nu are activități de tutoriat trecute în orar")
    clear()


def iesire():
    system('clear')
    print("Pa")
    sys.exit()


def main():
    functions_names = [cursuri, laboratoare, profesori,
                       ore, proiecte, tutoriat, select_semigrupa, iesire]
    menu_items = dict(enumerate(functions_names, start=1))
    select_semigrupa()
    while True:
        display_menu(menu_items)
        selection = input("Alege o optiune: ")
        if not selection.isnumeric() or selection < '1' or selection > '9':
            print('Input invalid')
            input('Apasă Enter pentru a continua')
            system('clear')
            continue
        selected_value = menu_items[int(selection)]
        selected_value()


if __name__ == "__main__":
    main()
