from algo1 import *
import auxiliares as aux
import dictionary as d
import mylinkedlist_mica  as mll
import pickle
import sys

"---------------------------------------------------------------------------------"
#Para la creación del índice de la biblioteca
def create(local_path):
  with open(local_path,'r') as f:
    flota = f.readlines()
  #verificamos la fecha
  fecha = flota[0]
  if aux.checkDate(fecha) == False:
    return None
  # creamos el diccionario de la embarcación
  T = aux.create_table(flota)
  if T == None:
    print("Error: No se pudo crear la tabla de embarcaciones.")
    return None
  with open('tabla_flota.txt', 'wb') as f: #lo serializamos
    pickle.dump(T,f)
  return print("navy created successfully")

"---------------------------------------------------------------------------------"
#Devuelve la posición (X, Y) dado una fecha (<date>) y un nombre de embarcación (<nombre_embarcacion>)
def search(date,nombre_embarcacion):
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  # verificamos la fecha
  if aux.verifyDate(date, flota) == False:
    return None
  # verficamos que el barco nombre_embarcacion se encuentre en el diccionario
  val = d.search(flota,nombre_embarcacion)
  if val == None:
    return print("Error: No se encontró una embarcación con ese nombre.")
  day = aux.getDMY(date)[0]
  if day == 1: #en el día 1 están en la posición original
    print('X: %d Y: %d' %(val[1],val[2]))
    return (val[1],val[2])
  pos = aux.getPos(day,val)
  print("X: %d Y: %d" %(pos[0],pos[1]))
  return (pos[0],pos[1])

"---------------------------------------------------------------------------------"
#Devuelve el nombre de las dos embarcaciones más cercanas entre sí (menor distancia euclidiana)
def closer(date): 
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  # verificamos la fecha
  if aux.verifyDate(date, flota) == False:
    return None
  day = aux.getDMY(date)[0]
  closestPair = aux.closest(flota, day)
  print ("La distancia mínima el día %s es %f entre los barcos:" %(day, closestPair[0]))
  cur = closestPair[1].head
  while cur != None:
    print("%s y %s" %(cur.value[0], cur.value[1]))
    cur = cur.nextNode
  return 

"---------------------------------------------------------------------------------"
#Devuelve el día del mes (date) y los barcos que están involucrados en un riesgo de colisión. En caso que no exista ningún riesgo de colisión en el mes se devuelve False
def collision(): 
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  collisionList = aux.colisiones(flota)
  Cur=collisionList.head
  while Cur!=None:
    if len(Cur.value)==3:
      print ("El día %s, los barcos %s y %s estuvieron en riesgo de colisión." %(Cur.value[2],Cur.value[0][0],Cur.value[1][0]))
    else:
      print ("Los barcos %s y %s viajaron en paralelo en riesgo de colision durante todo el mes." %(Cur.value[0][0],Cur.value[1][0]))
    Cur=Cur.nextNode
  print("")
  return 

"---------------------------------------------------------------------------------"
#Devuelve un ranking (10) de las embarcaciones más cercanas entre sí.
def collision_ranking(date):
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  # verificamos la fecha
  if aux.verifyDate(date, flota) == False:
    return None
  day = aux.getDMY(date)[0]
  rank = aux.ranking(flota, day)
  lista_rank = mll.inverse(rank[1])
  l = mll.length(lista_rank)
  print("El día %s las %d embarcaciones más cercanas entre sí fueron:" %(day, 2*l))
  cur = lista_rank.head
  i = 1
  while cur != None:
    print("%d. %s y %s con una distancia de %f" %(i, cur.value[0], cur.value[1], cur.value[2]))
    cur = cur.nextNode
    i += 1
  return

"================================================================================="
"FUNCIONES SYS MODULE"

# for i in range(len(sys.argv)): #cosas que hice para ver como funcionaba el módulo
#   print (sys.argv[i])

if len(sys.argv) > 1:  
  if sys.argv[1] == "-create":
    create(sys.argv[2]) # el argv 2 debería ser el archivo o la ubicación de este
  elif sys.argv[1] == "-search":
    search(sys.argv[2],sys.argv[3])
  elif sys.argv[1] == "-closer":
    closer(sys.argv[2])
  elif sys.argv[1] == "-collision":
    collision()
  elif sys.argv[1] == "-collision_ranking":
    collision_ranking(sys.argv[2])
  else:
    print ("Error") 
