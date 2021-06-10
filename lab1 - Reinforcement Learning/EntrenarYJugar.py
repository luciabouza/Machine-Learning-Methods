"""
Funciones para Entrenar y realizar partidas 
"""

from Jugador import Jugador
from GeneradorExperimentos import experimento
from SistemaDePerformance import GenerarHistoriaDeJuego
from Critic import generarEjemplosDeEntrenamiento
from Generalizador import lmsWeightUpdate
import matplotlib.pyplot


def train(cantidadDeJugadasParaEntrenar, alpha, jugadorQueAprende, Parte):
    PartidasGanadasRojas, PartidasGanadasNegras, PartidasEmpatadas, SumErrorCuadratico = 0,0,0,0
    coeficientesRojo, coeficientesNegro = [0.5,0.5,0.5,0.5,0.5],[0.5,0.5,0.5,0.5,0.5]
    vector_SumErrorCuadratico = []
    Rojo = Jugador('Rojo', coeficientesRojo)
    Negro = Jugador ('Negro', coeficientesNegro)
 
    #PARTE BI: entreno con jugador aleatorio
    if (Parte == 'BI'):      
        for CantidadDeJuegos in range(cantidadDeJugadasParaEntrenar):		
            # generador experimentos
            experiment = experimento(Rojo, Negro)
            SumErrorCuadratico = 0
    		
    		# Sistema de performance
            HistoriaDeJuego = GenerarHistoriaDeJuego(experiment, Negro, Rojo,'aleatorio', jugadorQueAprende)
            
            # actualizo contadores de resultados
            if (len(HistoriaDeJuego)==0): PartidasGanadasNegras +=1 #en el primer movimiento gana el negro y quien aprende es el rojo
            elif (HistoriaDeJuego[-1].EsGanador(Rojo)): PartidasGanadasRojas +=1
            elif (HistoriaDeJuego[-1].EsGanador(Negro)): PartidasGanadasNegras +=1
            else: PartidasEmpatadas +=1
    					
            # Critic y Generalizador              
            if jugadorQueAprende=='Rojo':
                EjEntrenamiento = generarEjemplosDeEntrenamiento(Rojo, Negro, HistoriaDeJuego, jugadorQueAprende)
                Rojo.coeficientes, SumErrorCuadratico = lmsWeightUpdate(Rojo.coeficientes,alpha, EjEntrenamiento)
            else:
                EjEntrenamiento = generarEjemplosDeEntrenamiento(Negro, Rojo, HistoriaDeJuego, jugadorQueAprende)
                Negro.coeficientes, SumErrorCuadratico = lmsWeightUpdate(Negro.coeficientes,alpha, EjEntrenamiento)    
           
            if(len(EjEntrenamiento)>0):
                vector_SumErrorCuadratico.append(SumErrorCuadratico)
    
    
    #PARTE BII: entreno con jugador al que le voy pasando conocimiento
    if (Parte == 'BII'):
        TiempoParaPasarCoeficientes = 50
        contador = 0
        
        for CantidadDeJuegos in range(cantidadDeJugadasParaEntrenar):		
            # generador experimentos
            experiment = experimento(Rojo, Negro)
            SumErrorCuadratico = 0
    		
    		# Sistema de performance
            HistoriaDeJuego = GenerarHistoriaDeJuego(experiment, Negro, Rojo, 'jugAnterior', jugadorQueAprende)
            
            # actualizo contadores de resultados
            if (len(HistoriaDeJuego)==0): PartidasGanadasNegras +=1 #en el primer movimiento gana el negro y quien aprende es el rojo
            elif (HistoriaDeJuego[-1].EsGanador(Rojo)): PartidasGanadasRojas +=1
            elif (HistoriaDeJuego[-1].EsGanador(Negro)): PartidasGanadasNegras +=1
            else: PartidasEmpatadas +=1
    					
    		# Critic y Generalizador       
            contador += 1
            if jugadorQueAprende=='Rojo':
                EjEntrenamiento = generarEjemplosDeEntrenamiento(Rojo, Negro, HistoriaDeJuego, jugadorQueAprende)
                Rojo.coeficientes, SumErrorCuadratico = lmsWeightUpdate(Rojo.coeficientes,alpha, EjEntrenamiento)
                if contador == TiempoParaPasarCoeficientes:
                   Negro.coeficientes = Rojo.coeficientes.copy()
                   contador = 0
            else:
                EjEntrenamiento = generarEjemplosDeEntrenamiento(Negro, Rojo, HistoriaDeJuego, jugadorQueAprende)
                Negro.coeficientes, SumErrorCuadratico = lmsWeightUpdate(Negro.coeficientes,alpha, EjEntrenamiento)   
                if contador == TiempoParaPasarCoeficientes:
                   Rojo.coeficientes = Negro.coeficientes.copy()
                   contador = 0
            
            if(len(EjEntrenamiento)>0):
                vector_SumErrorCuadratico.append(SumErrorCuadratico)
    		
    # imprimo estadísticas
    print("Juegos ganados por ROJO:  " + str(PartidasGanadasRojas))
    print("Juegos ganados por NEGRO:  " + str(PartidasGanadasNegras))
    print("Juegos empatados: " + str(PartidasEmpatadas))     
    print("Suma Error cuadrático: " + str(sum(vector_SumErrorCuadratico)))
    print("Grafica Error Cuadrático  ")  
    matplotlib.pyplot.plot(range(0,len(vector_SumErrorCuadratico)), vector_SumErrorCuadratico)
    
    #devuelvo coeficientes
    Coef = []
    if (jugadorQueAprende == 'Rojo'):Coef = Rojo.coeficientes.copy()
    else: Coef = Negro.coeficientes.copy()
    return(Coef)
   
    
# ejecución de un juego entre los dos
def JugarPartida(experimento,jugadorRojas, jugadorNegras):	
    JuegoFinalizado = False
    cantidadJugadas = 0
    TableroIntermedio = experimento.tablero.copy()
    turno = 'Negro'
    while(JuegoFinalizado != True):
        if (turno == 'Negro'):
            TableroIntermedio = jugadorNegras.Movimiento(TableroIntermedio)
            turno = 'Rojo'
            cantidadJugadas +=1
        else:
            TableroIntermedio = jugadorRojas.Movimiento(TableroIntermedio)
            turno = 'Negro'
            cantidadJugadas +=1
        if(TableroIntermedio.EsGanador(jugadorNegras)):
            return 1
        if TableroIntermedio.EsGanador(jugadorRojas): 
            return -1 
        if (cantidadJugadas==200):
            return 0
 
       
def Jugar(CoeficientesRojo, CoeficientesNegro, cantPartidas):    
    JugadorRojo = Jugador('Rojo', CoeficientesRojo)
    JugadorNegro = Jugador ('Negro', CoeficientesNegro)
    PartidasGanadasRojo, PartidasGanadasNegro, PartidasEmpatadas = 0,0,0
    
    for i in range (cantPartidas):
        experiment = experimento(JugadorRojo,JugadorNegro)
        resultado = JugarPartida(experiment, JugadorRojo,JugadorNegro)
        if resultado == -1: PartidasGanadasRojo += 1
        if resultado == 1: PartidasGanadasNegro += 1
        if resultado == 0: PartidasEmpatadas += 1
        
    print("Juegos ganados por Jugador Rojo:  " + str(PartidasGanadasRojo))
    print("Juegos ganados por Jugador Negro:  " + str(PartidasGanadasNegro))
    print("Juegos empatados: " + str(PartidasEmpatadas))

