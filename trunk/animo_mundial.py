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
import time


#AMOR_QUERY = '"te quiero mucho" OR "te quiero más" OR "amo tanto" OR "amo tanto" OR "todo mi amor" OR "muy enamorado" OR "tan enamorada"'
#IRA_QUERY='"te odio" OR "siento rabia" OR "le odio" OR "estoy furioso" OR "estoy furiosa" OR "crispado" OR "estoy cabreado"'
#ALEGRIA_QUERY='"mas feliz" OR "bastante feliz" OR "tan feliz" OR "muy feliz" OR gozo OR júbilo OR deleite OR alborozo OR juerga'
#SORPRESA_QUERY='"no me lo puedo creer" OR increible OR asombro OR "me ha sorprendido" OR "te ha sorprendido" OR "cogido por sorpresa"'
#ENVIDIA_QUERY='ambiciono OR codicio OR "mucha envidia" OR "yo quiero ser" OR "por que no puedo" OR envidio OR celoso'
#TRISTEZA_QUERY='"muy triste" OR "tan deprimido" OR "estoy llorando" OR "tengo el corazón roto" OR "estoy triste" OR "me quiero morir"'
#MIEDO_QUERY='"muy asustado" OR "tan asustada" OR "realmente asustado" OR terrorifico OR "tanto temor" OR "que horror" OR aterrozizado'


AMOR_QUERY='%22te%20quiero%20mucho%22%20OR%20%22te%20quiero%20m%C3%A1s%22%20OR%20%22amo%20tanto%22%20OR%20%22amo%20tanto%22%20OR%20%22todo%20mi%20amor%22%20OR%20%22muy%20enamorado%22%20OR%20%22tan%20enamorada%22'
IRA_QUERY='%22te%20odio%22%20OR%20%22siento%20rabia%22%20OR%20%22le%20odio%22%20OR%20%22estoy%20furioso%22%20OR%20%22estoy%20furiosa%22%20OR%20%22crispado%22%20OR%20%22estoy%20cabreado%22'
ALEGRIA_QUERY='%22mas%20feliz%22%20OR%20%22bastante%20feliz%22%20OR%20%22tan%20feliz%22%20OR%20%22muy%20feliz%22%20OR%20gozo%20OR%20j%C3%BAbilo%20OR%20deleite%20OR%20alborozo%20OR%20juerga'
SORPRESA_QUERY='%22no%20me%20lo%20puedo%20creer%22%20OR%20increible%20OR%20asombro%20OR%20%22me%20ha%20sorprendido%22%20OR%20%22te%20ha%20sorprendido%22%20OR%20%22cogido%20por%20sorpresa%22'
ENVIDIA_QUERY='ambiciono%20OR%20codicio%20OR%20%22mucha%20envidia%22%20OR%20%22yo%20quiero%20ser%22%20OR%20%22por%20que%20no%20puedo%22%20OR%20envidio%20OR%20celoso'
TRISTEZA_QUERY='%22muy%20triste%22%20OR%20%22tan%20deprimido%22%20OR%20%22estoy%20llorando%22%20OR%20%22tengo%20el%20coraz%C3%B3n%20roto%22%20OR%20%22estoy%20triste%22%20OR%20%22me%20quiero%20morir%22'
MIEDO_QUERY='%22muy%20asustado%22%20OR%20%22tan%20asustada%22%20OR%20%22realmente%20asustado%22%20OR%20terrorifico%20OR%20%22tanto%20temor%22%20OR%20%22que%20horror%22%20OR%20aterrozizado'

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
        base_url='http://search.twitter.com/search.json?q='+query_dict[animoID]+'&rpp=30&lang=es&result_type=recent'
        f = 0
        try:
                f = urllib2.urlopen(base_url)
		a = json.loads(f.read())
		b = json.dumps(a, sort_keys=True, indent=4)
        except urllib2.URLError, (err):
                print "URL error(%s)" % (err)
        if (f != 0 and len(a['results']) == 30 and b != None):
                #debug
                first_tw_time = a['results'][0]['created_at']
		print "first_tw_time="+first_tw_time
                last_tw_time= a['results'][29]['created_at']
		print "last_tw_time"+last_tw_time
                tstart = time_string_to_stamp(first_tw_time)
		print "tstart="+str(tstart)
                tend = time_string_to_stamp(last_tw_time)
		print "tend="+str(tend)
                tps = 30 / (tstart - tend)
		print "tps="+str(tps)
		print "This value is stored when we get no data from twitter c.all_tpm[animoID]="+str(c.all_tpm[animoID])
        else:
                print 'We shouldnt be here, as this is bad'
                #as failure we take the last value of tps, not bad :-)
		#be careful what you are working with tps or tpm
                tps = c.all_tpm[animoID] / 60
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
        me = ['root']
        them = ['']
        msg['Subject'] = 'Alerta - alta intensidad para la emoción: '+str(animoID)
        msg['From'] = "root"
        msg['Cc'] = ''
        msg['To'] = ""
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
        content = {}
        f = open('/home/user/Dropbox/Public/animo.html', 'w')
        s ="""<html> 
            <head> 
	    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1"/> 
            <META HTTP-EQUIV="refresh" CONTENT="60"> 
            </head> 
            <body>"""
        s+= '<h3>El &aacute;nimo mundial es: '+str(emotion_dict[animoID])+' con intensidad: '+str(intensity_dict[intenID])+'</h3>'
        s+= """<img src="./all_tpm.png" alt="Emoci&oacute;n instant&aacute;nea" /> 
            <img src="./ratios_animo.png" alt="Animo ratio" /> 
            <img src="./ratios_temperamento.png" alt="Temperamento ratio" />""" 
        dirList=os.listdir('/home/user/Dropbox/Public/alerts/')
	s+= """<p> Puedes ver como he dise&ntilde;ado todo <a href="http://madremiamadremiaque.blogspot.com/2011/02/midiendo-el-animo-del-mundo.html">AQU&Iacute;</a></p>"""
        s+= """<table border="1">"""
        s+="""<tr><td>Alertas</td><td>Timestamp</td></tr>"""
	#build up directory of time stamps
        for item in dirList:
	    full_path='/home/user/Dropbox/Public/alerts/'+str(item)
	    content[item] = os.path.getmtime(full_path)
        #sort keys, based on time stamps
	items = content.keys()
	items.sort(lambda x,y: cmp(content[x],content[y]), reverse=True)
	#report items in order writing them into html table
	for item in items:
            s+= '<tr><td>'+'<a href="./alerts/'+str(item)+'">'+str(item)+'</a>'+'</td><td>'+str(time.ctime(content[item]))+'</td></tr>'
        s+= """</table>
            </body> 
            </html>"""
        f.write(s)
        f.close

def register_alert(text_msg,animoID):
        print 'Writing data to alerts'
        f = open('/home/user/Dropbox/Public/alerts/alerts_'+str(emotion_dict[animoID])+'_'+str(_time.time())+'.txt', 'a')
        f.write(text_msg)
        f.close
        
def main():
        #the initial ratios can be adapted to normal mood so you dont receive alert
        #while starting the code, but otherwise is useful for testing email and flashing.
        c = AnimodelMundo(0.6,0.05,2.5,4,[0.18,0.18,0.35,0.04,0.06, 0.04,0.11],'None')
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
                                #send_mail(msg_email,c.ANIMO_MUNDIAL)
                                flash = True
                                register_alert(msg_email,c.ANIMO_MUNDIAL)
                print 'timestamp: '+str(_time.time())+' setting colorid '+str(c.ANIMO_MUNDIAL)
                setserial(c.ANIMO_MUNDIAL,flash)
                _time.sleep(60)
        return 0

if __name__ == '__main__':
        main()

