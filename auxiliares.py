from algo1 import *
import random
import sympy #para buscar un número primo
import copy
import dictionary_universal as d
import mylinkedlist_mica as mll
import myarray_mica as a
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
  fecha = d.search(tabla,'fecha')
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
  l = sympy.nextprime(1.5*n) #el tamaño de la tabla es un primo mayor a 1,5 * len(flota_list) 
  D = Array(l,mll.LinkedList())

  L_ab = mll.LinkedList() #para guardar los (a,b) usados en universal hashing
  with open('lista_ab.txt', 'wb') as f: #lo serializamos
    pickle.dump(L_ab,f)

  d.insert(D,'fecha',flota[0]) #se resevar la key "fecha" para la fecha
  d.insert(D,'navysize', n - 1) #guarda el número de embarcaciones

  for i in range(1,n):
    t = getInfo(flota[i])
    if t[3] != "N" and t[3] != "S" and t[3] != "E" and t[3] != "W" and t[3] != "NE" and t[3] != "NW" and t[3] != "SE" and t[3] != "SW":
      print("Error. No es una dirección posible.")
      return None
    d.insert(D,t[0], t)

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
      mll.insert(e,str_val,j)
      j += 1
      str_val = ''

  output = (e.head.value, e.head.nextNode.value, e.head.nextNode.nextNode.value, e.head.nextNode.nextNode.nextNode.value)
  return output

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
  n = d.search(flota,'navysize') #número de embarcaciones
  m = len(flota)

  Bx = Array(n, tuple()) # Barcos ordenados segun x
  By = Array(n, tuple()) # Barcos ordenados segun y

  k = 0
  for i in range(m):
    if flota[i] != None and flota[i].head.value[0] != 'fecha' and flota[i].head.value[0] != 'navysize':
      boat = flota[i].head.value[1]
      b_pos = getPos(day,boat) #calculamos la posición del barco en day
      Bx[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      By[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      k += 1
  # ordenamos los barcos segun x y segun y (ascendente)
  mergesortMOD(Bx,'x')
  mergesortMOD(By,'y')
  # print("Bx")
  # print(Bx)
  # print("By")
  # print(By)
  BoatPairs = mll.LinkedList()
  return closestR(Bx, By, BoatPairs)

#---------------------------------------------------------------------------------
def closestR(Bx, By, BPairs):
  lenBx = len(Bx)
  if lenBx <= 3:
    #print("Brute Force", Bx)
    return closestBF(Bx, BPairs) #O(1)
  else:
    mid = lenBx//2
    mid_x = Bx[mid][1] #coordenada x media
    # print("n:", lenBx, "mid:", mid, "mid_x:", mid_x)
    # print("Bx")
    # print(Bx)
    # print("By")
    # print(By)
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
      cur = boatPW.head #Si me dejan usar copy no hace falta este while
      while cur != None:
        mll.insert(bp, cur.value, mll.length(bp))
        cur = cur.nextNode
      #bp = copy.deepcopy(boatPW) 
    else:
      delta = deltaE
      cur = boatPE.head
      while cur != None:
        mll.insert(bp, cur.value, mll.length(bp))
        cur = cur.nextNode
      #bp = copy.deepcopy(boatPE)

    # comparamos lo elementos en la banda delimitada por delta
    band = Array(lenBy, tuple())
    for i in range(lenBy):
      if (mid_x - delta) <= By[i][1] <= (mid_x + delta):
        band[i] = By[i]
    band = a.createSet(band) 
    #print("Banda", band)
    lenBand = len(band)
    # nos quedamos con la distancia más corta de esa banda
    for i in range(lenBand): # parece O(n^2)....
      end = min(i + 7, lenBand)
      for j in range(i + 1, end): # pero está probado que este bucle corre en cuanto mucho 7 veces [Ver Cormen ;)]
        d = dist(band[i], band[j])
        #print("smart:", band[i], band[j])
        if d == delta and ((mll.search(bp, (band[i][0], band[j][0], d)), mll.search(bp, (band[j][0], band[i][0], d))) == (None, None)):
          mll.add(bp, (band[i][0], band[j][0], d))
          # print("here TOP 1")
          # mll.printh(BPairs)
          # mll.printh(bp) 
        if d < delta:
          delta = d
          # print(d, delta)
          # print("here TOP 2")
          # mll.printh(BPairs)
          # mll.printh(bp)
          bp.head = None
          # print("here TOP 2.5")
          # mll.printh(BPairs)
          # mll.printh(bp)
          mll.add(bp, (band[i][0], band[j][0], d))
    #       print("here TOP 3")
    #       mll.printh(BPairs)
    #       mll.printh(bp)
    # print("wtf")
    # mll.printh(BPairs)
    # mll.printh(bp)
    addToBPairs(BPairs, bp, delta)
    # print("wth")
    # mll.printh(BPairs)
    # mll.printh(bp)
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
        # print("here BF 1")  
        # mll.printh(BPairs)
        # mll.printh(bp)
      if d < min_dist:
        min_dist = d
        bp.head = None
        mll.add(bp, (B[i][0], B[j][0], d))
        # print("here BF 2")  
        # mll.printh(BPairs)
        # mll.printh(bp)
       

  addToBPairs(BPairs, bp, min_dist)
  return (min_dist, BPairs)
  
def addToBPairs(BPairs, bp, d):
  if BPairs.head != None and BPairs.head.value[2] == d:
    # print("here ADD 4")
    # mll.printh(BPairs)
    # mll.printh(bp)
    cur = bp.head
    while cur != None:
      if ((mll.search(BPairs, cur.value), mll.search(BPairs, (cur.value[1], cur.value[0], d))) == (None, None)):
        mll.add(BPairs, cur.value)
      cur = cur.nextNode
  if BPairs.head == None or (BPairs.head != None and BPairs.head.value[2] > d):
    # print("here ADD 3")
    # mll.printh(BPairs)
    # mll.printh(bp)
    BPairs.head = None
    cur = bp.head
    while cur != None:
      mll.add(BPairs, cur.value)
      cur = cur.nextNode
  # print("here ADD 5")
  # mll.printh(BPairs)
  # mll.printh(bp)
  return BPairs
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
