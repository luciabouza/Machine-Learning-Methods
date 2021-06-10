# -*- coding: utf-8 -*-
"""
dado una lista de ejemplos de entrenamiento <X, Ventrenamiento(X)>, 
para cada uno se va aproximando la lista de coeficientes con LMS
"""

from Critic import calcularValorTablero

def lmsWeightUpdate(coeficientes,alpha, EjemplosEntrenamiento):
		#actualiza el vector de coeficioentes con LMS
        coefAux = coeficientes.copy()
        SumErrorCuadratico = 0
        for i in range(len(EjemplosEntrenamiento)-1):
            ejemploEntrenamiento = EjemplosEntrenamiento[i]
            vTecho = calcularValorTablero(coefAux, ejemploEntrenamiento[0]) 
            SumErrorCuadratico = SumErrorCuadratico + (ejemploEntrenamiento[1] - vTecho)**2
            for i in range(5):
               coefAux[i]= coefAux[i] + (alpha * (ejemploEntrenamiento[1] - vTecho) * ejemploEntrenamiento[0][i]) 
        return coefAux, SumErrorCuadratico