#testng the methods in Cov.py 
#a lot of debugging code in here.

from __future__ import print_function
import Cov
from urllib.request import Request, urlopen
import json
import time

a = time.time()

c = Cov.Cov()
country = 'south africa'


# c.getData('https://api.covid19api.com/summary')
# [print(line,'\nends',100* '--','\n') for line in c.getData('https://api.covid19api.com/summary')]
# print("1",c.getData('https://api.covid19api.com/summary'),'\n')
# print('2',c.getNew(country),'\n')
# print('3',c.getCases(country),'\n')
# print('4',c.getTotal(country),'\n')
# print('0',c.getProvFull(),'\n')
print('\n5',c.getByDate('20200425'),'\n')
# print('6',c.getProvTot('lp'),'\n')
# print('7', c.getProvLate(),'\n')
# print('8', c.getCountry('afghanistan'))
# # c.getProvFull()
# # w = c.getProvFull()
# # for i in range(len(w)): print(w[i])

# print('9',c.getProvDeaths())

b = time.time()
print(b-a)

