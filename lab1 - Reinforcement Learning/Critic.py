# -*- coding: utf-8 -*-
"""
en este modulo se genera una lista con los ejemplos de entrenamiento. 
Un ejemplo de entrenamiento es un par <X, Ventrenamiento(X)>
Los ejemplos de entrenamiento se obtienen a partir de una Historia de Juego, 
valorando los tableros de la partida a partir de los tableros sucesores y de los coeficientes conocidos hasta el momento. 
"""


def generarEjemplosDeEntrenamiento(jugador,contrincante, HistoriaDeJuego, jugadorQueAprende):
        EjEntrenamiento=[]
        vectorDeXproximo, vectorDeX = [],[]
        #para que tableros intermedios tengan valores menores al tablero final
        FactorDescuento = 0.9 
        
        if (len(HistoriaDeJuego)!=0):
            for i in range(len(HistoriaDeJuego)-2):
                    vectorDeX = HistoriaDeJuego[i].SacarDatosX(jugador).copy()
                    vectorDeXproximo = HistoriaDeJuego[i+1].SacarDatosX(jugador).copy()
                    valorTechoSucesor = FactorDescuento * calcularValorTablero(jugador.coeficientes, vectorDeXproximo)  
                    EjEntrenamiento.append([vectorDeX, valorTechoSucesor])
                    #libero memoria
                    del vectorDeX
                    del vectorDeXproximo
                        
            #para el tablero penultimo y el final
            valorTableroFinal = HistoriaDeJuego[-1].calcularValorTableroFinal(jugador,contrincante)
            
            if (len(HistoriaDeJuego)>1):    
                vectorDeX = HistoriaDeJuego[-2].SacarDatosX(jugador).copy()
                EjEntrenamiento.append([vectorDeX, FactorDescuento*valorTableroFinal])
                del vectorDeX
                
            vectorDeX = HistoriaDeJuego[-1].SacarDatosX(jugador).copy()
            EjEntrenamiento.append([vectorDeX, valorTableroFinal])
            del vectorDeX   
            
        return(EjEntrenamiento)
     
def calcularValorTablero(coeficientes, vectorX):
       result =0;
       for i in range(5):
           result += vectorX[i]*coeficientes[i]
       return result