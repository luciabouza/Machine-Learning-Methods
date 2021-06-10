# -*- coding: utf-8 -*-
import preprocesamiento
from sklearn import model_selection, metrics, neighbors, naive_bayes
import numpy as np
from KNN import CrossValidationKNN, KNN
from NaiveBayes import CrossValidationNB, NB
import time

"Función que aplica cross validation sobre el algoritmo KNN  de Scikit para un dataset " 
"Se puede elegir cantidad de splits y el k de KNN."
"imprime las métricas"
def CrossValidationKNNSciKit(dataset, splits, k):
    #inicializo variables
    P, R, F1, S, A = np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2), 0
    
    kf = model_selection.KFold(splits)
    # genero indices de train y test para cada split
    for trainCVindices, testCVindices in kf.split(dataset):
        ClassKNN = neighbors.KNeighborsClassifier(k, algorithm= 'auto')
        ClassKNN = ClassKNN.fit(dataset.iloc[trainCVindices].drop('Salida', axis=1), dataset.iloc[trainCVindices].Salida)
        #predecimos los ejemplos del conjunto de validacion
        arrayPrediccion = ClassKNN.predict(dataset.iloc[testCVindices].drop('Salida', axis=1))
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
    
    
"Función que aplica cross validation sobre el algoritmo Naive Bayes  de Scikit para un dataset " 
"Se puede elegir cantidad de splits"
"imprime las métricas"
def CrossValidationNBSciKit(dataset, splits):
    #inicializo variables
    P, R, F1, S, A = np.zeros(2), np.zeros(2), np.zeros(2), np.zeros(2), 0
    
    kf = model_selection.KFold(splits)
    # genero indices de train y test para cada split
    for trainCVindices, testCVindices in kf.split(dataset):
        ClassNB = naive_bayes.BernoulliNB(0.5,binarize=0.5)
        ClassNB = ClassNB.fit(dataset.iloc[trainCVindices].drop('Salida', axis=1), dataset.iloc[trainCVindices].Salida)
        #predecimos los ejemplos del conjunto de validacion
        arrayPrediccion = ClassNB.predict(dataset.iloc[testCVindices].drop('Salida', axis=1))
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



"Carga y Preprocesamiento de datos"
dataset_resultado = preprocesamiento.preprocesamiento()
train, test = model_selection.train_test_split(dataset_resultado, stratify=dataset_resultado['Salida'], test_size=0.2)
trainKNN = preprocesamiento.BorradoColumnasRazaPaisNatal(train)
testKNN = preprocesamiento.BorradoColumnasRazaPaisNatal(train)
trainNBSciKit = preprocesamiento.preprocesamientoColumnasContinuas(train)
testNBSciKit = preprocesamiento.preprocesamientoColumnasContinuas(test)


"Prueba implementación KNN"   
print("Prueba implementación KNN")
start_time = time.time()
CrossValidationKNN(trainKNN,5,10)
print("Tiempo ejecución Validación cruzada KNN implementado %s seg \n" % (time.time() - start_time))

"Prueba implementación NB" 
print("Prueba implementación NB")
start_time = time.time()
CrossValidationNB(train,5,0.1)
print("Tiempo ejecución Validación cruzada NB implementado %s seg \n" % (time.time() - start_time))


"Prueba Scikit-learn KNN"  
print("Prueba Scikit-learn KNN") 
start_time = time.time()
CrossValidationKNNSciKit(trainKNN,5,5)
print("Tiempo ejecución Validación cruzada Scikit-learn KNN %s seg\n"  % (time.time() - start_time))

"Prueba Scikit-learn NB"   
print("Prueba Scikit-learn NB") 
start_time = time.time()
CrossValidationNBSciKit(trainNBSciKit,5)
print("Tiempo ejecución Validación cruzada Scikit-learn NB %s seg\n" % (time.time() - start_time))




"ejecuciones contra conjunto de test"



"Prueba implementación KNN contra test" 
print("Prueba implementación KNN contra test") 
start_time = time.time() 
KNN(trainKNN, testKNN, 10, trainKNN.shape[0], testKNN.shape[0])
print("Tiempo ejecución contra test KNN implementado %s seg \n" % (time.time() - start_time))

"Prueba implementación NB contra test" 
print("Prueba implementación NB contra test") 
start_time = time.time() 
NB(train, test, train.shape[0], test.shape[0], 0.1)
print("Tiempo ejecución contra test NB implementado %s seg \n" % (time.time() - start_time))

"Prueba Scikit-learn KNN contra test" 
print("Prueba Scikit-learn KNN contra test")  
start_time = time.time()
ClassKNN = neighbors.KNeighborsClassifier(10, algorithm= 'auto')
ClassKNN = ClassKNN.fit(trainKNN.drop('Salida', axis=1), trainKNN.Salida)
arrayPrediccion = ClassKNN.predict(testKNN.drop('Salida', axis=1))
print(metrics.classification_report(testKNN.Salida, arrayPrediccion))
print("Tiempo ejecución contra test KNN Scikit-learn %s seg \n" % (time.time() - start_time))

"Prueba Scikit-learn NB contra test" 
print("Prueba Scikit-learn NB contra test") 
start_time = time.time() 
ClassNB = naive_bayes.BernoulliNB(0.5,binarize=0.5)
ClassNB = ClassNB.fit(trainNBSciKit.drop('Salida', axis=1), trainNBSciKit.Salida)
arrayPrediccion = ClassNB.predict(testNBSciKit.drop('Salida', axis=1))
print(metrics.classification_report(testNBSciKit.Salida, arrayPrediccion))
print("Tiempo ejecución contra test NB Scikit-learn %s seg \n" % (time.time() - start_time))




