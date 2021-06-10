# -*- coding: utf-8 -*-

import ID3
from sklearn import utils

'Funcion que devuele el Random Forest'
def RandomForest(Datos, targetAttribute, Atributos, CantArboles, CantAtributos, CantElementos):
    ListaArboles = []
    #calculo los valores de los atributos
    ValsAtributos = ID3.ValsAtributos(Datos, Atributos)
       
    for i in range(CantArboles):
        #Genero Dataset con CantElementos, tomando de forma uniforme de Datos
        DatasetArbol = utils.resample(Datos, n_samples=CantElementos)
        
        # se utilizan estructuras auxiliares porque estas son modificadas al crear el arbol
        AtributosAux = Atributos.copy()   
        ValsAtributosAux = ValsAtributos.copy()

        #llamo a ID3
        ArbolDecision = ID3.Arbol()
        ArbolDecision = ID3.ID3(DatasetArbol, targetAttribute, AtributosAux, ValsAtributosAux, CantAtributos)
        
        ListaArboles.insert(i,ArbolDecision)
        
    return ListaArboles   

        
""" Funcion que evalua una instancia en el RandomForest. 
devuelve 7 valores, que pueden tomar valores binarios.
A = 1 si Acierto, Vp= verdadero positivo, Vn= verdadero negativo,
Fp = falso psitivo, Fn= falso negativo, P= isntancia Positiva, N= instancia Negativa
"""
def EvaluarInstanciaRF (instancia, targetAtribute, ListaArboles, ValsAtributos, Atributos):
    ContadorAciertos, A, Vp, Vn, Fp, Fn, P, N = 0,0,0,0,0,0,0,0
    #evaluo instancia en cada arbol del forest, y cuento aciertos
    for arbol in ListaArboles:
        A, Vp, Vn, Fp, Fn, P, N = ID3.EvaluarInstancia (instancia, targetAtribute, arbol, ValsAtributos, Atributos)           
        ContadorAciertos += A
        
    #si en la mayoria de los arboles acerte, entonces el algoritmo Acierta 
    if (ContadorAciertos>= (len(ListaArboles)/2)): 
        #ejemplo positivo clasificado correctamente
        if instancia[targetAtribute] == 1: Vp,P = 1,1
        #ejemplo negativo clasificado correctamente
        else: Vn,N = 1,1
    else: 
        #ejemplo negativo clasificado incorrectamente
        if instancia[targetAtribute] == 0: Fp,N = 1,1
        #ejemplo positivo clasificado incorrectamente
        else: Fn,P = 1,1  
    
    return (A, Vp, Vn, Fp, Fn, P, N)

        
'Metodo que evalua un dataset en el Random Forest e imprime metricas'
def EvaluarRF(Datos, targetAtribute, ListaArboles, ValsAtributos, Atributos):
    A, Vp, Vn, Fp, Fn, CantP, CantN = 0,0,0,0,0,0,0
    for i in range(Datos.shape[0]):
        Fila = Datos.iloc[i]
        Ai, Vpi, Vni, Fpi, Fni, P, N = EvaluarInstanciaRF (Fila, targetAtribute, ListaArboles, ValsAtributos, Atributos)
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


'Metodo para crear un arandom forest y evaluar su performance'
def CreacionYEvaluacionRandomForest(dataset, train, validation, CantArboles, CantAtributos, CantElementos):
    #obtengo todas las cabeceras de columnas y borro de la lista las columnas de salida, para quedarme solo con los de entrada
    Atributos = dataset.columns.values.tolist()
    Atributos.remove('c1024')
    Atributos.remove('output')
    
    ListaArboles = []
    ListaArboles = RandomForest(train,'output', Atributos,CantArboles, CantAtributos, CantElementos)
    
    #evaluacion
    ValsAtributos = ID3.ValsAtributos(dataset, Atributos) 
    EvaluarRF(validation,'output', ListaArboles, ValsAtributos, Atributos)

