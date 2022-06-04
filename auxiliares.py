from msilib.schema import Error
from algo1 import *
import random
import sympy #para buscar un número primo
import dictionary_Universal as u
import mylinkedlist_mica as mll
import pickle

"Verificación de fecha"
"---------------------------------------------------------------------------------"
#se fija que la fecha ingresada (string) tenga el formato correcto dd/mm/yyyy
def checkDate(date):
  if date[2] == date[5] == "/":
    mes = int(date[3:5]) #no toma el valor en la posición 5
    if mes>0 and mes<13:
      dia = date[0:2]
      year = date[6:10]
      if dia == '01' and year == '2022':
        return True

  print("Error: La fecha no comple con el formato especificado.")
  return False #no cumple con el formato

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
  with open('lista_a_B.txt', 'wb') as f: #lo serializamos
    pickle.dump(L_ab,f)

  u.insert(D,'fecha',flota[0]) #se resevar la primer ubicación para la fecha
  for i in range(1,n):
    t = getInfo(flota[i])
    if t[3] != "N" and t[3] != "S" and t[3] != "E" and t[3] != "W" and t[3] != "NE" and t[3] != "NW" and t[3] != "SE" and t[3] != "SW":
      print("Error. No es una dirección posible.")
      return None
    u.insert(D,t[0],(t[1],t[2],t[3]))

  return D
  
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

  output = (e.head.value,e.head.nextNode.value,e.head.nextNode.nextNode.value,e.head.nextNode.nextNode.nextNode.value)
  return output

"Obetener posición"
"---------------------------------------------------------------------------------"
#value es una tupla (posicion inicial x, posicion inicial y, dirección)
def getPos(date,value): 
  x = value[0]
  y = value[1]
  direc = value[2]
  print(direc)
  if direc[0] == 'N':
    y = y + date - 1
  elif direc[0] == 'S':
    y = y - date + 1
  elif direc[0] == 'W': #si no es ni N o S entonces solo se mueve en W o E
    x = x - date + 1
  elif direc[0] == 'E':
    x = x + date - 1

  if len(direc) > 1:
    if direc[1] == 'W': #si no es ni N o S entonces solo se mueve en W o E
      x = x - date + 1
    elif direc[1] == 'E':
      x = x + date - 1
  
  return (x,y)

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

    coor = (random.randrange(n),random.randrange(n))
    while coor in  coor_flota: #o misma coordena 
      coor = (random.randrange(n),random.randrange(n))
    coor_flota.append(coor)

    flota_m.append("(b"+str(num)+","+str(coor[0])+","+str(coor[1])+","+direccion[random.randrange(8)]+")")

  with open('flota.txt', 'w') as f: #si no exite el archivo flota lo crea
    f.write('\n'.join(flota_m))

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

# with open('flota.txt', 'wb') as f: #lo serializamos
#   pickle.dump(flota_m,f)

# with open('flota.txt', 'rb') as f: #deserializacion
#   flota_d = pickle.load(f)
