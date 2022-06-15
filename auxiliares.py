from algo1 import *
import random
import sympy #para buscar un número primo
import dictionary_universal as d
import mylinkedlist_mica as mll
import pickle
import math

"Verificación de fecha"
"---------------------------------------------------------------------------------"
#se fija que la fecha ingresada (string) tenga el formato correcto dd/mm/yyyy
def checkDate(date): 
  if date[2] == date[5] == "/":
    mes = int(date[3:5]) #no toma el valor en la posición 5
    if mes>0 and mes<13:
      dia = date[0:2]
      year = date[6:10]
      if (dia == '01' or dia == '01')  and year == '2022':
        return True

  print("Error: La fecha no comple con el formato especificado.")
  return False #no cumple con el formato

#"---------------------------------------------------------------------------------"
#devuelve la cantidad de días en un mes
def getDays(month): 
  if month == "02":
    return 28
  month = int(month)
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

#"---------------------------------------------------------------------------------"
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

"Funciones para calcular la distancia"
"---------------------------------------------------------------------------------"
def closestPair(date):
  #se chequea el formato de la fecha
  if len(date) > 2:
    if not checkDate(date):
      return None

  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)

  fecha = d.search(flota,'fecha')
  maxdays = getDays(fecha[3:5])
  date = int(date[0:2])
  if date < 1 and date > maxdays:
    print("No es una fecha posible.")
    return None

  m = d.search(flota,'navysize')
  # dos arreglos de tuplas
  Bx = Array(m, tuple()) # ordenado según coordenada x
  By = Array(m, tuple()) # ordenado según coordenada y
  k = 0
  for i in range(n):
    if flota[i] != None and flota[i].head.value[0] != 'fecha' and flota[i].head.value[0] != 'navysize':
      boat = flota[i].head.value[1]
      b_pos = getPos(date,boat) #calculamos la posición del barco en date
      Bx[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      By[k] = (boat[0],b_pos[0],b_pos[1],boat[3])
      k += 1

  mergesortMOD(Bx,'x')
  mergesortMOD(By,'y')

  closest = closestPairR(Bx, By, k) # devuelve la tupla (distancia mínima, lista nombre barcos, pares de barcos)
  if closest[2] > 1:
    print ("La distancia mínima el día %d es %d entre los barcos:" %(date, closest[0]))
    cur = closest[1].head
    for i in range(closest[2]):
      print(cur.value)
      cur = cur.nextNode
  else:
    print ("La distancia mínima el día %d es %d entre los barcos %s y %s." %(date,closest[0], closest[1].head.value[0], closest[1].head.value[1]))
  

#"---------------------------------------------------------------------------------"
def closestPairR(Px, Py, n):
  if n <= 3:
    return closestPairBF(Px, n)

  mid = n // 2
  print(n, mid)
  midBoat = Px[mid] #barco en la posición media del plano (respecto a los demas barcos)
  print("mid boat: ", midBoat)
  #separamos a los barcos ordenados por la coordena 'x' segun si estan al oeste o al este de mid boat
  # como ya están ordenados solo hay que dividir el array por la mitad
  BxWest = Array(mid,tuple()) # barcos de Px al Oeste de la línea
  BxEast = Array(n - mid,tuple())
  for i in range(mid):
    BxWest[i] = Px[i]
  k = 0
  for i in range(mid, n - mid): #contiene a mid boat
    BxEast[k] = Px[i]
    k += 1

  #Dividimos las coordenadas ordenadas segun 'Y' al rededor de la línea vertical
  # Asumimos que las coordenadas en x son distintas
  ByWest = Array(mid,tuple()) # barcos de Py al Oeste de la línea
  ByEast = Array(n - mid,tuple())
  iW = 0 #indices de los arreglos
  iE = 0
  for i in range(n):
    if Py[i] != midBoat:  
      if (Py[i][1] < midBoat[1] and iW < mid):
        print("West:", Py[i], midBoat[1], n, mid, n-mid, i, iW)
        ByWest[iW] = Py[i]
        iW += 1
      elif iE < (n - mid):
        print("East:", Py[i], midBoat[1], n, mid, n-mid, i, iE)
        ByEast[iE] = Py[i]
        iE += 1
    
  # consideramos la linea vertical pasando por el barco medio
  # calcular la distancia mínima al Oeste de midBoat (dW) y al Este (dE)
  dW = closestPairR(BxWest, ByWest, mid)
  dE = closestPairR(BxEast, ByEast, n - mid)
  
  d = min(dW[0], dE[0]) # Tomamos la distancia menor

  # guardamos los puntos cercanos (a una distancia <= a d) a la línea que pasa por midBoat
  strip = Array(n, tuple())
  j = 0
  for i in range(n):
    if (abs(Py[i][1] - midBoat[1]) < d):
      strip[j] = Py
      j += 1

  return stripClosest(strip, j, d)

#"---------------------------------------------------------------------------------"
# busca los puntos más cercanos en una franja (strip) de tamaño determinado 
def stripClosest(strip, n, d):
  min_dist = d
  min_boats = mll.LinkedList()
  b = 1 
  #parece O(n^2) pero...
  for i in range(n):
    j = i + 1
    # está provado que este bucle corre en cuanto mucho 7 veces... Ver Cormen ;) 
    while j < n and (strip[j][2] - strip[i][2]) < min_dist:
      dist = calculateDistantance((strip[i][1], strip[i][2]), (strip[j][1], strip[j][2])) 
      if dist == min_dist:
        mll.add(min_boats, (strip[i][0],strip[j][0]))
        b += 1
      if dist < min_dist:
        min_boats = mll.LinkedList() #se crea la lista que almacena el o los barcos
        min_dist = dist
        mll.add(min_boats, (strip[i][0],strip[j][0]))
        b = 1 # se vuelve a 1
      if dist < min_dist:
        min_dist = dist 
  
  return (min_dist, min_boats, b)

#"---------------------------------------------------------------------------------"
# calcula por fuerza bruta la distancia más corta entre n < 3 barcos 
# complejidad O(nC2) <= O(n^2) si n = 3 ent. (3C2) = 3 o sea O(1)
def closestPairBF(flota, n): 
  min_dist = 1e9
  min_boats = mll.LinkedList() #para guardar los barcos en caso de que más de un par tenga la misma dist min
  for i in range(n):
    for j in range(i + 1,n):
      dist = calculateDistantance((flota[i][1], flota[i][2]), (flota[j][1], flota[j][2])) 
      if dist == min_dist:
        mll.add(min_boats, (flota[i][0],flota[j][0]))
        b += 1
      if dist < min_dist:
        min_boats = mll.LinkedList() #se crea la lista que almacena el o los barcos
        min_dist = dist
        mll.add(min_boats, (flota[i][0],flota[j][0]))
        b = 1 # se vuelve a 1
   
  return (min_dist, min_boats, b)

#"---------------------------------------------------------------------------------"
#calcula la distancia entre dos barcos cuya posición desconocemos
def getDistance(b1,b2,date):
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
  dist = calculateDistantance(b1_pos,b2_pos) 
  return dist

#"---------------------------------------------------------------------------------"
# Dado dos puntos (tuplas de coordenadaas) calcula su distancia 
def calculateDistantance(Point1,Point2):
  return math.sqrt(((Point1[0] - Point2[0])**2)+((Point1[1] - Point2[1])**2))

#"---------------------------------------------------------------------------------"
#Merge Sort Modificado para ordenar barcos según coordenada x o y 
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




"EXTRAS"
"---------------------------------------------------------------------------------"
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

#"---------------------------------------------------------------------------------"
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
