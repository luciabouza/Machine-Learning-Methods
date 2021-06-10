# -*- coding: utf-8 -*-
"""
modulo para definir el tablero y sus metodos
"""

import random

class Tablero:
    
    def __init__(self):
        # inicializo matrices
        self.xRojas =[]
        self.yRojas = []
        self.xNegras =[]
        self.yNegras = []

    # Coloca fichas en coordenadas aleatorias en el tablero. NO verifica si es Tablero final           
    def inicializoPartida(self):  
        coordenadasOcupadas = []           
        for i in range(4):
            x = random.randrange(5)
            y = random.randrange(5)
            while ([x,y] in coordenadasOcupadas):
                x = random.randrange(5)
                y = random.randrange(5)
            else:
                self.xRojas.append(x)
                self.yRojas.append(y)
                coordenadasOcupadas.append([x,y])
        for i in range(4):
            x = random.randrange(5)
            y = random.randrange(5)
            while ([x,y] in coordenadasOcupadas):
                x = random.randrange(5)
                y = random.randrange(5)
            else:
                self.xNegras.append(x)
                self.yNegras.append(y)
                coordenadasOcupadas.append([x,y])
        
        
    def copy(self):
        TabCopia = Tablero()
        TabCopia.xRojas = self.xRojas.copy()
        TabCopia.yRojas = self.yRojas.copy()
        TabCopia.xNegras = self.xNegras.copy()
        TabCopia.yNegras = self.yNegras.copy()
        return TabCopia
    
    #Verifica si se dan las condiciones en el tablero para determinar si jugador gano la partida    
    def EsGanador(self,jugador):
            color = jugador.color
            Gano = False
            setX= set(())
            setY= set(())
            setDiferencia= set(())
            setSuma= set(())
            
            #defino sets auxiliares
            if (color=='Rojo'):
                for i in range(4):
                    setX.add(self.xRojas[i])
                    setY.add(self.yRojas[i])
                    setDiferencia.add(self.xRojas[i]-self.yRojas[i])
                    setSuma.add(self.xRojas[i]+self.yRojas[i])
            
            if (color=='Negro'):
                for i in range(4):
                    setX.add(self.xNegras[i])
                    setY.add(self.yNegras[i])
                    setDiferencia.add(self.xNegras[i]-self.yNegras[i])
                    setSuma.add(self.xRojas[i]+self.yNegras[i])
                
            #chequeo si fichas estan en fila y consecutivas
            if (len(setX)== 1 and (1 in setY) and (2 in setY) and (3 in setY)):
                Gano = True
            #chequeo si fichas estan en columna y consecutivas
            elif (len(setY)== 1 and (1 in setX) and (2 in setX) and (3 in setX)):
                Gano = True     
            #chequeo si fichas estan en diagonal principal y consecutivas
            elif (len(setDiferencia)== 1 and (0 in setDiferencia) and (1 in setY) and (2 in setY) and (3 in setY)):
                Gano = True
            #chequeo si fichas estan en diagonal por encima de la principal (siempre consecutivas)
            elif (len(setDiferencia)== 1 and (1 in setDiferencia)): 
                Gano = True
            #chequeo si fichas estan en diagonal por debajo de la principal (siempre consecutivas)
            elif (len(setDiferencia)== 1 and (-1 in setDiferencia)):
                Gano = True
            #chequeo si fichas estan en diagonal inversa y consecutivas
            elif (len(setSuma)== 1 and (4 in setSuma) and (1 in setY) and (2 in setY) and (3 in setY)):
                Gano = True
            #chequeo si fichas estan en diagonal por encima de la inversa (siempre consecutivas)
            elif (len(setSuma)== 1 and (3 in setSuma)): 
                Gano = True
            #chequeo si fichas estan en diagonal por debajo de la inversa (siempre consecutivas)
            elif (len(setSuma)== 1 and (5 in setSuma)):
                Gano = True
            #chequeo cuadrado
            elif ((len(setX)== len(setY) == 2) and (setX.issubset(setY))) :
                indice1 = setX.pop()
                indice2 = setX.pop()
                if abs(indice1-indice2)==1:
                    Gano = True
                    
            #borro sets auxiliares        
            del setX
            del setY
            del setDiferencia
            del setSuma
            return Gano
            
    #Da valores a los tableros finales.    
    def calcularValorTableroFinal(self, jugador, contrincante):
        if self.EsGanador(jugador):
            return 1
        elif self.EsGanador(contrincante):
            return -1
        else:
            return 0
    
    #Dado un tablero y un jugador, obtiene el vector Xi.
    def SacarDatosX(self, jugador):
        color = jugador.color
        #notación variables
        #x1 = maxima cantidad de fichas jugador, sin fichas contrincante, tomando de a 4 casillas adyacentes (lineas, diagonal o cuadrado)
        #x2 = maxima cantidad de fichas contrincante, sin fichas jugador, tomando de a 4 casillas adyacentes (lineas, diagonal o cuadrado)
        #x3 = minimo de todas las distancias maximas entre fichas jugador
        #x4 = minimo de todas las distancias maximas entre fichas contrincante
        
        
        maxAdyRojas = self.maxCantidadFichasEnAdyacencia(self.xRojas, self.yRojas, self.xNegras, self.yNegras)
        maxAdyNegras = self.maxCantidadFichasEnAdyacencia(self.xNegras, self.yNegras, self.xRojas, self.yRojas)
        
        minDistMaxRojas = self.minDistanciasMaximas(self.xRojas, self.yRojas)
        minDistMaxNegras = self.minDistanciasMaximas(self.xNegras, self.yNegras)
        
        if color =='Rojo':
            x1 = maxAdyRojas
            x2 = maxAdyNegras
            x3 = minDistMaxRojas
            x4 = minDistMaxNegras
        else:
            x2 = maxAdyNegras
            x1 = maxAdyRojas
            x3 = minDistMaxNegras
            x4 = minDistMaxRojas
        
        vectorX = [1,x1,x2,x3,x4]		
        return(vectorX)
    
    # devuelve maxima cantidad de fichas jugador, sin fichas contrincante, tomando de a 4 casillas adyacentes (lineas, diagonal o cuadrado)
    def maxCantidadFichasEnAdyacencia(self,xJugador, yJugador, xContrincante, yContrincante):
        x1=0     
        #Filas        
        for i in xJugador:
            if (i in xContrincante):
                if xContrincante.count(i)>1 or xContrincante.index(i)==1 or xContrincante.index(i)==2 or xContrincante.index(i)==3: #esta fila no sirve
                    contador =0
                else:
                    contador = xJugador.count(i)
            else:
                listaIndices = self.devolverIndices(xJugador, i)
                listaValores = self.devolverValores(yJugador, listaIndices)  
                if (0 in listaValores) and (4 in listaValores):
                    contador = xJugador.count(i)-1
                else:
                    contador = xJugador.count(i)
            if contador>x1:x1 = contador 
        
        #Columnas
        for i in yJugador:
            if (i in yContrincante):
                if yContrincante.count(i)>1 or yContrincante.index(i)==1 or yContrincante.index(i)==2 or yContrincante.index(i)==3: #esta fila no sirve
                    contador =0
                else:
                    contador = yJugador.count(i)
            else:
                listaIndices = self.devolverIndices(yJugador, i)
                listaValores = self.devolverValores(xJugador, listaIndices)  
                if (0 in listaValores) and (4 in listaValores):
                    contador = yJugador.count(i)-1
                else:
                    contador = yJugador.count(i)
            if contador>x1:x1 = contador 
                
        #Diagonales principal y secundarias
        VectorRestaJugador = []
        VectorRestaContrincante = []
        for i in range(4):
                VectorRestaJugador.append(xJugador[i]-yJugador[i])
                VectorRestaContrincante.append(xContrincante[i]-yContrincante[i])
                
        if (0 in VectorRestaContrincante):
            if ((VectorRestaContrincante.count(0)>1) or (VectorRestaContrincante.index(0)==1) or (VectorRestaContrincante.index(0)==2) or (VectorRestaContrincante.index(0)==3)): #tengo Negras en la diagonal, no me sirve
                contador =0
            else:
                contador = VectorRestaJugador.count(0)
        else:
            listaIndices = self.devolverIndices(VectorRestaJugador, 0)
            listaValores = self.devolverValores(yJugador, listaIndices)  
            if (0 in listaValores) and (4 in listaValores):
                contador = VectorRestaJugador.count(0)-1
            else:
                contador = VectorRestaJugador.count(0)
        if contador>x1:x1 = contador 
                
        if not (1 in VectorRestaContrincante):# no tengo contrincantes en la diagonal secundaria
           contador = VectorRestaJugador.count(1)
        if contador>x1:x1 = contador 
            
        if not (-1 in VectorRestaContrincante):# no tengo contrincantes en la diagonal secundaria superior
           contador = VectorRestaJugador.count(-1)
        if contador>x1:x1 = contador 
                
                
        #Diagonales inversa y secundarias
        VectorSumaJugador = []
        VectorSumaContrincante =[]
        for i in range(4):
                VectorSumaJugador.append(xJugador[i]+yJugador[i])
                VectorSumaContrincante.append(xContrincante[i]+yContrincante[i])
        
        if (4 in VectorSumaContrincante):
            if VectorSumaContrincante.count(4)>1 or VectorSumaContrincante.index(4)==1 or VectorSumaContrincante.index(4)==2 or VectorSumaContrincante.index(4)==3: #tengo Negras en la diagonal iversa, no me sirve
                contador =0
            else:
                contador = VectorSumaJugador.count(4)
        else:
            listaIndices = self.devolverIndices(VectorSumaJugador, 4)
            listaValores = self.devolverValores(yJugador, listaIndices)  
            if (0 in listaValores) and (4 in listaValores):
                contador = VectorSumaJugador.count(4)-1
            else:
                contador = VectorSumaJugador.count(4)
        if contador>x1:x1 = contador 
                
        if not (3 in VectorSumaContrincante):# no tengo contrincantes en la diagonal inversa secundaria
           contador = VectorSumaJugador.count(3)
        if contador>x1: x1 = contador 
            
        if not (5 in VectorSumaContrincante):# no tengo contrincantes en la diagonal inversa secundaria superior
           contador = VectorSumaJugador.count(5)
        if contador>x1: x1 = contador
        
        #Cuadrados
        listaCantidadAdyacentes =[]
        for i in range(4):
            if (self.adyacentes(xJugador[i], yJugador[i], xContrincante, yContrincante)==0):
                cantAdyJugador = self.adyacentes(xJugador[i], yJugador[i], xJugador, yJugador)
                listaCantidadAdyacentes.append(cantAdyJugador)
        if (listaCantidadAdyacentes.count(3)==4):
           contador = 4
        elif (listaCantidadAdyacentes.count(2)==3):
            contador = 3
        elif(listaCantidadAdyacentes.count(1)>=1):
            contador = 1
        if contador>x1: x1 = contador
    
        return x1
     
    # calcula la distancia maxima entre todas las fichas y se queda con el minimo
    def minDistanciasMaximas(self,xJugador, yJugador):   
        minDistanciaMax = 4
        for i in range(4):
            x1 = xJugador[i]
            y1 = yJugador[i]
            cont = 0
            for j in range(i,4):
                dist = self.distancia(x1,y1,xJugador[j],yJugador[j])
                if dist > cont:
                    cont = dist
            if cont< minDistanciaMax:
                minDistanciaMax = cont
        return minDistanciaMax
                  
    
    #devuelve una lista de indices de otra lista donde aparece un valor
    def devolverIndices(self,lista, valor):
        listaRes = []
        for i in range(len(lista)):
            if lista[i]== valor: listaRes.append(i)
        return listaRes
    
    
    #devuelve una lista de valores de una lista, dado una lista de indices
    def devolverValores(self,lista, listaIndices):
        listaRes = []
        for i in listaIndices:
            listaRes.append(lista[i])
        return listaRes    
    
    #calcula distancia
    def distancia(self,x1,x2,y1,y2):
        return max(abs(x1-x2),abs(y1-y2)) 
    
    #calcula cantidad de adyacentes
    def adyacentes(self,x,y, listaX, listaY):
        cantAdy = 0
        for i in range(4):
            x2= listaX[i]
            y2= listaY[i]
            if (self.distancia(x,y,x2,y2)==1):
                cantAdy += 1
            return cantAdy
    
    #verifica que una coordenada este ocupada
    def ocupado(self, x, y):
        ret = False
        for i in range(4):
            if (((self.xRojas[i]==x) and (self.yRojas[i]==y)) or 
                ((self.xNegras[i]==x) and (self.yNegras[i]==y))):
                ret = True
                break
        return ret
    
    #libera memoria
    def liberarMemoria(self):
        del self.xRojas
        del self.yRojas
        del self.xNegras
        del self.yNegras
    

            
            
        
                
                
                