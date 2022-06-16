from algo1 import *
import auxiliares as aux
import dictionary_universal as d
import pickle
import sys

"---------------------------------------------------------------------------------"
#Para la creación del índice de la biblioteca
def create(local_path):
  with open(local_path,'r') as f:
    flota = f.readlines()

  fecha = flota[0]
  if not aux.checkDate(fecha):
    return None

  T = aux.create_table(flota)
  if T == None:
    return None
  with open('tabla_flota.txt', 'wb') as f: #lo serializamos
    pickle.dump(T,f)

  return print("navy created successfully")

"---------------------------------------------------------------------------------"
#Devuelve la posición (X, Y) dado una fecha (<date>) y un nombre de embarcación (<nombre_embarcacion>)
def search(date,nombre_embarcacion):
  #se chequea el formato de la fecha
  if len(date) > 2:
    if not aux.checkDate(date):
      return None
  # verificamos si el número es válido
  s = date[0]
  i = 1
  while date[i] != '/' and i < len(date) :
    s += date[i]
    i += 1
  day = int(s)
  
  if day < 1 or day > 31:
    return print("Error. No es una fecha posible.")
  
  # buscamos la fecha del informe original  
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  # verficamos que el barco nombre_embarcacion se encuentre en el listado
  val = d.search(flota,nombre_embarcacion)
  if val == None:
    return print("Error. No se encontró una embarcación con ese nombre.")
  
  if day == 1: #en el día 1 están en la posición original
    return print(val[0],val[1])
  #vericamos que sea un día posible (no supere los 28/30/31 diás según el mes)
  fecha = d.search(flota,'fecha')
  dias_max = aux.getDays(fecha[3:5]) #calcula cantidad de días en el mes
  if day > dias_max:
    return print("Error. No es una fecha posible.")

  pos = aux.getPos(day,val)
  print("X: %d Y: %d" %(pos[0],pos[1]))
  return (pos[0],pos[1])

"---------------------------------------------------------------------------------"
#Devuelve el nombre de las dos embarcaciones más cercanas entre sí (menor distancia euclidiana)
def closer(date): #HECHO PARA UN 1 BARCO DE MOMENTO
  l = len(date)
  # verificamos si el número es válido
  s = date[0]
  i = 1
  while date[i] != '/' and i < l:
    s += date[i]
    i += 1
  day = int(s)
  
  if day < 1 or day > 31:
    return print("Error. No es una fecha posible.")
  
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)
  # buscamos la fecha del informe original
  fecha = d.search(flota,'fecha')
  dias_max = aux.getDays(fecha[3:5]) #calcula cantidad de días en el mes
  if day > dias_max:
    return print("Error. No es una fecha posible.")

  closestPair = aux.closest(flota, day)
  return print ("La distancia mínima el día %s es %d entre los barcos %s y %s." %(day,closestPair[0], closestPair[1][0], closestPair[1][1]))

"---------------------------------------------------------------------------------"
#Devuelve el día del mes (date) y los barcos que están involucrados en un riesgo de colisión. En caso que no exista ningún riesgo de colisión en el mes se devuelve False
def collision():
  return

"---------------------------------------------------------------------------------"
#Devuelve un ranking (10) de las embarcaciones más cercanas entre sí.
def collision_ranking(date):
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
