#!/usr/bin/python2.6
# -*- coding: latin-1 -*-

"""Copyright (C) 2011 by Daniel Guerrero (chancleta at gmail dot com)

Code based on: 
http://www.instructables.com/id/Twitter-Mood-Light-The-Worlds-Mood-in-a-Box/
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Daniel Guerrero' 

import urllib2
from animolib import *
import json
from datetime import datetime, date, time
import time as _time
import serial


AMOR_QUERY = '\"te+quiero+mucho\"+OR+\"te+quiero+más\"+OR+\"amo+tanto\"+OR+\"amo+tanto\"+OR+\"todo+mi+amor\"+OR+\"muy+enamorado\"+OR+\"tan+enamorada\"'
IRA_QUERY='\"te+odio\"+OR+\"siento+rabia\"+OR+\"le+odio\"+OR+\"estoy+furioso\"+OR+\"estoy+furiosa\"+OR+\"crispado\"+OR+\"estoy+cabreado\"'
ALEGRIA_QUERY='\"mas+feliz\"+OR+\"bastante+feliz\"+OR+\"tan+feliz\"+OR+\"muy+feliz\"+OR+\"gozo\"+OR+\"júbilo\"+OR+\"deleite\"+OR+\"alborozo\"+OR+\"juerga\"'
SORPRESA_QUERY='\"no+me+lo+puedo+creer\"+OR+\"increible\"+OR+\"asombro\"+OR+\"me+ha+sorprendido\"+OR+\"te+ha+sorprendido\"+OR+\"cogido+por+sorpresa\"'
ENVIDIA_QUERY='\"ambiciono\"+OR+\"codicio\"+OR+\"mucha+envidia\"+OR+\"yo+quiero+ser\"+OR+\"por+que+no+puedo\"+OR+\"envidio\"+OR+\"celoso\"'
TRISTEZA_QUERY='\"muy+triste\"+OR+\"tan+deprimido\"+OR+\"estoy+llorando\"+OR+\"tengo+el+corazón+roto\"+OR+\"estoy+triste\"\"+OR+\"me+quiero+morir\"'
MIEDO_QUERY='\"muy+asustado\"+OR+\"tan+asustada\"+OR+\"realmente+asustado\"+OR+\"terrorifico\"+OR+\"tanto+temor\"+OR+\"horror\"+OR+\"aterrozizado\"'

#diccionario para almacenar las querys asociadas al animoID
query_dict = {
0:AMOR_QUERY,
1:ALEGRIA_QUERY,
2:SORPRESA_QUERY,
3:IRA_QUERY,
4:ENVIDIA_QUERY,
5:TRISTEZA_QUERY,
6:MIEDO_QUERY
}

def time_string_to_stamp(date_string):
	#tweeter is using UTC!
	dt = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S +0000")
	tt = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.weekday(), 0, -1)
	stamp = _time.mktime(tt)
	return stamp

def parse_tps(animoID):
	print 'query_dict[animoID]= '+query_dict[animoID]
	#query can be done either json or atom
	base_url='http://search.twitter.com/search.json?q='+query_dict[animoID]+'&rpp=30&locale=es&result_type=recent'
	f = urllib2.urlopen(base_url)
	a = json.loads(f.read())
	#debug
	#todo keep the msg if somethings happens
	#b = json.dumps(a, sort_keys=True, indent=4)
	first_tw_time = a['results'][0]['created_at']
	last_tw_time= a['results'][29]['created_at']
	tstart = time_string_to_stamp(first_tw_time)
	tend = time_string_to_stamp(last_tw_time)
	tps = 30 / (tstart - tend)
	return tps
	
def setcolor(animoID):
	ser = serial.Serial('/dev/ttyACM0')
	print ser.portstr  # check which port was really used
	print 'writing animoID to LED='+str(animoID)
	ser.write(str(animoID))      # write a string
	ser.close()
	
def main():
	c = AnimodelMundo(0.4,0.05,2,4,[0.1,0.1,0.1,0.1,0.1,0.1,0.1],'None')
	while True:
		#rellenando todos los tps
		for animoID in range(NUM_TIPOS_ANIMO):
			tps = parse_tps(animoID)
			#trabajemos con tweets por minuto
			tpm = tps * 60
			c.registrar_tweets(animoID,tpm)
			c.calcula_animo_actual()
			c.calcula_intensidad_animo_actual()
		print 'timestamp: '+str(_time.time())+' setting colorid '+str(c.ANIMO_MUNDIAL)
		setcolor(c.ANIMO_MUNDIAL)
		_time.sleep(60)
	return 0

if __name__ == '__main__':
	main()
