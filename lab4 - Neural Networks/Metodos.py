#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 20:43:19 2020

@author: luciabouza
"""

import pandas as pd
from sklearn import  neighbors, metrics
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

'preprocesamiento de los datos'
# opción 1 = borro todas las tuplas con valores faltantes
# opcion 2 = borro las tuplas con valores faltantes en la clase objetivo y al resto le pongo la media de la clase
# opcion 3 = A todas las celdas con valores faltantes le coloco el valor de la media de la clase
def preprocesamiento(dataset, Opción):
    
    if (Opción == 1):
        # borro todas las tuplas con datos faltantes
        dataset.drop(dataset[(dataset['LIBCPRE_SELF'] < 0)].index, inplace= True)
        dataset.drop(dataset[(dataset['INCGROUP_PREPOST'] < 0)].index, inplace= True)
        dataset.drop(dataset[(dataset['DEM_AGEGRP_IWDATE'] < 0)].index, inplace= True)
        dataset.drop(dataset[(dataset['DEM_EDUGROUP'] < 0)].index, inplace= True)
        dataset.drop(dataset[(dataset['RELIG_IMPORT'] < 0)].index, inplace= True)
        dataset.drop(dataset[(dataset['DEM_RACEETH'] < 0)].index, inplace= True)
    elif (Opción == 2):
        # borro las tuplas con valores faltantes en la clase objetivo y al resto le pongo la media de la clase
        dataset.drop(dataset[(dataset['LIBCPRE_SELF'] < 0)].index, inplace= True)
        dataset.loc[(dataset['INCGROUP_PREPOST'] < 0), 'INCGROUP_PREPOST'] = 13
        dataset.loc[(dataset['DEM_AGEGRP_IWDATE'] < 0), 'DEM_AGEGRP_IWDATE'] = 8
        dataset.loc[(dataset['DEM_EDUGROUP'] < 0), 'DEM_EDUGROUP'] = 3
        dataset.loc[(dataset['RELIG_IMPORT'] < 0), 'RELIG_IMPORT'] = 1
        dataset.loc[(dataset['DEM_RACEETH'] < 0), 'DEM_RACEETH'] = 1
    else:
        # para los datos faltantes coloco la media
        dataset.loc[(dataset['LIBCPRE_SELF'] < 0), 'LIBCPRE_SELF'] = 4
        dataset.loc[(dataset['INCGROUP_PREPOST'] < 0), 'INCGROUP_PREPOST'] = 13
        dataset.loc[(dataset['DEM_AGEGRP_IWDATE'] < 0), 'DEM_AGEGRP_IWDATE'] = 8
        dataset.loc[(dataset['DEM_EDUGROUP'] < 0), 'DEM_EDUGROUP'] = 3
        dataset.loc[(dataset['RELIG_IMPORT'] < 0), 'RELIG_IMPORT'] = 1
        dataset.loc[(dataset['DEM_RACEETH'] < 0), 'DEM_RACEETH'] = 1
        

'Plots de relaciones'    
def RelacionesAtributoConIdeologia(dataset, soloRelevantes):
    labelsIdologia = ["", "Extremadamente liberal", "Liberal", "Ligeramente liberal", "Moderado", "Ligeramente Conservador", "Conservador", "Extremadamente Conservador"]
    paleta = sns.cubehelix_palette(8, start=.5, rot=-.75)
    
    sns.set()
    GraficoRaza = sns.catplot(x= 'DEM_RACEETH', y="LIBCPRE_SELF", kind="boxen", data= dataset, palette=paleta)
    GraficoReligion = sns.catplot(x= 'RELIG_IMPORT', y="LIBCPRE_SELF", kind="boxen", data= dataset, palette=paleta)
    GraficoEducacion = sns.catplot(x= 'DEM_EDUGROUP', y="LIBCPRE_SELF", kind="boxen", data= dataset, height=7, aspect=2, palette=paleta)
    GraficoEdad = sns.catplot(x= 'DEM_AGEGRP_IWDATE', y="LIBCPRE_SELF", kind="boxen", data= dataset, height=6, aspect=2, palette=paleta)
    
    GraficoRaza.set_axis_labels("Raza", "Ideología")
    GraficoRaza.set_xticklabels(["Blanco", "Negro", "Latino", "Otro"])
    GraficoRaza.set_yticklabels(labelsIdologia)
    
    GraficoReligion.set_axis_labels("Importancia a la religión", "Ideología")
    GraficoReligion.set_xticklabels(["Si", "No"])
    GraficoReligion.set_yticklabels(labelsIdologia)
    
    GraficoEducacion.set_axis_labels("Nivel educativo", "Ideología")
    GraficoEducacion.set_xticklabels(["Menos que liceo", "Liceo aprobado", "Terciario sin título", "Título de grado", "Título Maestría o doctorado"])
    GraficoEducacion.set_yticklabels(labelsIdologia)
    
    GraficoEdad.set_axis_labels("Escala edad", "Ideología")  
    GraficoEdad.set_yticklabels(labelsIdologia)
       
    if not soloRelevantes:
        GraficoIngresos = sns.catplot(x= 'INCGROUP_PREPOST', y="LIBCPRE_SELF", kind="boxen", data= dataset, palette=paleta)
        GraficoIngresos.set_axis_labels("Escala ingresos", "Ideología")  
        GraficoIngresos.set_yticklabels(labelsIdologia)

def Relaciones2AtributosConIdeologia(dataset, soloRelevantes):
    labelsIdologia = ["Ext. lib.", "Lib.", "Lig. lib.", "Mod.", "Lig. Cons.", "Cons.", "Extr. Cons."]
    paleta = sns.cubehelix_palette(8, start=.5, rot=-.75)
    
    sns.set()  
    GraficoReligionIngresos = sns.catplot(x= 'RELIG_IMPORT', y="INCGROUP_PREPOST",  kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=6, aspect=2, palette=paleta)
    GraficoEducacionIngresos = sns.catplot(x= 'DEM_EDUGROUP', y="INCGROUP_PREPOST", kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=7, aspect=2, palette=paleta)
    
    GraficoEducacionIngresos.set_axis_labels("Nivel educativo", "Escala ingresos")
    GraficoEducacionIngresos.set_xticklabels(["Menos que liceo", "Liceo aprobado", "Terciario sin título", "Título de grado", "Título Maestría o doctorado"])
  
    GraficoEducacionIngresos._legend.set_title("Ideologia")
    for t, l in zip(GraficoEducacionIngresos._legend.texts, labelsIdologia): t.set_text(l)
    
    GraficoReligionIngresos.set_axis_labels("Importancia a la religión", "Escala ingresos")
    GraficoReligionIngresos.set_xticklabels(["Si", "No"])
    
    GraficoReligionIngresos._legend.set_title("Ideologia")
    for t, l in zip(GraficoReligionIngresos._legend.texts, labelsIdologia): t.set_text(l)

    if not soloRelevantes:
        sns.catplot(x= 'DEM_RACEETH', y="INCGROUP_PREPOST", kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=7, aspect=3, palette=paleta)   
        sns.catplot(x= 'DEM_AGEGRP_IWDATE', y="INCGROUP_PREPOST",  kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=7, aspect=3,palette=paleta)
        sns.catplot(x= 'DEM_RACEETH', y="DEM_AGEGRP_IWDATE",  kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=6, aspect=2, palette=paleta)
        sns.catplot(x= 'RELIG_IMPORT', y="DEM_AGEGRP_IWDATE",  kind="boxen", hue="LIBCPRE_SELF", data= dataset, palette=paleta)
        sns.catplot(x= 'DEM_EDUGROUP', y="DEM_AGEGRP_IWDATE", kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=7, aspect=3, palette=paleta)
        sns.catplot(x="DEM_RACEETH", y='DEM_EDUGROUP', kind="boxen", hue="LIBCPRE_SELF", data= dataset, height=6, aspect=2, palette=paleta)
        sns.catplot(x="RELIG_IMPORT", y= 'DEM_EDUGROUP', kind="boxen", hue="LIBCPRE_SELF", data= dataset, palette=paleta)
        sns.catplot(x= 'RELIG_IMPORT', y="DEM_RACEETH", kind="boxen", hue="LIBCPRE_SELF", data= dataset, palette=paleta)


'PCA'
# normalización dataset
def PreprocesamientoPCA(dataset):
    scaler = StandardScaler()
    scaler.fit(dataset) 
    dataset = scaler.transform(dataset) 


def PCA_impl(dataset, target):
    pca = PCA(n_components=2) #elijo obtener 2 componentes
    ComponentesPrincipales = pca.fit_transform(dataset.drop(target, axis=1)) #No considero la clase objetivo
    CP = pd.DataFrame(data = ComponentesPrincipales, columns = ['CP1', 'CP2'])  # genero nuevo dataset con los componentes
    print('Porcentaje información de cada componente: {}'.format(pca.explained_variance_ratio_))
    return CP


'KNN'
#Predicciones KNN con algoritomo de Scikit-learn. También imprimo métricas
def KNN(train, test, target, k):
    ClassKNN = neighbors.KNeighborsClassifier(k, algorithm= 'auto')
    ClassKNN = ClassKNN.fit(train.drop(target, axis=1), train[target])
    arrayPrediccion = ClassKNN.predict(test.drop(target, axis=1))
    print(metrics.classification_report(test[target], arrayPrediccion))
    return arrayPrediccion
  
    
'Clustering'   
# aplicación k-means de scikit. 
def K_Means(dataset, clusters):    
    arrayPrediccion = KMeans(n_clusters= clusters, init='k-means++').fit_predict(dataset)
    return arrayPrediccion

# cálculo de clusters óptima con método del codo
def CantidadClustersOptima(dataset):
    # calculo incercia de cálculo con diferentes cantidades de clusters (del 1 al 10)
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters= i, init='k-means++').fit(dataset)
        wcss.append(kmeans.inertia_)
    #grafico
    plt.plot(range(1, 11), wcss)
    plt.title('Método del codo')
    plt.xlabel('#Clusters')
    plt.ylabel('WCSS')


