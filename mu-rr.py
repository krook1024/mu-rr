# Imports
import os
import requests
import pandas as pd
import getpass
import configparser
from tabulate import tabulate

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Global variables
username = ''
password = ''

s = requests.session()

# Functions
def clear():
    os.system("clear")
    os.system("cls")

def login(username, password):
    post_fields = {
        'Username': username,
        'Password': password,
        'tr_agree': 'on',
        'account_login': 'account_login',
        'Login.x': '11',
        'Login.y': '3'
    }

    r = s.post('https://muonline.hu/index.php?mod=250/flogin', data=post_fields)
    r.encoding = 'ISO-8859-2'
    
    if r.status_code == 200:
        if "Hibás felhasználónév vagy jelszó!" in r.text:
            print('We couldn\'t log you in. The program will now exit.')
            input()
            quit()
        else:
            global characters
            characters = pd.read_html(r.content)
            characters = characters[7]
            characters = characters.drop([0], axis=0)

        print('Successfully logged you in.')
    else:
        print('We couldn\'t log you in. The program will now exit.')
        input()
        quit()

def printCharacters(characters):
    headers = ["#", "Name", "Reset", "Level", "Class", "Guild"]
    print(tabulate(characters, headers, showindex="never", tablefmt="fancy_grid"))
        
def reset(charnum):
    charnum += 40

    payload = {'mod': '256', 'code': charnum}

    r = s.get("http://muonline.hu/index.php", params=payload)
    r.encoding = 'ISO-8859-2'

    stats = pd.read_html(r.content)
    stats = stats[6]
    stats = stats.drop(columns=[2,3])
    stats = stats.drop([0], axis=0)

    level = int(stats[1][1])

    if not level == 400:
        print("The character's level is below 400.")
    else:
        post_fields = {
            'ps_str': '',
            'ps_agi': '',
            'ps_vit': '',
            'ps_ene': '',
            'ps_newcharname': '',
            'ps_reset': 'on',
            'Submit.x': '56',
            'Submit.y': '7'
        }

        r = s.post(r.url, data=post_fields)
        r.encoding = 'ISO-8859-2'

        if "reszetelve!" in r.text:
            print("Character successfully reseted.\n\n")
        else:
            print("Some kind of error occured during the reset process.")

def addStats(charnum):
    charnum += 40

    payload = {'mod': '256', 'code': charnum}

    r = s.get("http://muonline.hu/index.php", params=payload)
    r.encoding = 'ISO-8859-2'

    stats = pd.read_html(r.content)
    stats = stats[6]
    stats = stats.drop(columns=[2,3])
    stats = stats.drop([0], axis=0)

    points = int(stats[1][6])
    cclass = stats[1][2]

    if points > 0:
        print('Points to add:', points)
        print('Character class:', cclass)

        if cclass == 'DK' or cclass == 'BK' or cclass == 'BM':
            t_str = int(points * 0.7)
            points -= t_str

            t_agi = int(points * 0.9)
            t_ene = int(points * 0.1)
            points -= (t_agi + t_ene)

            t_vit = points
            points = 0
        elif cclass == 'DW' or cclass == 'SM' or cclass == 'GM':
            t_str = 500
            points -= t_str

            t_agi = int(points * 0.3)
            t_ene = int(points * 0.69)
            t_vit = int(points * 0.01)

            points -= (t_agi + t_ene + t_vit)
            t_ene += points

            points = 0
        elif cclass == 'Sum' or cclass == 'BSum' or cclass == 'DimM':
            t_str = 500
            points -= t_str

            t_agi = int(points * 0.65)
            t_ene = int(points * 0.35)
            points -= (t_agi + t_ene)

            t_vit = points
            points = 0
        elif cclass == 'MG' or cclass == 'DM':
            t_str = int(points / 3)
            t_agi = int(points / 3)
            t_ene = int(points / 3)
            points -= (t_str + t_agi + t_ene)

            t_vit = points
            points = 0
        else:
            print('Character class not (yet) supported.')

        print("\t+ STR:", t_str)
        print("\t+ AGI:", t_agi)
        print("\t+ ENE:", t_ene)
        print("\t+ VIT:", t_vit)

        post_fields = {
            'ps_str': t_str,
            'ps_agi': t_agi,
            'ps_ene': t_ene,
            'ps_vit': t_vit,
            'ps_newcharname': '',
            'ps_reset': 'off',
            'Submit.x': '56',
            'Submit.y': '7'
        }

        r = s.post(r.url, data=post_fields)
        r.encoding = 'ISO-8859-2'

        print('\nPoints added accordingly to the character class.')
    else:
        print('The selected character has no points to add.')

def charInfo(charnum):
    charnum += 40

    payload = {'mod': '256', 'code': charnum}

    r = s.get("http://muonline.hu/index.php", params=payload)
    r.encoding = 'ISO-8859-2'

    stats = pd.read_html(r.content)
    stats = stats[6]
    stats = stats.drop(columns=[2,3])
    stats = stats.drop([0], axis=0)

    print(print(tabulate(stats, showindex="never", tablefmt="fancy_grid")))

# Main
clear()

print('Welcome to MuOnline-RR.')

if config['User']:
    username = config['User']['Username']
    password = config['User']['Password']

else:
    print('To get started, we\'ll need your username and password')

    username = input('\n\nPlease enter your username: ')
    password = getpass.getpass('Please enter your password: ')

clear()

print('Trying to log into muonline.hu using the proivded credentials...')

while True:
    login(username, password)
    
    clear()

    print('Found Utopia characters:\n')
    printCharacters(characters)

    print('\n\nAvailable tasks are the following:')
    print('1) - Reset character')
    print('2) - Add stats')
    print('3) - Reset & add stats')
    print('4) - Display character info')
    print('\n0) - Quit')

    task = int(input('\n\nPlease select a task: '))

    if task == 1:
        characternum = int(input('Please select which character (1-5): '))
        clear()
        reset(characternum - 1)
    elif task == 2:
        characternum = int(input('Please select which character (1-5): '))
        clear()
        addStats(characternum - 1)
    elif task == 3:
        characternum = int(input('Please select which character (1-5): '))
        clear()
        reset(characternum - 1)
        addStats(characternum - 1)
    elif task == 4:
        characternum = int(input('Please select which character (1-5): '))
        charInfo(characternum - 1)
        input()
    elif task == 0:
        quit()
    else:
        print('That\'s not a valid task.')
        input()

# Keep window open
input()
