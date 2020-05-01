#An apologetic, half-hearted attempt at parsnig the data into an sqlite3 db.


import sqlite3
import Cov

from sqlite3 import Error

c = Cov.Cov()
country = 'south africa'

global con
global cursorObj

global entries
entries = c.getData('https://api.covid19api.com/summary')[0]


def sql_connection():
	global con
	try:

		con = sqlite3.connect('covid2.db')


		print("Connection is established: Database is created on disk")

	except Error:

		print(Error)

def sql_table(con):
	global cursorObj
	cursorObj = con.cursor()

	try:
		cursorObj.execute("""CREATE TABLE ZA (
	DAY	integer,
	RECOVERED	integer,
	DEATHS	integer,
	ACTIVE	integer,
	TOTAL	integer,
	EC	INTEGER,
	FS	INTEGER,
	GP	INTEGER,
	KZN	INTEGER,
	LP	INTEGER,
	MP	INTEGER,
	NC	INTEGER,
	NW	INTEGER,
	WC	INTEGER,
	UNKNOWN	INTEGER
			)""")

		con.commit()

	except sqlite3.OperationalError:
		pass

	# try:
	# 	cursorObj.execute("""CREATE TABLE countries(
	# 		country text,
	# 		country_code text,
	# 		total integer, 
	# 		recovered integer, 
	# 		deaths integer, 
	# 		active integer, 
	# 		day text
	# 		)""")

	# 	con.commit()

	# except sqlite3.OperationalError:
	# pass

def sql_countries():
	diff=0

	for i in range(len(entries)):
		try:
			# print(i)
			diff = entries[i].get('totalconfirmed')-entries[i].get('totalrecovered')-entries[i].get('totaldeaths')
			
			cursorObj.execute("INSERT INTO countries (country,country_code, total,recovered,deaths,active,day) VALUES(?,?,?,?,?,?,?)",
							(entries[i].get('slug'),entries[i].get('countrycode'),entries[i].get('totalconfirmed'), entries[i].get('totalrecovered'),entries[i].get('totaldeaths'), diff,''))
			con.commit()
		except KeyError:
			pass


def sql_update_countries():
	for i in range(len(entries)):
		diff = entries[i].get('totalconfirmed')-entries[i].get('totalrecovered')-entries[i].get('totaldeaths')
		data = (entries[i].get('totalconfirmed'), entries[i].get('totalrecovered'),entries[i].get('totaldeaths'), diff,entries[i]['date'],entries[i].get('slug'))
	
		cursorObj.execute(	"UPDATE countries SET total=?, recovered=?, deaths=?, active=?, day=? WHERE country=?", data)
		# cursorObj.executemany(sql_update_query, data)
		con.commit()

def sql_in_za():
	w = c.getProvFull()
	# # for i in range(len(w)): print(w[i])
	for i in w:

		# print(type(w[i]['date']))
		# e = 
		cursorObj.execute('SELECT WC FROM ZA WHERE DAY=?',(i['date'],))
		entry = cursorObj.fetchone()

		if entry is None:
			cursorObj.execute("INSERT INTO ZA (DAY, EC, FS, GP, KZN, LP, MP, NC, NW, WC, UNKNOWN, total) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
			(i['date'],i['EC'],i['FS'],i['GP'],i['KZN'],i['LP'],i['MP'],i['NC'],i['NW'],i['WC'],i['UNKNOWN'],i['total']))
			con.commit()
			print('New entry')
		else:
		    print('Entry found')



	#update
	# data = ()

	# cursorObj.execute(	"UPDATE ZA SET RECOVERD=?, DEATHS=?, ACTIVE=? WHERE DAY=?", data)
	
	# con.commit()



global z
global f
z=c.getProvLate()
f = list(z.values())
f.pop(0)
q=list(z.keys())
def sql_update_prov():
	global f
	# z = list(z.values())
	w = c.getProvFull()
	# # for i in range(len(w)): print(w[i])
	# i = w[len(w)-1]

	# print(type(w[i]['date']))
	# e = 
	cursorObj.execute('SELECT WC FROM ZA WHERE DAY=?',(c.getCountry(country)['date'],))
	entry = cursorObj.fetchone()
	print('entry', entry)
	if entry is None:

		cursorObj.execute( " UPDATE ZA SET  RECOVERED=? WHERE day=?", (c.getCountry(country)['totalrecovered'], c.getCountry(country)['date']))
		con.commit()
		print("hahaha")

	# print(len(f))
	tmp = f
	tmp.append(1)
	cursorObj.execute(	"UPDATE ZA SET  EC=?, FS=?, GP=?, KZN=?, LP=?, MP=?, NC=?, NW=?, WC=?, UNKNOWN=?, total=? WHERE day=?", tmp)
	con.commit()
	for i in c.getProvDeaths():
		data = (i['total'],i['date'])
		cursorObj.execute(	"UPDATE ZA SET DEATHS=? WHERE day=?", data)
		con.commit()





# print(z,'\n',f)
sql_connection()
sql_table(con)
sql_in_za()
# sql_update_countries()
sql_update_prov()
x = c.getSouthy()
# cursorObj.execute("INSERT INTO ZA (total,recovered,deaths,active,day) VALUES(?,?,?,?,?)",
# 					(c.getSouthy(),c.getRecoveries('south africa'), c.getDeaths('south africa'), c.getActCases('south africa'),'20-20-20'))

# con.commit()


