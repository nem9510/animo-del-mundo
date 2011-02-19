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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import io
import subprocess
from subprocess import call
import os

AMOR_QUERY = '\"te+quiero+mucho\"+OR+\"te+quiero+más\"+OR+\"amo+tanto\"+OR+\"amo+tanto\"+OR+\"todo+mi+amor\"+OR+\"muy+enamorado\"+OR+\"tan+enamorada\"'
IRA_QUERY='\"te+odio\"+OR+\"siento+rabia\"+OR+\"le+odio\"+OR+\"estoy+furioso\"+OR+\"estoy+furiosa\"+OR+\"crispado\"+OR+\"estoy+cabreado\"'
ALEGRIA_QUERY='\"mas+feliz\"+OR+\"bastante+feliz\"+OR+\"tan+feliz\"+OR+\"muy+feliz\"+OR+\"gozo\"+OR+\"júbilo\"+OR+\"deleite\"+OR+\"alborozo\"+OR+\"juerga\"'
SORPRESA_QUERY='\"no+me+lo+puedo+creer\"+OR+\"increible\"+OR+\"asombro\"+OR+\"me+ha+sorprendido\"+OR+\"te+ha+sorprendido\"+OR+\"cogido+por+sorpresa\"'
ENVIDIA_QUERY='\"ambiciono\"+OR+\"codicio\"+OR+\"mucha+envidia\"+OR+\"yo+quiero+ser\"+OR+\"por+que+no+puedo\"+OR+\"envidio\"+OR+\"celoso\"'
TRISTEZA_QUERY='\"muy+triste\"+OR+\"tan+deprimido\"+OR+\"estoy+llorando\"+OR+\"tengo+el+corazón+roto\"+OR+\"estoy+triste\"\"+OR+\"me+quiero+morir\"'
MIEDO_QUERY='\"muy+asustado\"+OR+\"tan+asustada\"+OR+\"realmente+asustado\"+OR+\"terrorifico\"+OR+\"tanto+temor\"+OR+\"que+horror\"+OR+\"aterrozizado\"'

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

emotion_dict = {
0:'AMOR',
1:'ALEGRIA',
2:'SORPRESA',
3:'IRA',
4:'ENVIDIA',
5:'TRISTEZA',
6:'MIEDO'
}

intensity_dict = {
0:'MEDIO',
1:'CONSIDERABLE',
2:'EXTREMO',
}

def time_string_to_stamp(date_string):
	#tweeter is using UTC!
	dt = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S +0000")
	tt = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.weekday(), 0, -1)
	stamp = _time.mktime(tt)
	return stamp

def parse_tps(animoID,c):
	print 'query_dict[animoID]= '+query_dict[animoID]
	#query can be done either json or atom
	base_url='http://search.twitter.com/search.json?q='+query_dict[animoID]+'&rpp=30&locale=es&result_type=recent'
	f = 0
	try:
		f = urllib2.urlopen(base_url)
	except urllib2.URLError, (err):
		print "URL error(%s)" % (err)
	if (f != 0):
		a = json.loads(f.read())
		#debug
		#todo keep the msg if somethings happens
		b = json.dumps(a, sort_keys=True, indent=4)
		first_tw_time = a['results'][0]['created_at']
		last_tw_time= a['results'][29]['created_at']
		tstart = time_string_to_stamp(first_tw_time)
		tend = time_string_to_stamp(last_tw_time)
		tps = 30 / (tstart - tend)
	else:
		print 'We shouldnt be here, as this is bad'
		#as failure we take the last value of tps, not bad :-)
		tps = c.all_tpm[animoID]
		b =''
	#returning the tweets per second and all the message just in case we have an alert
	return tps,b
	
def setserial(animoID,flash):
	ser = serial.Serial('/dev/ttyACM0')
	print ser.portstr  # check which port was really used
	print 'writing animoID to LED= '+str(animoID)
	ser.write(str(animoID))      # write a string
	if (flash == True):
		#we are using a 9 to tell arduino to flash
		#this should be changed if more colors or Moods are added.
		print "FLASHING!!"
		ser.write(str(9))
	ser.close()

def send_mail(text_msg,animoID):
	msg = {}
	msg = MIMEMultipart('alternative')
	me = ['myemail']
	them = ['youremail']
	msg['Subject'] = 'Alerta - alta intensidad para la emoción: '+str(animoID)
	msg['From'] = "myemail"
	msg['Cc'] = ''
	msg['To'] = "youremail"
	#part0 = MIMEText("default msg", 'plain') 
	part1 = MIMEText(text_msg,'plain')
	#msg.attach(part0)
	msg.attach(part1)
	s = smtplib.SMTP('localhost')
	s.sendmail(me, them, msg.as_string())
	s.close

def register_plot(all_tpm,ratios_animo_mundial,ratios_temperamento):
	print 'Writing data to tps.txt'
	f = open('./plots/all_tpm.txt', 'a')
	s =''
        t = str(_time.time())
        for i in range(NUM_TIPOS_ANIMO):
	   s += ' '+str(all_tpm[i])
        s = t + s + '\n'
	print s
	f.write(s)
	f.close
	print 'Writing data to ratios_animo.txt'
        f = open('./plots/ratios_animo.txt', 'a')
        s =''
        t = str(_time.time())
        for i in range(NUM_TIPOS_ANIMO):
           s += ' '+str(ratios_animo_mundial[i])
        s = t + s + '\n'
        print s
        f.write(s)
        f.close
        print 'Writing data to ratios_temperatmento.txt'
        f = open('./plots/ratios_temperamento.txt', 'a')
        s =''
        t = str(_time.time())
        for i in range(NUM_TIPOS_ANIMO):
           s += ' '+str(ratios_temperamento[i])
        s = t + s + '\n'
        print s
        f.write(s)
        f.close

def write_to_html(intenID,animoID):
	f = open('/home/Dropbox/Public/animo.html', 'w')
        s ="""<html> 
            <head> 
	    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/> 
	    <META HTTP-EQUIV="refresh" CONTENT="60"> 
	    </head> 
	    <body>"""
        s+= '<h3>El ánimo mundial es: '+str(emotion_dict[animoID])+' con intensidad: '+str(intensity_dict[intenID])+'</h3>'
	s+= """<img src="./all_tpm.png" alt="Emoción instantánea" /> 
	    <img src="./ratios_animo.png" alt="Animo ratio" /> 
	    <img src="./ratios_temperamento.png" alt="Temperamento ratio" />""" 
	dirList=os.listdir('/home/Dropbox/Public/alerts/')
	s+= """<table border="1">"""
	s+="""<tr><td>Alertas</td></tr>"""
	for fname in dirList:
	    print fname
            s+= '<tr><td>'+'<a href="./alerts/'+str(fname)+'">'+str(fname)+'</a>'+'</td></tr>'
        s+= """</table>
	    </body> 
	    </html>"""
	f.write(s)
	f.close

def register_alert(text_msg,animoID):
	print 'Writing data to alerts'
        f = open('/home/Dropbox/Public/alerts/alerts_'+str(emotion_dict[animoID])+'_'+str(_time.time())+'.txt', 'a')
        f.write(text_msg)
	f.close
	
def main():
	#the initial ratios can be adapted to normal mood so you dont receive alert
	#while starting the code, but otherwise is useful for testing email and flashing.
	c = AnimodelMundo(0.6,0.05,2,4,[0.18,0.18,0.35,0.04,0.06, 0.04,0.11],'None')
	msg_dict = {}
	#led will not flash unless something big happens
	while True:
		flash = False
		#rellenando todos los tps
		for animoID in range(NUM_TIPOS_ANIMO):
			tps,msg_dict[animoID] = parse_tps(animoID,c)
			#trabajemos con tweets por minuto
			tpm = tps * 60
			c.registrar_tweets(animoID,tpm)
		c.calcula_animo_actual()
		intensity = c.calcula_intensidad_animo_actual()
		register_plot(c.all_tpm,c.ratios_animo_mundial,c.ratios_temperamento)
		#actually ploting chart
		retcode = subprocess.call(["gnuplot", "./plots/animo.dat"])
		print 'returning code for ploting is= '+str(retcode)
		print "la intensidad actual es= "+str(intensity)
		write_to_html(intensity,c.ANIMO_MUNDIAL)
		if (intensity == IntensidadAnimo.EXTREMO or intensity == IntensidadAnimo.CONSIDERABLE):
				#taking tweets from right emotion to send
				msg_email = msg_dict[c.ANIMO_MUNDIAL]
				print "sending mail and flashing"
				send_mail(msg_email,c.ANIMO_MUNDIAL)
				flash = True
				register_alert(msg_email,c.ANIMO_MUNDIAL)
		print 'timestamp: '+str(_time.time())+' setting colorid '+str(c.ANIMO_MUNDIAL)
		setserial(c.ANIMO_MUNDIAL,flash)
		_time.sleep(60)
	return 0

if __name__ == '__main__':
	main()
