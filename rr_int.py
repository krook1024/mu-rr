# Imports
import os
import getpass
import requests
import pandas as pd

# Figlet
from pyfiglet import Figlet
f = Figlet(font='slant')

def drawFig():
	print(f.renderText('     Mu-RR'))

# User settings

karakter = ''
username = ''
password = ''

# Main

os.system("cls")
drawFig()

username = input("[!] Kérem a felhasználónevet: ")
password = getpass.getpass("[!] Kérem a jelszavat: ")
karakter = input("[!] Kérem a karakternevet: ")

print("[!] A Mu-RR indítása", karakter, "nevű karakter használatával...")

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

	print("[!] Talált Utopia karakterek:")

	if karik[karik[1].str.contains(karakter)].empty == True:
		print("[!] Hiba történt. Nincs ilyen karaktered az Utopia szerveren, vagy a webszerver nem válaszol.")
		quit()

	i = -1
	listaszam = 0

	for x, y in zip(karik[1], karik[2]):
		i += 1
		if x == karakter:
			print("   [x]\t", x, "[", y + " RR ]")
			listaszam = i
		else:
			print("\t", x, "[", y + " RR ]")

	listaszam += 40

	print("\n[!] Kiválasztott karakter listaszáma:", listaszam)

	get_fields = {'mod': '256', 'code': listaszam}

	r = s.get("http://muonline.hu/index.php", params=get_fields)
	r.encoding = 'ISO-8859-2'

	html = r.content
	kariadatok = pd.read_html(html)
	kariadatok = kariadatok[6]
	kariadatok = kariadatok.drop(columns=[2,3])
	kariadatok = kariadatok.drop([0], axis=0)
	print('[!] Karakter adatai:')
	
	# debug:
	# print(kariadatok)

	for x, y in zip(kariadatok[0], kariadatok[1]):
		print("\t -", x, y)

	szint = int(kariadatok[1][1])

	should_reset = False

	if not szint == 400:
		print("\n[!] Figyelmeztetés: A karakter szintje nem 400. Nem lehet így reszetelni.")
		should_reset = False
		#quit()
	else:
		should_reset = True

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

	if should_reset:
		r = s.post(r.url, data=post_fields)
		r.encoding = 'ISO-8859-2'

	#print("\n\n", r.text.split('<!-- Page Content -->')[1].split('<!-- Page Footer -->')[0], "\n\n")

	if "reszetelve!" in r.text and should_reset:
		print("[!] Karakter reszetelve!")
	else:
		if should_reset:
			print("[!] Hiba a reszetelés során! Valószínűleg nem járt le az 1 perces timeout még.")

	html = r.content
	kariadatok = pd.read_html(html)
	kariadatok = kariadatok[6]
	kariadatok = kariadatok.drop(columns=[2,3])
	kariadatok = kariadatok.drop([0], axis=0)
	#print(kariadatok)

	pontok = int(kariadatok[1][6])
	kaszt = kariadatok[1][2]

	if pontok > 0:

		print("[!] Osztás folyamatban:")
		print("\t> Elosztható pontok:", pontok)
		print("\t> Kaszt:", kaszt)

		if kaszt == 'GM' or kaszt == 'SM':
			t_str = 1000
			pontok += -1000

			t_ene = int(pontok * 0.5)
			t_agi = int(pontok * 0.5)

			pontok -= (t_ene + t_agi)

			t_vit = pontok
			pontok = 0
		elif kaszt == 'BSum' or kaszt == 'DimM':
			t_str = 1000
			pontok -= 1000

			t_ene = int(pontok * 0.3)
			t_agi = int(pontok * 0.7)

			pontok -= (t_ene + t_agi)

			t_vit = pontok
			pontok = 0
		else:
			t_str = int(pontok/3)
			t_ene = int(pontok/3)
			t_agi = int(pontok/3)
			t_vit = 0
			pontok = 0

		print("\tSTR:", t_str)
		print("\tAGI:", t_agi)
		print("\tENE:", t_ene)
		print("\tVIT:", t_vit)

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

		html = r.content
		kariadatok = pd.read_html(html)
		kariadatok = kariadatok[6]
		kariadatok = kariadatok.drop(columns=[2,3])
		kariadatok = kariadatok.drop([0], axis=0)
		
		print("[!] Pontok elosztva!")
	else:
		print("[!] Nincs elosztható pont! A program kilép...")

	# TODO: rrelés
	# x karakter link megtalálása
	# x post request arra a címre amit találtunk
	# x ha "karakter reszetelve" stringet megtaláljuk akkor PONTOK elosztása
	# x ha nem, akkor tudjuk a usert hogy nem sikerült
	# 
	# TODO: pontok elosztása
	# x összes pont megtalálása
	# x százalékosan elosztás
	# x post request ugyanarra a linkre, pontok elosztása...
else:
	print("[!] Hiba: A szerver nem válaszol...")
		
input()