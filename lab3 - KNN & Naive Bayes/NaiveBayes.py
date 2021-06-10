# -*- coding: utf-8 -*-
from sklearn import model_selection, metrics, utils
import numpy as np
  
"Función auxiliar para calcular m-estimador"
def TerminoBin(columna, valor):   
    if valor in columna.value_counts().index: termino= columna.value_counts()[valor] 
    else: termino=0
    return termino

'''Función para calcular las probabilidades de los valores de las clases. usaremos m-estimador"  
"sabemos que todos los valores son 0 o 1 para los discretos, o valores entre 0 y 1 para los continuos"
"Para los continuos los dividiremos en 4 valores para calcular la probabilidad:
    - 0<= x < 0,25
    - 0,25 <= x < 0,5
    -,50 <= x < 0,75
    -,75 <= x <= 1
    '''
def NB_CalcularProbabilidades(trainset, m):
    #probabilidad de las clase salida
    cantidadSalida = trainset.Salida.value_counts()
    Psalida0=  cantidadSalida[0]/trainset.shape[0]
    Psalida1= 1-Psalida0 
    
    cols_continuas = ['Edad', 'Años_de_educación', 'Capital_ganado', 'Capital_perdido', 'Horas_por_semana']
    cols_binarias = (trainset.columns.difference(cols_continuas)).drop('Salida')
    RowsClase0 = trainset[trainset['Salida']==0]
    RowsClase1 = trainset[trainset['Salida']==1]
    
    Probabilidad={}
    
    #Probabilidad de las clases binarias
    p = 0.5
    for i in cols_binarias:
        P0DadoSalida0 = (TerminoBin(RowsClase0[i],0) + m*p ) / cantidadSalida[0] + m  
        P0DadoSalida1 =  (TerminoBin(RowsClase1[i],0) + m*p ) / cantidadSalida[1] + m
        P1DadoSalida0 = (TerminoBin(RowsClase0[i],1) + m*p ) / cantidadSalida[0] + m  
        P1DadoSalida1 = (TerminoBin(RowsClase1[i],1) + m*p ) / cantidadSalida[1] + m  
        
        Probabilidad[i]= {"P0|salida0":P0DadoSalida0, 
                          "P0|salida1":P0DadoSalida1, 
                          "P1|salida0": P1DadoSalida0, 
                          "P1|salida1": P1DadoSalida1}

    #Probabilidad de las clases continuas
    p = 0.25
    for i in cols_continuas:
        P1cuartoDadoSalida0 =  (RowsClase0[RowsClase0[i]<0.25].shape[0] + m*p ) / cantidadSalida[0] + m  
        P1cuartoDadoSalida1 =  (RowsClase1[RowsClase1[i]<0.25][i].shape[0] + m*p ) / cantidadSalida[1] + m
        P2cuartoDadoSalida0 =  (RowsClase0[(RowsClase0[i]>=0.25) & (RowsClase0[i]<0.50)][i].shape[0] + m*p ) / cantidadSalida[0] + m      
        P2cuartoDadoSalida1 =  (RowsClase1[(RowsClase1[i]>=0.25) & (RowsClase1[i]<0.50)][i].shape[0] + m*p ) / cantidadSalida[1] + m
        P3cuartoDadoSalida0 =  (RowsClase0[(RowsClase0[i]>=0.50) & (RowsClase0[i]<0.75)][i].shape[0] + m*p ) / cantidadSalida[0] + m      
        P3cuartoDadoSalida1 =  (RowsClase1[(RowsClase1[i]>=0.50) & (RowsClase1[i]<0.75)][i].shape[0] + m*p ) / cantidadSalida[1] + m
        P4cuartoDadoSalida0  = (RowsClase0[RowsClase0[i]>0.75][i].shape[0] + m*p ) / cantidadSalida[0] + m
        P4cuartoDadoSalida1  = (RowsClase1[RowsClase1[i]>0.75][i].shape[0] + m*p ) / cantidadSalida[1] + m
        Probabilidad[i]= {"P1cuarto|salida0":P1cuartoDadoSalida0, 
                          "P1cuarto|salida1":P1cuartoDadoSalida1, 
                          "P2cuarto|salida0":P2cuartoDadoSalida0, 
                          "P2cuarto|salida1":P2cuartoDadoSalida1, 
                          "P3cuarto|salida0":P3cuartoDadoSalida0, 
                          "P3cuarto|salida1":P3cuartoDadoSalida1, 
                          "P4cuarto|salida0":P4cuartoDadoSalida0, 
                          "P4cuarto|salida1":P4cuartoDadoSalida1}
    
    return Psalida0, Psalida1, Probabilidad


"Función para evaluar una instancia con NB."   
def NB_evaluoInstancia(ejemplo, columnas, Psalida0, Psalida1, Probabilidad):
    cols_continuas = ['Edad', 'Años_de_educación', 'Capital_ganado', 'Capital_perdido', 'Horas_por_semana']
    cols_binarias = columnas.difference(cols_continuas).drop('Salida')
    
    #inicio terminos con probabilidades de las clases salida
    P0= Psalida0
    P1= Psalida1
    
    #multiplico cada termino por las probabilidades respectivas de cada valor de cada atributo binario
    for i in cols_binarias:
        if (ejemplo[i]==0):
            P0 = P0*Probabilidad[i]['P0|salida0']
            P1 = P1*Probabilidad[i]['P0|salida1']
        else:
            P0 = P0*Probabilidad[i]['P1|salida0']
            P1 = P1*Probabilidad[i]['P1|salida1']
    
    #multiplico cada termino por las probabilidades respectivas de cada valor de cada atributo coninuo
    for i in cols_continuas:
        if (ejemplo[i]<0.25):
            P0 = P0*Probabilidad[i]['P1cuarto|salida0']
            P1 = P1*Probabilidad[i]['P1cuarto|salida1']
        elif (ejemplo[i]<0.50):
            P0 = P0*Probabilidad[i]['P2cuarto|salida0']
            P1 = P1*Probabilidad[i]['P2cuarto|salida1']
        elif (ejemplo[i]<0.75):
            P0 = P0*Probabilidad[i]['P3cuarto|salida0']
            P1 = P1*Probabilidad[i]['P3cuarto|salida1']
        else:
            P0 = P0*Probabilidad[i]['P4cuarto|salida0']
            P1 = P1*Probabilidad[i]['P4cuarto|salida1']
    
    #predigo quien tenga mayor probabilidad
    if P0>P1: prediccion = 0
    else: prediccion = 1
    return prediccion



"Función para predecir un conjunto de ejemplos. devuelve un vector con la predicción para cada ejemplo" 
def NB_predecir(trainset, Ejemplos_inputCols, m):
    Psalida0, Psalida1, Probabilidad = NB_CalcularProbabilidades(trainset, m)
    return Ejemplos_inputCols.apply(NB_evaluoInstancia, axis= 1, args=[trainset.columns, Psalida0, Psalida1, Probabilidad])
  
    
"Función que aplica cross validation sobre el algoritmo NB para un dataset" 
"Se puede elegir cantidad de splits."
"imprime las métricas"
def CrossValidationNB(dataset, splits, m):
    #inicializo variables
    P, R, F1, S, A = np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2), 0
    
    kf = model_selection.KFold(splits)
    # genero indices de train y test para cada split
    for trainCVindices, testCVindices in kf.split(dataset):
        # hago prediccion para dicha division del dataset
        arrayPrediccion = NB_predecir(dataset.iloc[trainCVindices], dataset.iloc[testCVindices].drop('Salida', axis=1), m)
        # saco metricas de la prediccion
        A += metrics.accuracy_score(dataset.iloc[testCVindices].Salida, arrayPrediccion)
        Pi, Ri, F1i, S = metrics.precision_recall_fscore_support(dataset.iloc[testCVindices].Salida, arrayPrediccion)
        P += Pi
        R += Ri
        F1 += F1i
    #imprimo métricas
    print("Accurancy " + str (A/splits))
    print("Precision " + str (P/splits))
    print("Recall " + str (R/splits))
    print("F1 " + str (F1/splits))
  
    
"Método para llamar a NB con posibilidad de elegir cantidad de ejemplos entrenamiento, evaluación, y cantidad de vecinos"      
def NB(trainset, testset, CantidadEjemplosEntrenamiento, CantidadinstanciasEvaluar, m):
    # selecciono de los diferentes datasets la cantidad de elementos
    DatasetTrain = utils.resample(trainset, n_samples= CantidadEjemplosEntrenamiento)
    DatasetEjemplos = utils.resample(testset, n_samples= CantidadinstanciasEvaluar)
    #ejecuto prediccion
    arrayPrediccion = NB_predecir(DatasetTrain, DatasetEjemplos.drop('Salida', axis=1), m)
    print(metrics.classification_report(DatasetEjemplos.Salida, arrayPrediccion))
      