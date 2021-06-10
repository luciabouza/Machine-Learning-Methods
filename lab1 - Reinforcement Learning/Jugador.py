# -*- coding: utf-8 -*-
"""
define la clase jugador y el metodo de movimiento en el tablero
"""

from Critic import calcularValorTablero
import numpy as np
import random

class Jugador:
    
    def __init__(self,color,coeficientes):	
        self.color = color
        self.coeficientes = coeficientes.copy()
    
    #devuelve el tabero siguiente con mejor puntaje
    def Movimiento(self, tablero): 
        Movimientos = self.PosiblesMovimientos(tablero)
        ValorMovimientos = []
        
        #calculo el valor para cada tablero siguiente posible
        for posibletablero in Movimientos:
            vectorX = posibletablero.SacarDatosX(self)
            ValorMovimientos.append(calcularValorTablero(self.coeficientes, vectorX))
        
        #si hay movimientos, inyecto azar para que no siempre elija los mejores movimientos aprendidos y explore
        if len(Movimientos)!=0:
            aleatorio = random.randrange(100)
            if (aleatorio>80): tableroElegido = Movimientos[random.randrange(len(Movimientos))]
            else:tableroElegido = Movimientos[np.argmax(ValorMovimientos)]
            return(tableroElegido)	
        else:
            raise Exception("no hay posibles movimientos")
     
        
    #devuelve un tablero Aleatorio con con un movimiento legal
    def MovimientoAleatorio(self, tablero): 
        Movimientos = self.PosiblesMovimientos(tablero)
        if len(Movimientos)!=0:
            tableroElegido = Movimientos[random.randrange(len(Movimientos))]
            return(tableroElegido)	
        else:
            raise Exception("no hay posibles movimientos")
   
    
    #devuelve una lista de posibles tableros siguientes
    def PosiblesMovimientos(self,tablero):
        Movimientos = []
        auxX = [-1, 0, 1]
        auxY = [-1, 0, 1]
        if self.color == 'Rojo':
            for ficha in range(4):
                for ax in auxX:
                    for ay in auxY:
                        #para cada ficha, me fijo si puedo moverme a una adyacente. en caso que si, agrego ese tablero como posible.
                        if ((tablero.xRojas[ficha]+ax in range(4)) and (tablero.yRojas[ficha]+ay in range(4)) and
                        not (tablero.ocupado(tablero.xRojas[ficha]+ax,tablero.yRojas[ficha]+ay))):
                            posibleTablero = tablero.copy()
                            posibleTablero.xRojas[ficha] = tablero.xRojas[ficha]+ax
                            posibleTablero.yRojas[ficha] = tablero.yRojas[ficha]+ay
                            Movimientos.append(posibleTablero)	
        if self.color == 'Negro':
            for ficha in range(4):
                for ax in auxX:
                    for ay in auxY:
                        #para cada ficha, me fijo si puedo moverme a una adyacente. en caso que si, agrego ese tablero como posible.
                        if ((tablero.xNegras[ficha]+ax in range(4)) and (tablero.yNegras[ficha]+ay in range(4)) and
                        not (tablero.ocupado(tablero.xNegras[ficha]+ax,tablero.yNegras[ficha]+ay))):
                            posibleTablero = tablero.copy()
                            posibleTablero.xNegras[ficha] = tablero.xNegras[ficha]+ax
                            posibleTablero.yNegras[ficha] = tablero.yNegras[ficha]+ay
                            Movimientos.append(posibleTablero)  				
        return(Movimientos)
    
