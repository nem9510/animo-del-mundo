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

import time as _time

class TipoAnimo:
    AMOR=0
    ALEGRIA=1
    SORPRESA=2
    IRA=3
    ENVIDIA=4
    TRISTEZA=5
    MIEDO=6
NUM_TIPOS_ANIMO = 7
	
class IntensidadAnimo:
	MEDIO=0
	CONSIDERABLE=1
	EXTREMO=2
NUM_INTENSIDADES = 3

class AnimodelMundo:
	"""Abstraccion del Animo mundial"""
	def __init__(self, factor_suavizado_emocion, factor_suavizado_animo, moderado_umbral_animo,
		extremo_umbral_animo, ratios_temperamento, all_tps):
		
			self.ANIMO_MUNDIAL = TipoAnimo.AMOR #inicializando por probar
			self.factor_suavizado_emocion = factor_suavizado_emocion
			self.factor_suavizado_animo = factor_suavizado_animo
			self.moderado_umbral_animo = moderado_umbral_animo
			self.extremo_umbral_animo = extremo_umbral_animo
			self.ratios_temperamento = ratios_temperamento #inicializando al primer temperamento
			self.ratios_animo_mundial = [-1]*NUM_TIPOS_ANIMO #list initializated to None
			self.all_tpm = [-1]*NUM_TIPOS_ANIMO #list with tweets per second per Animo
			self.animo_mundial_avg = [-1]*NUM_TIPOS_ANIMO #movig average of the world mood
			self.timestamp = 0
	
	def registrar_tweets(self, animoID, tpm):
		#debug
		self.tpm = tpm
		self.timestamp = _time.time()
		print tpm
		if (animoID < 0 or animoID > NUM_TIPOS_ANIMO or tpm < 0):
			print 'Valores incorrectos de entrada para registrar tweets'
			print 'We would not do calculations with this'
		else:
			a = self.factor_suavizado_emocion
			if (self.animo_mundial_avg[animoID] == -1):
				print 'Primera vez en el bucle'
				#not sure about below array if we'll use it or not
				self.all_tpm[animoID] = tpm
				self.animo_mundial_avg[animoID] = tpm
			else:
				#registering tpm as it is useful for preventing failures
				self.all_tpm[animoID] = tpm
				#aplicamos exponential moving averages
				print 'calculating===>'+'animo_mundial_avg='+str(self.animo_mundial_avg[animoID])+'*'+'(1 -'+str(a)+')'+'+'+str(tpm)+'*'+str(a)
				self.animo_mundial_avg[animoID] = self.animo_mundial_avg[animoID] * (1 - a) + tpm * a
				print 'timestamp: '+str(self.timestamp)+'animo_mundial_avg=='+str(self.animo_mundial_avg)
			
	def calcula_intensidad_animo_actual(self):
		#aqui calculamos como de intenso es el ánimo actual
		#get the mood ratio as a percent of the temperament ratio.
		#this will show the mood ratio as a divergence from the norm, and so is a good measure of mood intensity.
		percent = self.ratios_animo_mundial[self.ANIMO_MUNDIAL] / self.ratios_temperamento[self.ANIMO_MUNDIAL]
		if (percent > self.extremo_umbral_animo):
			print 'timestamp: '+str(self.timestamp)+' Intensidad EXTREMO con percent= '+str(percent)
			return IntensidadAnimo.EXTREMO
		elif (percent > self.moderado_umbral_animo):
			print 'timestamp: '+str(self.timestamp)+' Intensidad CONSIDERABLE con percent= '+str(percent)
			return IntensidadAnimo.CONSIDERABLE
		else:
			print 'timestamp: '+str(self.timestamp)+' Intensidad MEDIO con percent= '+str(percent)
			return IntensidadAnimo.MEDIO
		
	def calcula_animo_actual(self):
		#primero calculamos los ratios
		sum = 0
		for i in range(NUM_TIPOS_ANIMO):
			print 'self.animo_mundial_avg['+str(i)+']='+str(self.animo_mundial_avg[i])
			sum += self.animo_mundial_avg[i]
		for i in range(NUM_TIPOS_ANIMO):
			self.ratios_animo_mundial[i]=self.animo_mundial_avg[i]/sum
		print 'timestamp: '+str(self.timestamp)+' animo        at T'+str(self.ratios_animo_mundial)
		print 'timestamp: '+str(self.timestamp)+' temperamento at T-1'+str(self.ratios_temperamento)
		#Ahora calculamos el ánimo que se ha incrementado más como una proporción del moving average
		#find the ratio that has increased by the most, as a proportion of its moving average.
		#So that, for example, an increase from 5% to 10% is more significant than an increase from 50% to 55%.
		maxIncrease = -1
		for i in range(NUM_TIPOS_ANIMO):
			difference = self.ratios_animo_mundial[i] - self.ratios_temperamento[i]
			difference /= self.ratios_temperamento[i]
			#print "checking difference="+str(difference)
			if (difference > maxIncrease):
				maxIncrease = difference
				#este es el animo más influyente ahora mismo.
				#print 'this is the Animo mundial, ID='+str(i)
				self.ANIMO_MUNDIAL = i
				#calculating actual temperament ratio.
		
		
		#update the world temperament, as an exponential moving average of the mood.
		#this allows the baseline ratios, i.e. world temperament, to change slowly over time.
		#this means, in affect, that the 2nd derivative of the world mood wrt time is part of the current mood calcuation.
		#and so, after a major anger-inducing event, we can see when people start to become less angry.
		a = self.factor_suavizado_animo
		sum = 0
		for i in range(NUM_TIPOS_ANIMO):
			self.ratios_temperamento[i] = self.ratios_temperamento[i] * (1 - a) + self.ratios_animo_mundial[i] * a
			sum += self.ratios_temperamento[i]
		for i in range(NUM_TIPOS_ANIMO):
			self.ratios_temperamento[i]=self.ratios_temperamento[i]/sum
		print 'timestamp: '+str(self.timestamp)+' temperamento at T  '+str(self.ratios_temperamento)
		print 'timestamp: '+str(self.timestamp)+' El animo mundial es ahora: '+str(self.ANIMO_MUNDIAL)
