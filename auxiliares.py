from algo1 import *
import random
import dictionary as d
import mylinkedlist_mica as mll
import myarray_mica as a
import Stack_Emmanuel as SE
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
    if date[i] != '/':
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
  l = next_prime(1.5*n) #el tamaño de la tabla es un primo mayor a 1,5 * len(flota_list)
  D = Array(l,tuple())

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
  for i in range(1,len(string)):
    if string[i] != ',' and string[i] != ')':
      str_val += string[i]
    else:
      if j == 1 or j == 2:
        str_val = int(str_val)
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
      b_pos = getPos(day,boat) #calculamos la posición del barco en day
      Bx[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      By[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      k += 1
  # ordenamos los barcos segun x y segun y (ascendente)
  mergesortMOD(Bx,'x')
  mergesortMOD(By,'y')
  BoatPairs = mll.LinkedList()
  return closestR(Bx, By, BoatPairs)

#---------------------------------------------------------------------------------
def closestR(Bx, By, BPairs):
  lenBx = len(Bx)
  if lenBx <= 3:
    return closestBF(Bx, BPairs) #O(1)
  else:
    mid = lenBx//2
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
    ByW = Array(lenBx, tuple()) #Barcos ordenados segun x al Oeste de mid_x
    ByE = Array(lenBx, tuple()) #Barcos ordenados segun x al Este de mid_x
    iW = 0
    iE = 0
    lenBy = len(By)
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
    (deltaW, boatPW) = closestR(BxW, ByW, BPairs) 
    (deltaE, boatPE) = closestR(BxE, ByE, BPairs)

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
    for i in range(lenBand): # parece O(n^2)....
      end = min(i + 7, lenBand)
      for j in range(i + 1, end): # pero está probado que este bucle corre en cuanto mucho 7 veces [Ver Cormen ;)]
        d = dist(band[i], band[j])
        if d == delta and ((mll.search(bp, (band[i][0], band[j][0], d)), mll.search(bp, (band[j][0], band[i][0], d))) == (None, None)):
          mll.add(bp, (band[i][0], band[j][0], d))
        if d < delta:
          delta = d
          bp.head = None
          mll.add(bp, (band[i][0], band[j][0], d))
    addToBPairs(BPairs, bp, delta)
    return (delta, BPairs) 

#---------------------------------------------------------------------------------
# calcula la distancia entre dos barcos por fuerza bruta
# la complejidad es nC2 (combinatorio) entonces si n = 3, 3C2 = 3 y, por lo tanto, O(1)
def closestBF(B, BPairs):
  min_dist = 1e9
  bp = mll.LinkedList()
  n = len(B)
  for i in range(n):
    for j in range(i + 1, n):
      d = dist(B[i],B[j])
      if d == min_dist and ((mll.search(bp, (B[i][0], B[j][0], d)), mll.search(bp, (B[j][0], B[i][0], d))) == (None,None)): #O(1) en cuanto mucho hay tres elementos
        mll.add(bp, (B[i][0], B[j][0], d))
      if d < min_dist:
        min_dist = d
        bp.head = None
        mll.add(bp, (B[i][0], B[j][0], d))  
  addToBPairs(BPairs, bp, min_dist)
  return (min_dist, BPairs)

#---------------------------------------------------------------------------------
def addToBPairs(BPairs, bp, d):
  if BPairs.head != None and BPairs.head.value[2] == d:
    cur = bp.head
    while cur != None:
      if ((mll.search(BPairs, cur.value), mll.search(BPairs, (cur.value[1], cur.value[0], d))) == (None, None)):
        mll.add(BPairs, cur.value)
      cur = cur.nextNode
  if BPairs.head == None or (BPairs.head != None and BPairs.head.value[2] > d):
    BPairs.head = None
    cur = bp.head
    while cur != None:
      mll.add(BPairs, cur.value)
      cur = cur.nextNode
  return BPairs
#---------------------------------------------------------------------------------
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

  RelDirX=IntDir2[0]-IntDir1[0]
  if Pos1[0]<Pos2[0]:
    RelDirX=-RelDirX
  elif Pos1[0]==Pos2[0]:
    RelDirX=abs(RelDirX)

  RelDirY=IntDir2[1]-IntDir1[1]
  if Pos1[1]>Pos2[1]:
    RelDirY=-RelDirY
  elif Pos1[1]==Pos2[1]:
    RelDirY=abs(RelDirY)

  return(RelDirX,RelDirY)
#---------------------------------------------------------------------------------
#obtengo la distancia minima a lo largo del mes para un par de barcos
def obtainMinDist(Barco1,Barco2,date):
  #Formato Barco ("nombre",CoorX,CoorY,"Direccion")
  K=obtainRelationDir(Barco1,Barco2)
  a=K[0]*K[0]+K[1]*K[1]
  b=2*((Barco1[1]-Barco2[1])*K[0]+(Barco1[2]-Barco2[2])*K[1])

  #print(K)
  #print(a,b)
  (day, month, year)=getDMY(date)
  lastDay=maxDays(month)
  
  #obtengo un candidato para el dia de distancia minima (junto a los extremos) y lo aproximo al entero mas cercano
  if a!=0:
    T=-b/(2*a)
    Tfloor=int(T)
    Tceil=Tfloor+1
    #print(T,Tfloor,Tceil)
    if T-Tfloor<=Tceil-T:
      T=Tfloor
    else:
      T=Tceil

  #obtengo los tres candidatos a distancia minima
  distInit=CalcDist(Barco1,Barco2,K,0)
  distFin=CalcDist(Barco1,Barco2,K,lastDay)
  if a!=0:
    distT=CalcDist(Barco1,Barco2,K,T)

  #print(distInit,distFin,distT)
  
  #determino cual es la distancia minima de las tres y la devuelvo
  if a!=0:
    if distInit<=distFin:
      if T>1 and T<lastDay:
        if distT<=distInit:
          dist=distT
          day=T
        else:
          dist=distInit
          day=1
      else:
        dist=distInit
        day=1
    else:
      if T>1 and T<lastDay:
        if distT<=distFin:
          dist=distT
          day=T
        else:
          dist=distFin
          day=lastDay
      else:
        dist=distFin
        day=lastDay
    return(dist,day)
  else:
    if distInit<distFin:
      dist=distInit
      day=1
    elif distInit>distFin:
      dist=distFin
      day=lastDay
    else:
      dist=distFin
      day=lastDay
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
  
  #for i in range(20):
  #  print(Bx[i])
  #print("------------------------------------------------------------")
  
  lista=mll.LinkedList()
  #para cada barco del arreglo
  for i in range(n):
    #obtengo el rango de riesgo y agrego a una lista los pares de barcos sospechosos
    lim=Limites(Bx[i],date)
    #print(lim)
    candidatos(Bx,Bx[i],lim,i,lista)
  #print("termine candidatos")

  #Cur=lista.head
  #while Cur!=None:
  #  print(Cur.value)
  #  Cur=Cur.nextNode
  #print("")
  #print("------------------------------------------------------------")
  
  Resultado=mll.LinkedList()
  Cur=lista.head
  while Cur!=None:
    #viajando por la lista obtengo la distancia minima de cada par
    #de entrar en riesgo de colision, se agrega a la lista resultado, junto
    #a la fecha del incidente
    Temp=obtainMinDist(Cur.value[0],Cur.value[1],date)
    if Temp[0]==1:
      if len(Temp)!=3:
        mll.add(Resultado,(Cur.value[0],Cur.value[1],Temp[1]))
      else:
        mll.add(Resultado,(Cur.value[0],Cur.value[1],Temp[1],"el par de barcos estuvo en riesgo de colision todo el mes por viajar en paralelo"))
    Cur=Cur.nextNode

  #Cur=Resultado.head
  #while Cur!=None:
  #  print(Cur.value)
  #  Cur=Cur.nextNode
  #print("")
  
  return(mergesortListasMOD(Resultado,2))
#---------------------------------------------------------------------------------
def candidatos(Flota,Barco,Lims,Cont,Lista):
  #obtengo la lista de candidatos a par en riesgo de colision
  
  lenFlota=len(Flota)
  mid=lenFlota//2
  CurBarco=Flota[mid]
  #busco el barco mas cercano en x al x final del barco elegido

  k=ObtainStartingPoint(Flota,Lims[2])

  q=k-1
  if q>=0:
    #me vuelvo en el arreglo hasta alcanzar aquellos fuera de riesgo
    while Flota[q][1]>=Lims[0][0]:
      if q>Cont:
        #si tambien estan en zona de riesgo en y, los agrego a la lista
        if Flota[q][2]>=Lims[1][0] and Flota[q][2]<=Lims[1][1]:
          #print(Barco,Flota[q])
          mll.add(Lista,(Barco,Flota[q]))
      q=q-1
      if q<=0:
        break
  q=k+1
  if q<=lenFlota-1:
    #avanzo en el arreglo hasta alcanzar aquellos fuera de riesgo
    while Flota[q][1]<=Lims[0][1]:
      if q>Cont:
        #si tambien estan en zona de riesgo en y, los agrego a la lista
        if Flota[q][2]>=Lims[1][0] and Flota[q][2]<=Lims[1][1]:
          #print(Barco,Flota[q])
          mll.add(Lista,(Barco,Flota[q]))
      q=q+1
      if q>=lenFlota:
        break
  #print("------------------------------------------------------------")
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
    #if k!=prevK:
    #  print("posX:",Flota[k][1],"objX:",PosBus[0],"k:",k,"mid:",mid)
    #prevK=k
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

#print(obtainMinDist(("B1",-15,13,"NE"),("B2",18,-11,"SE"),"01/05/2022"))
#print(obtainMinDist(("B1",-1,0,"NE"),("B2",5,1,"NW"),"01/05/2022"))
#print(Limites(("B1",-15,13,"NE"),"01/05/2022"))

#---------------------------------------------------------------------------------
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
#---------------------------------------------------------------------------------
# Merge Sort Modificado para ordenar listas según enteros en la posicion pos
 def mergesortListasMOD(L,pos):
  Lar=mll.length(L)
  Med=int(Lar/2)

  if Lar<=1:
    return(L)

  left=mll.LinkedList()
  right=mll.LinkedList()

  Cur=L.head
  for i in range(Lar):
    if i<Med:
      mll.add(left,Cur.value)
    else:
      mll.add(right,Cur.value)
    Cur=Cur.nextNode

  left=mergesortListasMOD(left,pos)
  right=mergesortListasMOD(right,pos)

  L=merge(left,right,pos)
  return (L)

def merge(left,right,pos):
  mergedList=mll.LinkedList()

  CurL=left.head
  CurR=right.head

  while CurL!=None and CurR!=None:
    if CurL.value[pos] <= CurR.value[pos]:
      SE.push(mergedList,SE.pop(left))
      CurL=left.head
    else:
      SE.push(mergedList,SE.pop(right))
      CurR=right.head

  while CurL!=None:
    SE.push(mergedList,SE.pop(left))
    CurL=left.head
  while CurR!=None:
    SE.push(mergedList,SE.pop(right))
    CurR=right.head
  
  Cur=mergedList.head
  mll.inverse(mergedList)

  return(mergedList)
     
 
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
  return(math.sqrt((b1[1]-b2[1]+K[0]*T)*(b1[1]-b2[1]+K[0]*T)+(b1[2]-b2[2]+K[1]*T)*(b1[2]-b2[2]+K[1]*T)))





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

    flota_m.append("(b"+str(num)+","+str(coor[0])+","+str(coor[1])+","+direccion[random.randrange(8)]+")")

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

    
"---------------------------------------------------------------------------------"
"FUNCIONES PICKLE"

#copie y pegué para poder acceder a estas luego en caso de ser necesario

# with open('tabla_flota.txt', 'wb') as f: #lo serializamos
#   pickle.dump(flota,f)

# with open('tabla_flota.txt', 'rb') as f: #deserializacion
#   flota = pickle.load(f)
