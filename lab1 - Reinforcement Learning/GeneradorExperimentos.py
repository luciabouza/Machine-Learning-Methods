# -*- coding: utf-8 -*-
"""
Genera un tablero inicial con las fichas de los jugadores en una posicion donde ninguno de los dos es ganador. 
No tomo en cuenta la hipótesis actual y estrategias para mejorar la performance
"""

import Tablero

class experimento():
    
    #genero un tablero inicial llamando al constructor de la clase tablero y luego inicializo
    def __init__(self, jugadorRojas, jugadorNegras):
        self.tablero = Tablero.Tablero()           
        self.tablero.inicializoPartida()      
        while (self.tablero.EsGanador(jugadorRojas) or self.tablero.EsGanador(jugadorNegras)):
            self.tablero.liberarMemoria()
            self.tablero = Tablero.Tablero() 
            self.tablero.inicializoPartida()
        