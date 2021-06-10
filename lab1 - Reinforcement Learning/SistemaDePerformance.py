# -*- coding: utf-8 -*-
"""
toma como entrada en experimento (aquí siempre un nuevo tablero con posiciones aleatorias, sin ser tablero final) 
Como salida da la historia del juego, que es una lista de tableros que representan el total del juego entre dos jugadores
"""

def GenerarHistoriaDeJuego(experimento, jugadorNegras, jugadorRojas, entrenamiento, jugadorqueAprende):	
    HistoriaDeJuego = []
    JuegoFinalizado = False
    cantidadJugadas = 0
    TableroIntermedio = experimento.tablero.copy()
    turno = 'Negro' #siempre comienza jugador negro
    
    #cargo en Historia de Juego los Tableros correspondientes a cada movimiento.
    # dependiendo el turno, y cual sea eel tipo de entrenamiento elijo los diferentes metodos de movimiento
    while(JuegoFinalizado != True):
        if (turno == 'Negro'):
            if (jugadorqueAprende == 'Negro') or (entrenamiento != 'aleatorio'):
                TableroIntermedio = jugadorNegras.Movimiento(TableroIntermedio)
                HistoriaDeJuego.append(TableroIntermedio)
            else:
                TableroIntermedio = jugadorNegras.MovimientoAleatorio(TableroIntermedio)
            turno = 'Rojo'
            cantidadJugadas +=1
        else:
            if (jugadorqueAprende == 'Rojo') or (entrenamiento != 'aleatorio'):
                TableroIntermedio = jugadorRojas.Movimiento(TableroIntermedio)
                HistoriaDeJuego.append(TableroIntermedio)
            else:
                TableroIntermedio = jugadorRojas.MovimientoAleatorio(TableroIntermedio)  
            turno = 'Negro'
            cantidadJugadas +=1
        
        if(TableroIntermedio.EsGanador(jugadorNegras) or 
           TableroIntermedio.EsGanador(jugadorRojas) or 
           (cantidadJugadas==200)):
            JuegoFinalizado = True   
     			             
    return(HistoriaDeJuego)	
