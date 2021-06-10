#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 12:02:49 2020

@author: luciabouza
"""

import Metodos
import pandas as pd
from sklearn import model_selection
import seaborn as sns


'Carga de Datos'
dataset = pd.read_csv('./Data/sub-data.txt', sep=',')

'preporcesamiento, borrando tuplas sin datos'
Metodos.preprocesamiento(dataset, 1) 


'*************** PARTE B ***************'

Metodos.RelacionesAtributoConIdeologia(dataset, True)
Metodos.Relaciones2AtributosConIdeologia(dataset, True)


'*************** PARTE C ***************'

'preporcesamiento, borrando tuplas sin clase objetivo y colocando la media en el resto de los datos faltantes'
Metodos.preprocesamiento(dataset, 3) 

'PCA' 
target = 'LIBCPRE_SELF'
Metodos.PreprocesamientoPCA(dataset)
ComponentesPrincipales = Metodos.PCA_impl(dataset, target)

'Cálculo Cantidad óptima de clusters'
Metodos.CantidadClustersOptima(ComponentesPrincipales)

clusters = 3
arrayClusters = Metodos.K_Means(ComponentesPrincipales, clusters)

sns.set()
'visualización Clusters en dataset'
ComponentesPrincipales['Clusters'] = arrayClusters
sns.relplot(x="CP1", y="CP2", hue="Clusters", palette='bright', data=ComponentesPrincipales, height=7, aspect=2)

'visualización datos reales ideología en dataset'
ComponentesPrincipales['Ideologia'] = dataset[target].values
sns.relplot(x="CP1", y="CP2", hue='Ideologia', palette='bright', data=ComponentesPrincipales, height=7, aspect=3)


'*************** PARTE D ***************'

'separación conjuntos'
ConjuntoAux, test = model_selection.train_test_split(dataset, stratify=dataset['LIBCPRE_SELF'], test_size=0.2)
entrenamiento, validacion = model_selection.train_test_split(ConjuntoAux, stratify=ConjuntoAux['LIBCPRE_SELF'], test_size=0.2)

'KNN'
k = 8
arrayPrediccion = Metodos.KNN(entrenamiento, validacion, target, k)

arrayAciertos = arrayPrediccion==validacion[target]

ComponentesPrincipalesTest = Metodos.PCA_impl(validacion, target)

'visualización predicciones KNN de test'
ComponentesPrincipalesTest['PrediccionesKNN'] = arrayPrediccion
sns.relplot(x="CP1", y="CP2", hue='PrediccionesKNN', palette='bright', data=ComponentesPrincipalesTest, height=7, aspect=3)

'visualización datos reales de test'
ComponentesPrincipalesTest['IdeologiaTest'] = validacion[target].values
sns.relplot(x="CP1", y="CP2", hue='IdeologiaTest', palette='bright', data=ComponentesPrincipalesTest, height=7, aspect=3)

'visualización aciertos'
ComponentesPrincipalesTest['AciertosPrediccion'] = arrayAciertos.values
sns.relplot(x="CP1", y="CP2", hue='AciertosPrediccion', palette='bright', data=ComponentesPrincipalesTest, height=7, aspect=3)
