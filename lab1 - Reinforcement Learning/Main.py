# -*- coding: utf-8 -*-
"""
Código Principal, donde los jugadores juegan y aprenden. 
"""

from  EntrenarYJugar import train, Jugar


#Valores alpha (tasa de aprendizaje)      
alpha = 0.0005
cantidadEntrenamiento = 1000

#Parte BI
jugadorQueAprende = 'Negro'
coefJugadorBI = train(cantidadEntrenamiento, alpha, jugadorQueAprende, 'BI')
print(coefJugadorBI)

#Parte BII
jugadorQueAprende = 'Rojo'
coefJugadorBII = train(cantidadEntrenamiento, alpha, jugadorQueAprende, 'BII')
print(coefJugadorBII)


#Parte C
CoeficientesRojo = coefJugadorBII
CoeficientesNegro = coefJugadorBI
cantPartidas = 100
Jugar(CoeficientesRojo, CoeficientesNegro, cantPartidas)

