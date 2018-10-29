# Imports
import os
import time
import requests
import pandas as pd

# Figlet

from pyfiglet import Figlet
def drawFiglet():
	f = Figlet(font='slant')
	print(f.renderText('     Mu-RR'))

# Functions

def killMu():
	os.system("taskkill /im MuOnline.HU.exe /f")
	drawFiglet()

# Character-related info

username = ''
password = ''
karakter = ''

# Main

while True :
	os.system("cls")
	drawFiglet()

	post_fields = {
		'Username': username,
		'Password': password,
		'tr_agree': 'on',
		'account_login': 'account_login',
		'Login.x': '11',
		'Login.y': '3'
	}

	s = requests.session()
	r = s.post('https://www.muonline.hu/index.php?mod=250/flogin', data=post_fields)
	r.encoding = 'ISO-8859-2'
	rsc = r.status_code
	if rsc == 200:
		html = r.content

		karik = pd.read_html(html)
		karik = karik[7]
		karik = karik.drop([0], axis=0)

		# print(karik)

		for x, y, z in zip(karik[0], karik[1], karik[3]):
			x = x.rstrip('.')
			if(y.lower() == karakter.lower()):
				print("\t", "[" + x + "]", " - ", y, "LVL", z)
				if(int(z) > 399) :
					killMu()
			else:
				print("\t", "[" + x + "]", " - ", y, "LVL", z)
	else:
		quit()

	time.sleep(15)

input()
