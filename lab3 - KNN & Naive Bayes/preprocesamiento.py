# -*- coding: utf-8 -*-
import pandas as pd
import sklearn.preprocessing
import sklearn.feature_selection


"Función que borra las columnas de one-hot-encoding de País_Natal y Raza del dataset"
"se utliza para correr KNN"
def BorradoColumnasRazaPaisNatal(dataset):
    
    dataset_resultado = dataset.copy()
    
    # Borro Atributo Raza

    del dataset_resultado['Amer-Indian-Eskimo']
    del dataset_resultado['Asian-Pac-Islander']
    del dataset_resultado['Black']
    del dataset_resultado['Other']
    del dataset_resultado['White']
       
    # Borro Atributo País_natal
    del dataset_resultado['Cambodia']
    del dataset_resultado['Canada']
    del dataset_resultado['China']
    del dataset_resultado['Columbia']
    del dataset_resultado['Cuba']
    del dataset_resultado['Dominican-Republic']
    del dataset_resultado['Ecuador']
    del dataset_resultado['El-Salvador']
    del dataset_resultado['England']
    del dataset_resultado['France']
    del dataset_resultado['Germany']
    del dataset_resultado['Greece']
    del dataset_resultado['Guatemala']
    del dataset_resultado['Haiti']
    del dataset_resultado['Holand-Netherlands']
    del dataset_resultado['Honduras']
    del dataset_resultado['Hong']
    del dataset_resultado['Hungary']
    del dataset_resultado['India']
    del dataset_resultado['Iran']
    del dataset_resultado['Ireland']
    del dataset_resultado['Italy']
    del dataset_resultado['Jamaica']
    del dataset_resultado['Japan']
    del dataset_resultado['Laos']
    del dataset_resultado['Mexico']
    del dataset_resultado['Nicaragua']
    del dataset_resultado['Outlying-US(Guam-USVI-etc)']
    del dataset_resultado['Peru']
    del dataset_resultado['Philippines']
    del dataset_resultado['Poland']
    del dataset_resultado['Portugal']
    del dataset_resultado['Puerto-Rico']
    del dataset_resultado['Scotland']
    del dataset_resultado['South']
    del dataset_resultado['Taiwan']
    del dataset_resultado['Thailand']
    del dataset_resultado['Trinadad&Tobago']
    del dataset_resultado['United-States']
    del dataset_resultado['Vietnam']
    del dataset_resultado['Yugoslavia']
    
    return dataset_resultado
    

"Preporcesamiento de los datos según lo descrito en el informe"
"eliminación columnas, eliminación filas con valores faltantes, one-hot encoding, estandarización con min-max Scaling"
def preprocesamiento():

    #Carga de Datos
    columnas =['Edad','Relación_laboral', 'Peso_Final', 'Educación', 'Años_de_educación', 'Estado_civil', 'Ocupación', 'Relación_en_la_familia', 'Raza', 'Sexo', 'Capital_ganado', 'Capital_perdido', 'Horas_por_semana', 'País_natal', 'Salida' ]
    dataset = pd.read_csv('./Data/adult.data.csv', sep=',', names = columnas)
    
    #tratamiento elementos faltantes
    dataset.loc[dataset['País_natal'] == ' ?', 'País_natal']= 'United-States'
    dataset.drop(dataset[(dataset['Ocupación'] == ' ?')].index, inplace= True)
    
    #selección de atributos
    del dataset['Relación_en_la_familia']
    del dataset['Educación']
    del dataset['Peso_Final']
    
    #representación de atributos
    
    #genero nuevo dataset porque luego no puedo borrar las columnas categoricas
    columnasNumericas = dataset[['Edad', 'Años_de_educación', 'Sexo', 'Capital_ganado', 'Capital_perdido', 'Horas_por_semana', 'Salida']]
    dataset_resultado = columnasNumericas.copy()
    
    #Atributo Sexo
    le=sklearn.preprocessing.LabelEncoder()
    le.fit(dataset_resultado['Sexo'])
    dataset_resultado.loc[:,'Sexo'] = le.transform(dataset_resultado.loc[:,'Sexo'])
    
    #Atributo Relación_laboral
    ohe=sklearn.preprocessing.OneHotEncoder(sparse=False)
    ohe.fit(dataset['Relación_laboral'].to_numpy().reshape(-1,1))
    new=ohe.transform(dataset['Relación_laboral'].to_numpy().reshape(-1,1))
    dataset_resultado['Federal-gov']=new[:,0]
    dataset_resultado['Local-gov']=new[:,1]
    dataset_resultado['Private']=new[:,2]
    dataset_resultado['Self-emp-inc']=new[:,3]
    dataset_resultado['Self-emp-not-inc']=new[:,4]
    dataset_resultado['State-gov']=new[:,5]
    dataset_resultado['Without-pay']=new[:,6]
    
    
    #Atributo Estado_civil
    ohe=sklearn.preprocessing.OneHotEncoder(sparse=False)
    ohe.fit(dataset['Estado_civil'].to_numpy().reshape(-1,1))
    new=ohe.transform(dataset['Estado_civil'].to_numpy().reshape(-1,1))
    dataset_resultado['Divorced']=new[:,0]
    dataset_resultado['Married-AF-spouse']=new[:,1]
    dataset_resultado['Married-civ-spouse']=new[:,2]
    dataset_resultado['Married-spouse-absent']=new[:,3]
    dataset_resultado['Never-married']=new[:,4]
    dataset_resultado['Separated']=new[:,5]
    dataset_resultado['Widowed']=new[:,6]
    
    
    #Atributo Ocupación
    ohe=sklearn.preprocessing.OneHotEncoder(sparse=False)
    ohe.fit(dataset['Ocupación'].to_numpy().reshape(-1,1))
    new=ohe.transform(dataset['Ocupación'].to_numpy().reshape(-1,1))
    dataset_resultado['Adm-clerical']=new[:,0]
    dataset_resultado['Craft-repair']=new[:,1]
    dataset_resultado['Exec-managerial']=new[:,2]
    dataset_resultado['Farming-fishing']=new[:,3]
    dataset_resultado['Handlers-cleaners']=new[:,4]
    dataset_resultado['Machine-op-inspct']=new[:,5]
    dataset_resultado['Other-service']=new[:,6]
    dataset_resultado['Priv-house-serv']=new[:,7]
    dataset_resultado['Prof-specialty']=new[:,8]
    dataset_resultado['Protective-serv']=new[:,9]
    dataset_resultado['Sales']=new[:,10]
    dataset_resultado['Tech-support']=new[:,11]
    dataset_resultado['Transport-moving']=new[:,12]
    
    
    #Atributo Raza
    ohe=sklearn.preprocessing.OneHotEncoder(sparse=False)
    ohe.fit(dataset['Raza'].to_numpy().reshape(-1,1))
    new=ohe.transform(dataset['Raza'].to_numpy().reshape(-1,1))
    dataset_resultado['Amer-Indian-Eskimo']=new[:,0]
    dataset_resultado['Asian-Pac-Islander']=new[:,1]
    dataset_resultado['Black']=new[:,2]
    dataset_resultado['Other']=new[:,3]
    dataset_resultado['White']=new[:,4]
    
    
    #Atributo País_natal
    ohe=sklearn.preprocessing.OneHotEncoder(sparse=False)
    ohe.fit(dataset['País_natal'].to_numpy().reshape(-1,1))
    new=ohe.transform(dataset['País_natal'].to_numpy().reshape(-1,1))
    dataset_resultado['Cambodia']=new[:,0]
    dataset_resultado['Canada']=new[:,1]
    dataset_resultado['China']=new[:,2]
    dataset_resultado['Columbia']=new[:,3]
    dataset_resultado['Cuba']=new[:,4]
    dataset_resultado['Dominican-Republic']=new[:,5]
    dataset_resultado['Ecuador']=new[:,6]
    dataset_resultado['El-Salvador']=new[:,7]
    dataset_resultado['England']=new[:,8]
    dataset_resultado['France']=new[:,9]
    dataset_resultado['Germany']=new[:,10]
    dataset_resultado['Greece']=new[:,11]
    dataset_resultado['Guatemala']=new[:,12]
    dataset_resultado['Haiti']=new[:,13]
    dataset_resultado['Holand-Netherlands']=new[:,14]
    dataset_resultado['Honduras']=new[:,15]
    dataset_resultado['Hong']=new[:,16]
    dataset_resultado['Hungary']=new[:,17]
    dataset_resultado['India']=new[:,18]
    dataset_resultado['Iran']=new[:,19]
    dataset_resultado['Ireland']=new[:,20]
    dataset_resultado['Italy']=new[:,21]
    dataset_resultado['Jamaica']=new[:,22]
    dataset_resultado['Japan']=new[:,23]
    dataset_resultado['Laos']=new[:,24]
    dataset_resultado['Mexico']=new[:,25]
    dataset_resultado['Nicaragua']=new[:,26]
    dataset_resultado['Outlying-US(Guam-USVI-etc)']=new[:,27]
    dataset_resultado['Peru']=new[:,28]
    dataset_resultado['Philippines']=new[:,29]
    dataset_resultado['Poland']=new[:,30]
    dataset_resultado['Portugal']=new[:,31]
    dataset_resultado['Puerto-Rico']=new[:,32]
    dataset_resultado['Scotland']=new[:,33]
    dataset_resultado['South']=new[:,34]
    dataset_resultado['Taiwan']=new[:,35]
    dataset_resultado['Thailand']=new[:,36]
    dataset_resultado['Trinadad&Tobago']=new[:,37]
    dataset_resultado['United-States']=new[:,38]
    dataset_resultado['Vietnam']=new[:,39]
    dataset_resultado['Yugoslavia']=new[:,40]
    
    
    #Atributo Salida
    le=sklearn.preprocessing.LabelEncoder()
    le.fit(dataset_resultado['Salida'])
    dataset_resultado.loc[:,'Salida'] = le.transform(dataset_resultado.loc[:,'Salida'])
    
    #Estandarizacion de artibutos numericos con min max scaling

    min_x=min(dataset_resultado['Edad'])
    max_x=max(dataset_resultado['Edad'])
    dataset_resultado['Edad'] = (dataset_resultado['Edad']-min_x)/(max_x- min_x)
    
    min_x=min(dataset_resultado['Años_de_educación'])
    max_x=max(dataset_resultado['Años_de_educación'])
    dataset_resultado['Años_de_educación'] = (dataset_resultado['Años_de_educación']-min_x)/(max_x- min_x)
 
    min_x=min(dataset_resultado['Capital_ganado'])
    max_x=max(dataset_resultado['Capital_ganado'])
    dataset_resultado['Capital_ganado'] = (dataset_resultado['Capital_ganado']-min_x)/(max_x- min_x)
    
    
    min_x=min(dataset_resultado['Capital_perdido'])
    max_x=max(dataset_resultado['Capital_perdido'])
    dataset_resultado['Capital_perdido'] = (dataset_resultado['Capital_perdido']-min_x)/(max_x- min_x)
    
    min_x=min(dataset_resultado['Horas_por_semana'])
    max_x=max(dataset_resultado['Horas_por_semana'])
    dataset_resultado['Horas_por_semana'] = (dataset_resultado['Horas_por_semana']-min_x)/(max_x- min_x)
      
    return dataset_resultado


"cambio de atributos continuos a categóricos. utlizado para Naive bayes de scikit-learn"
def preprocesamientoColumnasContinuas(dataset1):
    cols_continuas = ['Edad', 'Años_de_educación', 'Capital_ganado', 'Capital_perdido', 'Horas_por_semana']
    dataset = dataset1.copy()
    
    for i in cols_continuas:
        dataset.loc[dataset[i]<0.25, i]= 1
        dataset.loc[((dataset[i]>=0.25) & (dataset[i]<0.50)), i]= 2
        dataset.loc[((dataset[i]>=0.50) & (dataset[i]<0.75)), i]= 3
        dataset.loc[dataset[i]>0.75, i]= 4
    return dataset

