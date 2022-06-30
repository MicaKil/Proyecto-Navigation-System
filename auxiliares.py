from algo1 import *
import random
import dictionary as d
import mylinkedlist_mica as mll
import myarray_mica as a
import Stack_Emmanuel as SE
import mypriorityqueue_mica as pq
import pickle
import math

"Verificación de fecha"
"---------------------------------------------------------------------------------"
# devuelve la tupla dia, mes y año de un string
def getDMY(date):
  day = None
  month = None
  year = None
  n = len(date)
  s = ''
  k = 0
  for i in range(n):
    if date[i] != '/' and date[i] != '\n':
      s += date[i]
    if date[i] == '/' or i == n-1:
      if k == 0:
        day = int(s)
      elif k == 1:
        month = int(s)
      elif k == 2:
        year = int(s)
      s = ''
      k += 1
  return (day,month,year)

#---------------------------------------------------------------------------------
# devuelve la cantidad de días en un mes
def maxDays(month): 
  if type(month) == str:
    month = int(month)
  if month == 2:
    return 28
  if month % 2 == 0: #si es mes par
    if month < 8: #antes de agosto
      return 30
    else: #desde agosto
      return 31
  else:
    if month < 8: #antes de agosto
      return 31
    else: #desde agosto
      return 30

#---------------------------------------------------------------------------------
# se fija que la fecha ingresada (string) del txt tenga el formato correcto
def checkDate(date): 
  (day,month,year) = getDMY(date)
  if day == None or month == None or year == None:
    print("Error: La fecha inicial no comple con el formato especificado dd/mm/yyyy.")
    return False
  if month > 12 or month < 1:
    print("Error: El mes debe estar entre 1 y 12.")
    return False
  if day != 1 or year != 2022:
    print("Error: La fecha debe ser 01/mm/2022.")
    return False
  return True

#---------------------------------------------------------------------------------
# se fija que la fecha ingresada (string) en las funciones tenga el formato correcto
def verifyDate(date, tabla): 
  # verificamos la fecha ingresada
  (day, month, year) = getDMY(date) 
  if day == None:
    print("Error: No se ingresó un día.")
    return False
  if (day < 1 or day > 31):
    print("Error: No es una fecha posible.")
    return False
  if month != None and (month < 1 or month > 12):
    print("Error: No es una fecha posible.")
    return False
  #comparemos con la fecha de la tabla
  fecha = tabla.date
  (dia, m, y) = getDMY(fecha)
  if month != None and month != m:
    print("Error: El mes ingresado no coincide con el del informe (%d)." % m)
    return False
  if year != None and year != y:
    print("Error: El año ingresado no coincide con el del informe (%d)." % y)
    return False
  #vericamos que sea un día posible (no supere los 28/30/31 diás según el mes)
  dias_max = maxDays(m) #calcula cantidad de días en el mes
  if day > dias_max:
    print("Error: No es una fecha posible.")
    return False
  return True

"Creación de Tabla"
"---------------------------------------------------------------------------------"
#crea una tabla hash a partir del txt
def create_table(flota):
  n = len(flota) 
  l = next_prime(1.25*n) #el tamaño de la tabla es un primo mayor a 1,25 * len(flota_list). Más de 1.25 no cambia mucho.
  D = Array(l, tuple())

  D.date = flota[0] #guardamos la fecha inicial como atributo de la tabla
  D.size = n - 1 #guardamos el número de embarcaciones

  for i in range(1,n):
    t = getInfo(flota[i])
    if t[3] != "N" and t[3] != "S" and t[3] != "E" and t[3] != "W" and t[3] != "NE" and t[3] != "NW" and t[3] != "SE" and t[3] != "SW":      
      print("Error. No es una dirección posible.")
      return None
    t_insert = d.insert(D,t[0], t, l)
    if t_insert == None:
      return None
  return D

#---------------------------------------------------------------------------------
#pasa la informacion de un string del txt a una tupla
def getInfo(string):
  str_val = ''
  e = mll.LinkedList()
  j = 0
  n = len(string)
  for i in range(n):
    if i != n - 1 and string[i] != ' ':
      str_val += string[i]
    else:
      if j == 1 or j == 2:
        str_val = int(str_val)
      if i == n - 1 and string[i] != '\n':
        str_val += string[i]
      mll.insert(e,str_val,j) #O(4)
      j += 1
      str_val = ''

  output = (e.head.value, e.head.nextNode.value, e.head.nextNode.nextNode.value, e.head.nextNode.nextNode.nextNode.value)
  return output

#---------------------------------------------------------------------------------
def next_prime(n):
  n = int(n)
  while is_prime(n) == False:
    n += 1
  return n

def is_prime(n):
  end = int(math.sqrt(n))+1
  for i in range(2,end):
    if (n%i) == 0:
      return False
  return True

"Obetener posición"
"---------------------------------------------------------------------------------"
#date es un día y value es una tupla (nombre, posicion inicial x, posicion inicial y, dirección)
def getPos(date,value): 
  if date == 1:
    return (value[1],value[2])

  x = value[1]
  y = value[2]
  direc = value[3]
  # direc[0] es la primer letra
  if direc[0] == 'N':
    y = y + date - 1
  elif direc[0] == 'S':
    y = y - date + 1
  elif direc[0] == 'W': #si no es ni N o S entonces solo se mueve en W o E
    x = x - date + 1
  elif direc[0] == 'E':
    x = x + date - 1
  #si la direccion de direc consiste en dos letras 
  if len(direc) > 1:
    if direc[1] == 'W': 
      x = x - date + 1
    elif direc[1] == 'E':
      x = x + date - 1
  
  return (x,y)

"Closest Pair"
"---------------------------------------------------------------------------------"
def closest(flota, day):
  n = flota.size #número de embarcaciones
  m = len(flota)

  Bx = Array(n, tuple()) # Barcos ordenados segun x
  By = Array(n, tuple()) # Barcos ordenados segun y

  k = 0
  for i in range(m):
    if flota[i] != None:
      boat = flota[i][1]
      (x, y) = getPos(day,boat) #calculamos la posición del barco en day
      Bx[k] = (boat[0], x ,y, boat[3])
      By[k] = (boat[0], x, y, boat[3])
      k += 1
  # ordenamos los barcos segun x y segun y (ascendente)
  mergesortMOD(Bx,'x')
  mergesortMOD(By,'y')
  BoatPairs = pq.PriorityQueue() # Min priority queue. Los pares con menor distancia tienen mayor prioridad.
  return closestR(Bx, By, BoatPairs)

#---------------------------------------------------------------------------------
def closestR(Bx, By, BoatPairs):
  lenBx = len(Bx)
  if lenBx <= 3:
    return closestBF(Bx, BoatPairs) #O(1)
  else:
    mid = lenBx // 2
    mid_x = Bx[mid][1] #coordenada x media
    #separamos los barcos en dos arreglos segun su posicion respecto a mid_x
    BxW = Array(mid, tuple()) #Barcos ordenados segun x al Oeste de mid_x
    BxE = Array(lenBx - mid, tuple()) #Barcos ordenados segun x al Este de mid_x
    for i in range(mid):
      BxW[i] = Bx[i]
    k = 0
    for i in range(mid,lenBx):
      BxE[k] = Bx[i]
      k += 1
    #separamos los barcos en dos arreglos segun su posicion respecto a mid_x
    lenBy = len(By)
    ByW = Array(lenBy, tuple()) #Barcos ordenados segun x al Oeste de mid_x
    ByE = Array(lenBy, tuple()) #Barcos ordenados segun x al Este de mid_x
    iW = 0
    iE = 0
    #print(lenBy, lenBx)
    for i in range(lenBy):
      if By[i][1] < mid_x:
        ByW[iW] = By[i]
        #print(iW,i)
        iW += 1
      else:
        ByE[iE] = By[i]
        iE += 1
    # al usar un arreglo puede haber espaciones en None
    ByW = a.createSet(ByW) # los eliminamos
    ByE = a.createSet(ByE) # O(n)
    # buscamos la distancia más corta delta
    deltaW = closestR(BxW, ByW, BoatPairs)
    deltaE = closestR(BxE, ByE, BoatPairs)

    if deltaW[0] < deltaE[0]:
      delta = deltaW[0]
    else:
      delta = deltaE[0]

    # comparamos lo elementos en la banda delimitada por delta
    band = Array(lenBy, tuple())
    for i in range(lenBy):
      if (mid_x - delta) <= By[i][1] <= (mid_x + delta):
        band[i] = By[i]
    band = a.createSet(band) 
    lenBand = len(band)
    # nos quedamos con la distancia más corta de esa banda
    for i in range(lenBand): # parece O(n^2)....
      end = min(i + 7, lenBand)
      for j in range(i + 1, end): # pero está probado que este bucle corre en cuanto mucho 7 veces [Ver Cormen ;)]
        d = dist(band[i], band[j])
        addToBoatPairs(BoatPairs, band[i],band[j], d)
        if delta > BoatPairs.head.value[2]:
          delta = BoatPairs.head.value[2]
    return (delta, BoatPairs) 

#---------------------------------------------------------------------------------
# calcula la distancia entre dos barcos por fuerza bruta
# la complejidad es nC2 (combinatorio) entonces si n = 3, 3C2 = 3 y, por lo tanto, O(1)
def closestBF(B, BoatPairs):
  if BoatPairs.head == None: #si no hay ningun par en la cola
    min_dist = 1e9 #min es + infinito
  else:
    min_dist = BoatPairs.head.value[2] #min es la distancia del primer par en la cola (menor distancia encontrada hasta ahora)
  n = len(B)
  for i in range(n):
    for j in range(i + 1, n):
      d = dist(B[i],B[j])
      addToBoatPairs(BoatPairs, B[i], B[j], d)
      if min_dist > BoatPairs.head.value[2]: 
        min_dist = BoatPairs.head.value[2]
  return (min_dist, BoatPairs)

#---------------------------------------------------------------------------------
def addToBoatPairs(BoatPairs, b1, b2, d):
  if BoatPairs.head == None:
    pq.enqueue_priority(BoatPairs, (b1[0], b2[0], d), - d) # -d para que sea un min-priority queue
  else:
    if d == BoatPairs.head.value[2] and ((mll.search(BoatPairs, (b1[0], b2[0], d)), mll.search(BoatPairs, (b2[0], b1[0], d))) == (None,None)): 
      pq.enqueue_priority(BoatPairs, (b1[0], b2[0], d), - d)
    if d < BoatPairs.head.value[2]:
      BoatPairs.head = None
      pq.enqueue_priority(BoatPairs, (b1[0], b2[0], d), - d)
  return BoatPairs

"Colission"
"---------------------------------------------------------------------------------"

#obtiene la direccion en un par (X,Y)
def DirIntFormat(Dir):
  if len(Dir)==1:
    if Dir=="W":
      X=-1
      Y=0
    elif Dir=="E":
      X=1
      Y=0
    elif Dir=="S":
      X=0
      Y=-1
    else:
      X=0
      Y=1
  else:
    if Dir[0]=='S':
      Y=-1
    else:
      Y=1
    if Dir[1]=='W':
      X=-1
    else:
      X=1
  return(X,Y)

#---------------------------------------------------------------------------------
#utilizando las posiciones inicial y las direcciones de los barcos, obtengo la relacion entre las distancias en cada eje
def obtainRelationDir(Barco1,Barco2):
  Dir1=Barco1[3]
  Pos1=(Barco1[1],Barco1[2])
  IntDir1=DirIntFormat(Dir1)
  Dir2=Barco2[3]
  Pos2=(Barco2[1],Barco2[2])
  IntDir2=DirIntFormat(Dir2)

  return(IntDir2[0]-IntDir1[0],IntDir2[1]-IntDir1[1])
  
#---------------------------------------------------------------------------------
#obtengo la distancia minima a lo largo del mes para un par de barcos
def obtainMinDist(Barco1,Barco2,date):
  #Formato Barco ("nombre",CoorX,CoorY,"Direccion")
  K=obtainRelationDir(Barco1,Barco2)
  #if K[0]!=K[1]:
    #print(K,Barco1,Barco2)
  a=K[0]*K[0]+K[1]*K[1]
  b=2*((Barco2[1]-Barco1[1])*K[0]+(Barco2[2]-Barco1[2])*K[1])

  #print(K,a,b)
  (day, month, year)=getDMY(date)
  lastDay=maxDays(month)-1
  
  #obtengo un candidato para el dia de distancia minima (junto a los extremos) y lo aproximo al entero mas cercano
  if a!=0:
    T=round(-b/(2*a))

  #obtengo los tres candidatos a distancia minima
  distInit=CalcDist(Barco1,Barco2,K,0)
  distFin=CalcDist(Barco1,Barco2,K,lastDay)
  if a!=0:
    distT=CalcDist(Barco1,Barco2,K,T)
    
  #determino cual es la distancia minima de las tres y la devuelvo
  if a!=0:
    dist=min(distInit,distFin,distT)
    if dist==distT:
      if T<=lastDay and T>=1:
        day=T+1
      elif dist==distFin:
        day=lastDay+1
      else:
        day=1
    elif dist==distFin:
      day=lastDay+1
    else:
      day=1
    return(dist,day)
  else:
    if distInit<distFin:
      dist=distInit
      day=1
    elif distInit>distFin:
      dist=distFin
      day=lastDay+1
    else:
      dist=distFin
      day=lastDay+1
      return(dist,day,"paralelos")
    return(dist,day)

#---------------------------------------------------------------------------------
def colisiones(flota):
  n=flota.size
  m=len(flota)
  date=flota.date
  
  Bx = Array(n, tuple()) # Barcos ordenados segun x
  k = 0
  for i in range(m):
    if flota[i] != None:
      boat = flota[i][1]
      Bx[k] = (boat[0],boat[1],boat[2],boat[3])
    k=k+1
  # ordenamos los barcos segun x y segun y (ascendente)
  mergesortMOD(Bx,'x')
  
  lista=mll.LinkedList()
  #para cada barco del arreglo
  for i in range(n):
    #obtengo el rango de riesgo y agrego a una lista los pares de barcos sospechosos
    lim=Limites(Bx[i],date)
    candidatos(Bx,Bx[i],lim,i,lista)

  Resultado=mll.LinkedList()
  Cur=lista.head
  cont=0
  while Cur!=None:
    #viajando por la lista obtengo la distancia minima de cada par
    #de entrar en riesgo de colision, se agrega a la lista resultado, junto
    #a la fecha del incidente
    Temp=obtainMinDist(Cur.value[0],Cur.value[1],date)
    if Temp[0]<=1:
      if len(Temp)!=3:
        cont=cont+1
        #print("El día %s, los barcos %s y %s estuvieron en riesgo de colisión." %(Temp[1],Cur.value[0][0],Cur.value[1][0]))
        mll.add(Resultado,(Cur.value[0],Cur.value[1],Temp[1]))
      else:
        cont=cont+1
        #print ("Los barcos %s y %s viajaron en paralelo en riesgo de colisión durante todo el mes." %(Cur.value[0][0],Cur.value[1][0]))
        mll.add(Resultado,(Cur.value[0],Cur.value[1],Temp[1],"el par de barcos estuvo en riesgo de colision todo el mes por viajar en paralelo."))
    Cur=Cur.nextNode
  
  res=Array(cont,tuple())
  cur=Resultado.head
  for i in range(cont):
    res[i]=cur.value
    cur=cur.nextNode

  mergesortMOD(res,'day')
 
  return(res)

#---------------------------------------------------------------------------------
def candidatos(Flota,Barco,Lims,Cont,Lista):
  #obtengo la lista de candidatos a par en riesgo de colision
  
  lenFlota=len(Flota)
  mid=lenFlota//2
  CurBarco=Flota[mid]
  #busco el barco mas cercano en x al x final del barco elegido

  k=ObtainStartingPoint(Flota,Lims[2])
  
  temp=k
  antirepe=k
  while temp!=0 and Flota[temp][1]>=Lims[0][0]:
    if Flota[temp][2]>=Lims[1][0] and Flota[temp][2]<=Lims[1][1]:
      if Barco[0]!=Flota[temp][0] and temp>Cont:
        mll.add(Lista,(Barco,Flota[temp]))
        antirepe=temp
    temp=temp-1
  temp=k
  while temp!=lenFlota and Flota[temp][1]<=Lims[0][1]:
    if Flota[temp][2]>=Lims[1][0] and Flota[temp][2]<=Lims[1][1]:
      if Barco[0]!=Flota[temp][0] and temp>Cont and temp!=antirepe:
        mll.add(Lista,(Barco,Flota[temp]))
    temp=temp+1

#---------------------------------------------------------------------------------
def ObtainStartingPoint(Flota,PosBus):
  #obtengo la posicion desde la que empiezo a seleccion de candidatos
  lenFlota=len(Flota)
  mid=lenFlota//2
  CurBarco=Flota[mid]
  
  k=mid
  found=False
  prevK=lenFlota
  while found==False:
    #si la posicion final del barco en X coincide con el X de otro Barco
    if Flota[k][1]==PosBus[0]:
      found=True
    else:
      #si pos final X del barco es mayor al X del barco actual
      if Flota[k][1]<PosBus[0]:
        #si llegue al final de la lista devuelvo ese X
        if k==lenFlota-1:
          found=True
        else:
          #si el X del siguiente barco es menor o igual al Barco seleccionado, entonces encontre el X mas cercano a la pos final
          if Flota[k+1][1]>=PosBus[0]:
            found=True
          else:
            #si no, avanzo el x
            if mid>1:
              k=k+mid//2
            else:
              k=k+1
      #si pos final X del barco es menor al X del barco actual
      else:
        #si llegue al principio de la lista devuelvo ese X
        if k==0:
          found=True
        else:
          #si el X del siguiente barco es mayor o igual al Barco seleccionado, entonces encontre el X mas cercano a la pos final
          if Flota[k-1][1]<=PosBus[0]:
            k=k-1
            found=True
          else:
            #si no, retrocedo el x
            if mid>1:
              k=k-mid//2
            else:
              k=k-1
    if mid>1:
      mid=mid//2
    #print(k)
  #print("k:",k,"barco",Flota[k])
  return(k)

#---------------------------------------------------------------------------------  
def Limites(Barco,date):
  #obtengo los limites del rango de alerta + la posicion final del barco
  Dir=DirIntFormat(Barco[3])
  (d,month,y)=getDMY(date)
  lastDay=maxDays(month)
  finalPos=(Barco[1]+Dir[0]*lastDay,Barco[2]+Dir[1]*lastDay)
  
  cor=Array(3,tuple())
  cor[0]=(finalPos[0]-lastDay-1,finalPos[0]+lastDay+1)
  cor[1]=(finalPos[1]-lastDay-1,finalPos[1]+lastDay+1)
  cor[2]=finalPos
  #formato: ((limite x menor, limite x mayor),(limite y menor, limite y mayor),(posicion x final,posicion y final))
  return(cor)

"MERGE SORT MODIFICACIONES"
'---------------------------------------------------------------------------------'
# Merge Sort Modificado para ordenar barcos según coordenada x o y 
# L es un arreglo de tuplas (nombre, pos inicial en x, pos inicial en y, dirección) y coordinate puede ser 'x' o 'y'
def mergesortMOD(L, coordinate): 
  l = len(L)
  if l > 1:
    m1 = l // 2 #división entera
    #Divido la lista en dos partes.
    Left = Array(m1, tuple()) #Parte izquierda.
    for i in range(0,m1):
      Left[i] = L[i]
    Right = Array(l - m1, tuple()) #Parte derecha.
    k = 0
    for j in range(m1, l): #empieza donde termina left
      Right[k] = L[j]
      k = k + 1
    mergesortMOD(Left, coordinate) #Ordena la parte izquierda...
    mergesortMOD(Right, coordinate) #y la derecha.
    i = 0
    j = 0
    k = 0
    if coordinate == 'x':
      n = 1
    elif coordinate == 'y':
      n = 2
    else:
      n = 2
    while i < len(Left) and j < len(Right):
      if Left[i][n] < Right[j][n]: #Si la izquierda es menor que la derecha...
        L[k] = Left[i]
        i = i + 1
      else:
        L[k] = Right[j]
        j = j + 1
      k = k + 1
    #Guardo elementos restantes (si es que hay)
    while i < len(Left):
      L[k] = Left[i]
      i = i + 1
      k = k + 1
    while j < len(Right):
      L[k] = Right[j]
      j = j + 1
      k = k + 1

"Ranking"
"---------------------------------------------------------------------------------"

def ranking(flota, day):
  n = flota.size #número de embarcaciones
  m = len(flota)

  Bx = Array(n, tuple()) # Barcos ordenados segun x
  By = Array(n, tuple()) # Barcos ordenados segun y

  k = 0
  for i in range(m):
    if flota[i] != None:
      boat = flota[i][1]
      b_pos = getPos(day,boat) #calculamos la posición del barco en day
      Bx[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      By[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      k += 1
  # ordenamos los barcos segun x y segun y (ascendente)
  mergesortMOD(Bx,'x')
  mergesortMOD(By,'y')
  rank = pq.PriorityQueue() #max priority queue -> se encolan los pares de barcos con mayor distancia al principio
  return rankingR(Bx, By, rank)

#---------------------------------------------------------------------------------
def rankingR(Bx, By, rank):
  lenBx = len(Bx)
  if lenBx <= 3:
    return rankingBF(Bx, rank) #O(1)
  else:
    mid = lenBx // 2
    mid_x = Bx[mid][1] #coordenada x media
    #separamos los barcos en dos arreglos segun su posicion respecto a mid_x
    BxW = Array(mid, tuple()) #Barcos ordenados segun x al Oeste de mid_x
    BxE = Array(lenBx - mid, tuple()) #Barcos ordenados segun x al Este de mid_x
    for i in range(mid):
      BxW[i] = Bx[i]
    k = 0
    for i in range(mid,lenBx):
      BxE[k] = Bx[i]
      k += 1
    #separamos los barcos en dos arreglos segun su posicion respecto a mid_x
    lenBy = len(By)
    ByW = Array(lenBy, tuple()) #Barcos ordenados segun x al Oeste de mid_x
    ByE = Array(lenBy, tuple()) #Barcos ordenados segun x al Este de mid_x
    iW = 0
    iE = 0
    
    for i in range(lenBy):
      if By[i][1] < mid_x:
        ByW[iW] = By[i]
        iW += 1
      else:
        ByE[iE] = By[i]
        iE += 1
    # al usar un arreglo puede haber espaciones en None
    ByW = a.createSet(ByW) # los eliminamos
    ByE = a.createSet(ByE) # O(n)
    # buscamos la distancia más corta delta
    (deltaW, boatPW) = rankingR(BxW, ByW, rank) 
    (deltaE, boatPE) = rankingR(BxE, ByE, rank)

    bp = mll.LinkedList()
    if deltaW < deltaE:
      delta = deltaW
      cur = boatPW.head  
      while cur != None:
        mll.insert(bp, cur.value, mll.length(bp))
        cur = cur.nextNode
    else:
      delta = deltaE
      cur = boatPE.head
      while cur != None:
        mll.insert(bp, cur.value, mll.length(bp))
        cur = cur.nextNode

    # comparamos lo elementos en la banda delimitada por delta
    band = Array(lenBy, tuple())
    for i in range(lenBy):
      if (mid_x - delta) <= By[i][1] <= (mid_x + delta):
        band[i] = By[i]
    band = a.createSet(band) 
    lenBand = len(band)
    # nos quedamos con la distancia más corta de esa banda
    for i in range(lenBand): 
      end = min(i + 7, lenBand) # no sé cuantos elementos deberían haber en la banda
      for j in range(i + 1, end): 
        addToRank(rank, band[i], band[j], delta)
        delta = rank.head.value[2] #la cota superior la da el primer elemento de la cola
    return (delta, rank) 

#---------------------------------------------------------------------------------
# calcula la distancia entre dos barcos por fuerza bruta
# la complejidad es nC2 (combinatorio) entonces si n = 3, 3C2 = 3 y, por lo tanto, O(1)
def rankingBF(B, rank):
  if rank.head == None:
    delta = 1e9
  else:
    delta = rank.head.value[2] #la menor distancia la da el primer elemento de la cola

  n = len(B)
  for i in range(n):
    for j in range(i + 1, n):
      addToRank(rank, B[i], B[j], delta)
      delta = rank.head.value[2] #la cota superior la da el primer elemento de la cola
  return (delta, rank)

# Nota: delta no es necesariamente la mínima distancia entre dos barcos
      # delta sería la mayor distancia (cota superior) entre un grupo de 5 pares de barcos

#---------------------------------------------------------------------------------
def addToRank(rank, b1, b2, delta):
  d = dist(b1, b2)
  if rank.head == None:
    pq.enqueue_priority(rank, (b1[0], b2[0], d), d)
  else:
    if d > delta:
      return rank
    # si el elemento no se encuentra en la cola...
    if (mll.search(rank, (b1[0], b2[0], d)), mll.search(rank, (b2[0], b1[0], d))) == (None,None):
      if d == delta: # si la distancia es igual a delta 
        pq.enqueue_priority(rank, (b1[0], b2[0], d), d)
      else:
        l = mll.length(rank)
        if d < delta:
          if l < 5 : # si la cola tiene menos de 5 elementos... 
            pq.enqueue_priority(rank, (b1[0], b2[0], d), d) #se agrega el nuevo elemento 
          else: # sino...
            count = 0
            cur = rank.head
            old_delta = delta
            # calcula que elementos debe eliminar
            while cur != None and (l - count) >= 5:  
              if cur.value[2] != old_delta:
                old_delta = cur.value[2]
              count += 1
              cur = cur.nextNode
            while cur != None and cur.value[2] == old_delta:
              count += 1
              cur = cur.nextNode
            if l - count >= 4:
              while count > 0:
                pq.dequeue_priority(rank)
                count -= 1
            else:
              while rank.head != None and rank.head.value[2] != old_delta:
                pq.dequeue_priority(rank)
            pq.enqueue_priority(rank, (b1[0], b2[0], d), d)
  return rank

# Operaciones con PriorityQueue tiene aproximadamente O(1) ya que van a haber 5 elementos aprox

"Funciones para calcular la distancia"
"---------------------------------------------------------------------------------"
#calcula la distancia entre dos barcos cuya posición desconocemos
def getDistance(b1, b2, date):
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)

  #buscamos a los barcos b1 y b2 en la tabla
  b1_info = d.search(flota,b1)
  if b1_info == None:
    print("Error. No se encontró b1.")
    return None
  b2_info = d.search(flota,b2)
  if b2_info == None:
    print("Error. No se encontró b2.")
    return None

  b1_pos = getPos(date,b1_info)
  b2_pos = getPos(date,b2_info)
  dist = dist(b1_pos,b2_pos) 
  return dist

#---------------------------------------------------------------------------------
# Dado dos barcos A y B (nombre, coordenada x, coordenada y, direccion) calcula su distancia 
def dist(A, B):
  return math.sqrt(((A[1] - B[1])**2)+((A[2] - B[2])**2))

#---------------------------------------------------------------------------------
# Dados dos barcos b1 y b2, junto a su relacion de movimiento y el dia en el mes. calcula su distancia
def CalcDist(b1,b2,K,T):
  return(math.sqrt(pow(b2[1]-b1[1]+K[0]*T,2)+pow(b2[2]-b1[2]+K[1]*T,2)))

"================================================================================="
"EXTRAS" 

# las funciones create_flotatxt y random_month no están en pseudo-python porque no va a ser usadas en el programa ppal
# su unico propósito es generar un txt para testeo 
def create_flotatxt(n):
  direccion = ["N","S","E","W","NE","NW","SE","SW"]

  flota_m = []
  flota_m.append(random_month())

  num_flota = []
  coor_flota = []

  for i in range(1,n + 1): #en 0 está la fecha
    #se guardan los nombres y coordenadas en "uso"
    #no hay do - while en python y ni ganas de buscar alternativa inteligente
    num = random.randrange(0,n+1)
    while num in num_flota: #para no tener barcos con el mismo nombre
      num = random.randrange(0,n+1)
    num_flota.append(num)

    coor = (random.randrange(-n,n),random.randrange(-n,n))
    while coor in  coor_flota: #o misma coordena 
      coor = (random.randrange(-n,n),random.randrange(-n,n))
    coor_flota.append(coor)

    flota_m.append("b"+str(num)+" "+str(coor[0])+" "+str(coor[1])+" "+direccion[random.randrange(8)])

  with open('flota.txt', 'w') as f: #si no exite el archivo flota lo crea
    f.write('\n'.join(flota_m))

#---------------------------------------------------------------------------------
# genera un mes random para la lista de los barcos
def random_month():
  mes = random.randint(1,12)
  if mes < 10:
    mes = str(mes)
    mes = "0" + mes 
  else:
    mes = str(mes)
  return "01/"+ mes + "/2022"

def create_fleet():
  result = []
  directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']

  # Random points.
  for i in range(20):
    point_r1 = (random.randrange(100), random.randrange(100), directions[random.randrange(len(directions) - 1)])
    point_r2 = (random.randrange(100), random.randrange(100), directions[random.randrange(len(directions) - 1)])
    result.append(point_r1)
    result.append(point_r2)
  #Lateral point. Estos barcos van a tener riesgo de colision el dia 10 y el 11.
  for i in range(20):
    point_left = (-10, i, 'E')
    point_right = (10, i, 'W')
    result.append(point_left)
    result.append(point_right)
  #Vertical point. Estos barcos van a tener riesgo de colision el dia 5.
  for i in range(20):
    point_down = (i+12, -5, 'N')
    point_up = (i+12, 4, 'S')
    result.append(point_down)
    result.append(point_up)
  #Diagonal point. Estos barcos van a tener riesgo de colision los primeros 20 dias pues van por la misma diagonal.
  for i in range(20):
    point_up = (i, i, 'SW')
    point_down = (-i, -i, 'NE')
    result.append(point_up)
    result.append(point_down)
  # Random points
  for i in range(20):
    point_r1 = (random.randrange(100), random.randrange(100), directions[random.randrange(len(directions) - 1)])
    point_r2 = (random.randrange(100), random.randrange(100), directions[random.randrange(len(directions) - 1)])
    result.append(point_r1)
    result.append(point_r2)
  return result

"---------------------------------------------------------------------------------"
"FUNCIONES PICKLE"

#copie y pegué para poder acceder a estas luego en caso de ser necesario

# with open('tabla_flota.txt', 'wb') as f: #lo serializamos
#   pickle.dump(flota,f)

# with open('tabla_flota.txt', 'rb') as f: #deserializacion
#   flota = pickle.load(f)

