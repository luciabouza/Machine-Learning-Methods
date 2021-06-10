# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import preprocessing, model_selection, tree, metrics
from sklearn.ensemble import RandomForestClassifier
import ID3
import RandForest
import RandForestHibrido




'''
Carga y preprocesamiento Dataset
Creacion Sets entrenamiento y test
'''
#Carga de Datos
dataset = pd.read_csv('qsar_oral_toxicity.csv', sep=';', prefix='c',header=None)

#preprocesamiento
# creamos un codificador "ordinal" y lo ajustamos a la columna 1024 
enc = preprocessing.OrdinalEncoder()
enc.fit(dataset[['c1024']])
#transformamos la columna 1024 y la guardamos en una nueva columna
dataset['output']  = enc.transform(dataset[['c1024']])

#creamos conjuntos entrenamiento, validación y test (entrenamiento 64%, validación 16%, test 20%)

#trainAux, test = model_selection.train_test_split(dataset, test_size=0.2)
trainAux, test = model_selection.train_test_split(dataset, stratify=dataset['output'], test_size=0.2)

#creamos conjuntos entrenamiento y validacion (entrenamiento 80%, validacion 20%) a partir del 80% de train
train, validation = model_selection.train_test_split(trainAux, stratify=trainAux['output'], test_size=0.2)


print ("-----Implementacion ID3 parte A------")
print("Creacion Arbol y evaluacion conjunto entrenamiento")

CantidadEjemplos =  train.shape[0]
CantAtributos =  1024
ID3.CreacionYEvaluacionID3(dataset, train, validation, CantidadEjemplos, CantAtributos)


print ("\n\n-----Implementacion Random Forest parte B-----")
print("Creacion Forest y evaluacion conjunto entrenamiento")

CantArboles= 100
CantAtributos= 400
CantElementos = 4000

RandForest.CreacionYEvaluacionRandomForest(dataset, train, validation, CantArboles, CantAtributos, CantElementos)


print ("\n\n-----Implementacion Random Forest Hibrido-----")
print("Creacion Forest y evaluacion conjunto entrenamiento")

CantArboles= 100
CantAtributos= 400
CantElementos = 4000

RandForestHibrido.CreacionYEvaluacionRandomForestH(dataset, train, validation, CantArboles, CantAtributos, CantElementos)


print ("\n\n------SciKit-Learn para ID3------")
print("Creacion Arbol y metricas")

input_cols = dataset.columns[0:1024]
my_tree = tree.DecisionTreeClassifier(criterion="entropy")
my_tree = my_tree.fit(train[input_cols], train.output)

#predecimos los ejemplos del conjunto de validacion
validation_pred = my_tree.predict(validation[input_cols])

# metricas
print(metrics.classification_report(validation.output, validation_pred))



print ("\n\n-----SciKit-Learn para Random Forest-----")
print("Creacion Forest y metricas")

my_RandomForest = RandomForestClassifier(n_estimators= 100, criterion="entropy", max_features=200,bootstrap = True, max_samples=5000, n_jobs=-1)
my_RandomForest = my_RandomForest.fit(train[input_cols], train.output)

#predecimos los ejemplos del conjunto de validacion
validation_predRF = my_RandomForest.predict(validation[input_cols])

# metricas
print("\nAcierto SciKit Learn Random Forest:", metrics.classification_report(validation.output, validation_predRF))


