'''
This class retrieves Coronavirus data from around the world 
(and also more detailed South African data) and provides differnt 
methods for viewing and/or manipulating the data.

In short, this class retrieves international data from 
https://api.covid19api.com/summary as a JSON file and saves/cahces 
the data offline. 

The detailed South African data is retrieved from 
https://github.com/dsfsi/covid19za/tree/master/data
as csv files and it is saved/chached offline. 

Both the JSON and CSV files are updated at least every 12 hours.

'''

import csv
import io
from urllib.request import Request, urlopen
import json
from urllib.error import HTTPError
from cachetools import cached, TTLCache
import datetime
import COVID19Py
import os
from datetime import *
from shutil import copyfile
import requests 



class Cov():

	global allcountries
	allcountries=[]

	global recovered
	recovered = 'recovered'
	global cases
	cases = 'cases'
	global deaths
	deaths = 'deaths'	

	global prov_data
	prov_data = []

	global prov_tmp
	prov_tmp = prov_data

	global data_dict
	data_dict = {}
	
	global headers
	headers = []

	global dict1
	dict1 = {}

	global list1
	list1 = []

	global from_another
	from_another = COVID19Py.COVID19()

	global reader_death

	cache = TTLCache(maxsize=100, ttl=3600)

	'''
	Default source is specified below, feel free to change this using the provided method
	not wise to hard code the source? Feel free to advise on this.
	Source can be changed using changeSrc() but the fromat of the new data may be an issue
	'''
	# cache = TTLCache(maxsize=100, ttl=14400)  # 2 - let's create the cache object.
	# @cached(cache)
	def __init__(self, src='https://interactive-static.scmp.com/sheet/wuhan/viruscases.jsonasd'):
		self.src = src
		self.getData(src)

	#doesn't work
	def changeSrc(self, src):
		self.src=src
		return self.getData(src)

	# @cached(cache)
	def getData(self, src):	
		
		'''
		This block checks when last the external/international
		data was updated, if 12 or more hours have lapsed, new data 
		will be retrieved. One back up of the data will be 
		created before every update / retrieval of new data.	
		'''

		url ='https://api.covid19api.com/summary'

		try:
		    mtime = os.path.getmtime('external_countries.json')
		except OSError:
		    mtime = 0
		last_modified_date = datetime.fromtimestamp(mtime)

		timedlt = datetime.now()-last_modified_date
		reader_death = []
		if timedlt >  timedelta(hours=12):
			r = requests.get(url)

			try:
				copyfile('external_countries.json','external_countries_arc.json')
			except FileNotFoundError:
				pass
			
			with open('external_countries.json', 'wb') as source:
			    source.write(r.content)

		try:
			with open('external_countries.json') as json_file: 
			    data = json.load(json_file) 
		except ValueError:
			with open('external_countries_arc.json') as json_file: 
			    data = json.load(json_file)
			    
		global allcountries 
		allcountries = data['Countries']
		for i in range(len(allcountries)):

			allcountries[i] = {k.lower(): v for k, v in allcountries[i].items()}
			k = allcountries[i]['date'].split('T')
			allcountries[i]['date'] = datetime.strptime(k[0], '%Y-%m-%d').strftime('%m-%d-%Y')

		global recovered
		recovered = 'totalrecovered'
		global cases
		cases = 'totalconfirmed'
		global deaths
		deaths = 'totaldeaths'	

		#---------------------------------
		'''
		The next two blocks will check when last the local data was updated, 
		if 12 or more hours have lapsed, new data will be retrieved.
		One back up of the local data will be created before every
		update / retrieval of new data.	
		'''



		url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_confirmed.csv"
		
		global prov_data

		try:
		    mtime = os.path.getmtime('prov_confirmed.csv')
		except OSError:
		    mtime = 0
		last_modified_date = datetime.fromtimestamp(mtime)

		timedlt = datetime.now()-last_modified_date

		if timedlt >  timedelta(hours=12):
			r = requests.get(url)
		
			try:
				copyfile('prov_confirmed.csv','prov_confirmed_arc.csv')
			except FileNotFoundError:
				pass
			
			with open('prov_confirmed.csv', 'wb') as f:
			    f.write(r.content)

		webpage = open('prov_confirmed.csv','r')
		datareader = webpage.readlines()
		q = list(datareader)
		for i in q:
			ma = i.split(",",len(q))
			d = ma[len(ma)-1]

			ma[len(ma)-1] = ma[len(ma)-1].split('\n')[0]

			prov_data.append(ma)

		if [] in prov_data:
			del prov_data[prov_data.index([])]
		# print('prov_data', prov_data,'\n')
		global prov_tmp
		prov_tmp = prov_data
		
		global headers
		headers = prov_tmp.pop(0)


				#-------------------------------
				# Deaths data

		reader_death = []
		url = "https://raw.githubusercontent.com/dsfsi/covid19za/master/data/covid19za_provincial_cumulative_timeline_deaths.csv"

		try:
		    mtime = os.path.getmtime('covid19za_provincial_cumulative_timeline_deaths.csv')
		except OSError:
		    mtime = 0
		last_modified_date = datetime.fromtimestamp(mtime)

		timedlt = datetime.now()-last_modified_date
		if timedlt >  timedelta(hours=12):
			r = requests.get(url)
			print('ke ka mo nna')
			try:
				copyfile('covid19za_provincial_cumulative_timeline_deaths.csv','covid19za_provincial_cumulative_timeline_deaths_arc.csv')
			except FileNotFoundError:
				pass
			
			with open('covid19za_provincial_cumulative_timeline_deaths.csv', 'wb') as f:
			    f.write(r.content)

		webpage = open('covid19za_provincial_cumulative_timeline_deaths.csv','r')
		datareader = webpage.readlines()
		q = list(datareader)
		for i in q:
			ma = i.split(",",len(q))
			d = ma[len(ma)-1]

			ma[len(ma)-1] = ma[len(ma)-1].split('\n')[0]

			reader_death.append(ma)


		return allcountries, prov_data, prov_tmp,


	#Returns a list of all the cases by provice since the day of first case.
	def getProvFull(self):
		global prov_data
		global prov_tmp
		prov_tmp = prov_data
		global headers
		global dict1

		global list1

		for row in prov_tmp:
			dict1 = {}
			for i in headers:
				dict1[i] = row[headers.index(i)]
			list1.append(dict1)
		return list1

	#Returns a dict containing all latest info, separated into provinces.
	# @cached(cache)
	def getProvLate(self):

		latest_prov= {}
		for i in range(len(headers)-1):
			latest_prov[headers[i+1].lower()] = prov_data[len(prov_data)-1][i+1]
		del latest_prov['source']
		return latest_prov


	#returns total numeber of confirmed cases for a province. Use province code ie: gp,ec,kzn...
	def getProvTot(self, prov):
		return self.getProvLate().get(prov)


	#returns list with dict objects containing death timeline.
	def getProvDeaths(self):
		headers = reader_death.pop(0)
		dict1 = {}
		gdeaths = []
		for row in reader_death:
			dict1 = {}
			for i in headers:
				dict1[i] = row[headers.index(i)]
			gdeaths.append(dict1)		
		return gdeaths
	

	'''
	This method returns a dict containing all the 
	available data about any country that is parsed 
	Returns None if country is not found
	'''
	# @cached(cache)
	def getCountry(self,country):	
		for i in range(len(allcountries)-1):
			if allcountries[i]['country'].lower()==country.lower():
				return allcountries[i]
		return None

	'''
	This method returns a dict containing all the 
	available data about any continet that is parsed 
	Check 'external_countries.json' for correct continent names
	'''
	# @cached(cache)
	def getContinent(self,continent):
		continent_data = []
		for i in range(len(allcountries)):
			if allcountries[i]['continent'].lower()==continent.lower():
				continent_data.append(allcountries[i])
		return continent_data


	'''
	The following getCases, getDeaths and getRecoveries methods
	each return the total confirmed cases, deahths and recoveries respectively
	for given country. 
	Check 'external_countries.json' for correct country names and codes.
	'''
	# @cached(cache)
	def getCases(self,country):
		global cases

		if country.lower() == 'south africa': #and t == cases:	
			return self.getSouthy()
		else: 
			return self.getCountry(country)[cases]

	def getDeaths(self,country):
		return self.getCountry(country)[deaths]

	def getRecoveries(self, country):
		return self.getCountry(country)[recovered]

	'''
	Returns active number of cases. 
	ie: total tested positive minus number recovered minus number of deaths
	'''
	# @cached(cache)
	def getActCases(self,country):
		return int(self.getTotal(country))- int(self.getDeaths(country))- int(self.getRecoveries(country))



	#Returns list [Date of changes, num new cases, num new recoveries, num new deaths]
	# @cached(cache)
	def getNew(self, country):
		# cntry = self.getCountry(country)
		return self.getCountry(country)['date'], self.getCountry(country)['newconfirmed'], self.getCountry(country)['newrecovered'], self.getCountry(country)['newdeaths']
  


	#Returns all recorded cases, same as calling getCases(country, t=0)
	# @cached(cache)
	def getTotal(self, country):
		if country.lower() == 'south africa':
			return self.getSouthy()
		try:	
			return self.getCases(country.lower())['totalconfirmed']
		except KeyError:
			return self.getCases(country.lower())['total']

	'''
	Someone please taka a look at this, I might be going crazy or there 
	may actually be something wrong with this method. It is supposed to
	return data for a date parsed in as a string. However, something 
	blocks it from returning the correct data for dates after 20-03-2020.
	'''
	# @cached(cache)
	def getByDate(self, date):
		list1 = self.getProvFull()
		last_row = list1[len(list1)-1]
		prev = list1[0]
		try:
			for i in list1:
				if date > last_row['YYYYMMDD']:
					return last_row

				elif (date == i['date'] or date == i['YYYYMMDD']):
					return i

				elif (date < i['date'] or date < i['YYYYMMDD'] and date > prev['YYYYMMDD']):

					return "prev",date, prev
				else:
					pass
				prev = i
		except KeyError:
			return "wtf"

	#returns value of total confirmed cases for south africa.
	def getSouthy(self):
		a = self.getProvLate()
		a = a.get('total')
		return a
		