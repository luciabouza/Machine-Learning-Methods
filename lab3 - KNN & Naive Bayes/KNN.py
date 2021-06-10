# -*- coding: utf-8 -*-
from sklearn import model_selection, metrics, utils
import numpy as np
  
 
"Función para evaluar una instancia con KNN. se puede elegir la cantidad de vecinos a tener en cuenta"   
def KNN_evaluoInstancia(ejemplo, trainset, k):
    # calculo distancia euclidea del ejemplo con cada fila del trianset (uso norma de la resta de la matriz trianset y vector ejemplo)
    Vectordistancias = np.linalg.norm(trainset.drop('Salida', axis=1) - ejemplo, axis=-1)
    # ordeno la lista y me quedo con los k primeros (mas cercanos)  
    indiceskvecinos = np.argsort(Vectordistancias)[0:k]    
    #evaluo el resultado de la salida para los k vecinos y sumo 
    suma = np.sum(trainset['Salida'].iloc[indiceskvecinos])
    # devuelvo el valor mas usual 
    prediccion = 0 
    if (suma> k/2): prediccion = 1  
    return (prediccion)


"Función para predecir un conjunto de ejemplos. devuelve un vector con la predicción para cada ejemplo" 
def KNN_predecir(trainset, k, Ejemplos_inputCols):
    return Ejemplos_inputCols.apply(KNN_evaluoInstancia, axis= 1, args=[trainset, k])
  
    
"Función que aplica cross validation sobre el algoritmo KNN para un dataset" 
"Se puede elegir cantidad de splits y el k de KNN."
"imprime las métricas"
def CrossValidationKNN(dataset, splits, k):
    #inicializo variables
    P, R, F1, S, A = np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2), 0
    
    kf = model_selection.KFold(splits)
    # genero indices de train y test para cada split
    for trainCVindices, testCVindices in kf.split(dataset):
        # hago prediccion para dicha division del dataset
        arrayPrediccion = KNN_predecir(dataset.iloc[trainCVindices], k, dataset.iloc[testCVindices].drop('Salida', axis=1))
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
 
    
"Método para llamar a KNN con posibilidad de elegir cantidad de ejemplos entrenamiento, evaluación, y cantidad de vecinos"      
def KNN(trainset, testset, k, CantidadEjemplosEntrenamiento, CantidadinstanciasEvaluar):
    # selecciono de los diferentes datasets la cantidad de elementos
    DatasetTrain = utils.resample(trainset, n_samples= CantidadEjemplosEntrenamiento)
    DatasetEjemplos = utils.resample(testset, n_samples= CantidadinstanciasEvaluar)
    #ejecuto prediccion
    arrayPrediccion = KNN_predecir(DatasetTrain, k, DatasetEjemplos.drop('Salida', axis=1))
    print(metrics.classification_report(DatasetEjemplos.Salida, arrayPrediccion))
      

