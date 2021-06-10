# -*- coding: utf-8 -*-

import numpy as np
import random
from sklearn import utils


class Arbol(object):
    
    def __init__(self):
        self.Ramas = []
        self.valor = None

'Funcion que devuelve True si el Arbol es una hoja'
def EsHoja(Arbol):
    return (len(Arbol.Ramas)==0)


'Funcion para calcular entropia'
def Entropia(ColOutput): 
    Valores, ocurrencias = np.unique(ColOutput,return_counts = True)
    CantTotal = np.sum(ocurrencias)
    E = 0
    #itero en los valores posibles de salida
    for indice in range(len(Valores)):
        P_X = ocurrencias[indice]/CantTotal
        E += - P_X*np.log2(P_X)
    return E


'Funcion para calcular termino sumatoria de Information Gain'
def IGAux(Datos, atributo):  
    Valores, ocurrencias = np.unique(Datos[atributo],return_counts = True)
    CantTotal = np.sum(ocurrencias)
    IGAux = 0
    
    for indice in range(len(Valores)):
        #me quedo solo con las filas que tienen valor Valores[indice] en el atributo y calculo cantidad registros
        mask = Datos[atributo].to_numpy() == Valores[indice]
        Datos_con_atributoValor = Datos.loc[mask]
        CantAt = ocurrencias[indice]
        #actualizo IGAux
        IGAux += (CantAt/CantTotal)*Entropia(Datos_con_atributoValor['output'])

    return IGAux


"""Funcion para calcular los posibles valores de los atributos.
Devuelve una lista de arrays con donde cada array contiene los posibles valores de del Atributo indice"""
def ValsAtributos(Datos, Atributos):
    ValsAtrib = []
    for indice in range(len(Atributos)):
        Valores = np.unique(Datos[Atributos[indice]])
        ValsAtrib.insert(indice, Valores)
    return ValsAtrib        
  
    
'Funcion que devuele el arbol de decision. No implelmenta podas'
def ID3(Datos,targetAttribute, Atributos, ValsAtributos, maxAtributos):
    
   #guardo en el array Valores, todos los valores diferentes de la columna objetivo.
   #guardo en ocurrencias la cantidad de veces que aparecen los valores de Valores
    Valores, ocurrencias = np.unique(Datos[targetAttribute],return_counts = True)
    Arb = Arbol()
    
    #si todos los valores son iguales, devuelvo ese valor
    if (len(Valores)==1):
        Arb.valor = Valores[0]
    
    #si no hay atributos, retorno el valor mas comun del atributo objetivo para los datos. 
    #aplico poda si no tengo un minimo de 10 datos
    elif (len(Atributos)==0) or (Datos.shape[0]<10):
        Arb.valor = Valores[np.argmax(ocurrencias)]
    
    else:
        #elijo de forma aleatoria maxAtributos indices en el rango del largo de Atributos
        if (len(Atributos)> maxAtributos):
            arraysubset = np.array(random.sample(list(range(len(Atributos))), maxAtributos))
            sbsetAtributos = [Atributos[i] for i in arraysubset]
            subsetValoresAtributos = [ValsAtributos[i] for i in arraysubset]
        else:
            sbsetAtributos = Atributos
            subsetValoresAtributos = ValsAtributos
        
        #seleccionar el mejor atributo
        E = Entropia(Datos[targetAttribute])
        IG_AuxAtributos = [(E-IGAux(Datos,at)) for at in sbsetAtributos] #devuelve IG de todos los at de Atributos
        Atributo_indice = np.argmax(IG_AuxAtributos)
        Atributo = sbsetAtributos[Atributo_indice]
        
        # si ningun atributo me da ganancia, aplico poda
        if(E-IG_AuxAtributos[Atributo_indice]==0):
            Arb.valor = Valores[np.argmax(ocurrencias)]
        else:
    
            #Coloco en la raiz Atributo      
            Arb.valor = Atributo
            
            #Array con valores de Atributo. 
            ValoresAtributoAux = np.array(subsetValoresAtributos[Atributo_indice], copy=True)       
            
            #obtengo indice de Atributo en Atributos
            indice = Atributos.index(Atributo) 
            #elimino el atributo de la lista
            del Atributos[indice]
            del ValsAtributos[indice]
            
            #hago crecer el arbol, iterando en cada valor posible del atributo
            for i in range(len(ValoresAtributoAux)):
                val = ValoresAtributoAux[i]
                Ejemplos = Datos.loc[Datos[Atributo] == val]
                
                # si no hay ejemplos con ese valor, coloco hoja  con el valor mas comun del atributo objetivo para los datos. 
                if (len(Ejemplos)==0):
                    Hoja = Arbol()
                    Hoja.valor = Valores[np.argmax(ocurrencias)]
                    Arb.Ramas.insert(i,Hoja)
                #sino, llamo recursivo
                else:
                    Arb.Ramas.insert(i, ID3(Ejemplos, targetAttribute, Atributos, ValsAtributos, maxAtributos))      
    return Arb


""" Funcion que evalua una instancia en el Arbol de decision. 
devuelve 7 valores, que pueden tomar valores binarios.
A = 1 si Acierto, Vp= verdadero positivo, Vn= verdadero negativo,
Fp = falso psitivo, Fn= falso negativo, P= isntancia Positiva, N= instancia Negativa
"""
def EvaluarInstancia (instancia, targetAtribute, Arbol, ValsAtributos, Atributos):
    if (EsHoja(Arbol)):
        A, Vp, Vn, Fp, Fn, P,N = 0,0,0,0,0,0,0
        if instancia[targetAtribute] == Arbol.valor:
            A = 1
            #ejemplo positivo clasificado correctamente
            if instancia[targetAtribute] == 1: Vp, P = 1,1
            #ejemplo negativo clasificado correctamente
            else: Vn,N = 1,1
        else: 
            #ejemplo negativo clasificado incorrectamente
            if instancia[targetAtribute] == 0: Fp,N = 1,1
            #ejemplo positivo clasificado incorrectamente
            else: Fn, P = 1,1             
        return (A, Vp, Vn, Fp, Fn, P, N)
    else:
        AtributoNodo= Arbol.valor
        valorInstancia = instancia[AtributoNodo]
        indice = Atributos.index(AtributoNodo) #obtengo indice de AtributoNodo en Atributos
        PosiblesvaloresAtributoNodo = ValsAtributos[indice]  #obtengo rango de valores de AtributoNodo
        indexValorInstancia = list(PosiblesvaloresAtributoNodo).index(valorInstancia) #obtengo indice de valorInstancia en posibles valores de atributo
        return EvaluarInstancia(instancia, targetAtribute, Arbol.Ramas[indexValorInstancia], ValsAtributos, Atributos)

        
'Metodo que evalua un dataset en el Arbol de decision e imprime metricas'
def Evaluar(Datos, targetAtribute, Arbol, ValsAtributos, Atributos):
    A, Vp, Vn, Fp, Fn, CantP, CantN = 0,0,0,0,0,0,0
    for i in range(Datos.shape[0]):
        Fila = Datos.iloc[i]
        Ai, Vpi, Vni, Fpi, Fni, P, N = EvaluarInstancia (Fila, targetAtribute, Arbol, ValsAtributos, Atributos)
        A += Ai
        Vp += Vpi
        Vn += Vni
        Fp += Fpi
        Fn += Fni
        CantP += P
        CantN += N
        
    print ("Accurancy: " + str(A/Datos.shape[0]))
    
    if (CantP>0): 
        print("ejemplos positivos: " + str(CantP))
        print("ejemplos positivos acertados: " + str(Vp))
        if ((Vp + Fp)==0):
            print("Ningun ejemplo fue clasificado como positivo por lo que Precision no puede calcularse")
            PresicionPositivos =0
        else:
            PresicionPositivos = Vp/(Vp + Fp)
            print("Precision 1: " + str(PresicionPositivos))
        RecallPositivos = Vp/(Vp + Fn)
        print("Recall 1: " + str(RecallPositivos))
        if (PresicionPositivos>0) and (RecallPositivos>0):
            print("F1 1: " + str(2*PresicionPositivos*RecallPositivos/(PresicionPositivos+RecallPositivos)))
        else:
            print("Ningun ejemplo positivo fue acertado por lo que F1 no puede calcularse")
    else:
        print("No hay ejemplos positivos en el conjunto de test")
    
    if (CantN>0): 
        print("ejemplos Negativos: " + str(CantN))
        print("ejemplos Negativos acertados: " + str(Vn))
        if ((Vn + Fn)==0):
            print("Ningun ejemplo fue clasificado como negativo por lo que Precision no puede calcularse")
            PresicionNegativos =0
        else:
            PresicionNegativos = Vn/(Vn + Fn)
            print("Precision 0: " + str(PresicionNegativos))
        RecallNegativos = Vn/(Vn + Fp)
        print("Recall 0: " + str(RecallNegativos))
        if (PresicionNegativos>0) and (RecallNegativos>0):
            print("F1 0: " + str(2*PresicionNegativos*RecallNegativos/(PresicionNegativos+RecallNegativos)))
        else:
            print("Ningun ejemplo negativo fue acertado por lo que F1 no puede calcularse")
    else:
        print("No hay ejemplos negativos en el conjunto de test")


'Metodo para crear un arbol de decision y evaluar su performance'
def CreacionYEvaluacionID3(dataset, train, validation, CantidadEjemplos, CantAtributos):
    #Genero Dataset con CantElementos, tomando de forma uniforme de Datos
    DatasetArbol = utils.resample(train, n_samples= CantidadEjemplos)
    
    #obtengo todas las cabeceras de columnas y borro de la lista las columnas de salida, para quedarme solo con los de entrada      
    Atributos = dataset.columns.values.tolist()
    Atributos.remove('c1024')
    Atributos.remove('output')
    
    #Tomo CantAtributos de Atributos de forma aleatoria, sin repetidos
    ValsAtributo = ValsAtributos(dataset, Atributos)
    
    # se utilizan estructuras auxiliares porque estas son modificadas al crear el arbol
    AtributosAux = Atributos.copy()   
    ValsAtributosAux = ValsAtributos(dataset, AtributosAux)
    
    #creacion del arbol
    ArbolDecision = ID3(DatasetArbol,'output', AtributosAux, ValsAtributosAux, CantAtributos)
    
    #evaluacion
    Evaluar(validation,'output', ArbolDecision, ValsAtributo, Atributos)

