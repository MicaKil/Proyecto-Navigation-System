from algo1 import *
import auxiliares as aux
import dictionary_Universal as u
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
  date = int(date)
  if date < 1 or date > 31:
    return print("Error. No es una fecha posible.")
  
  with open('tabla_flota.txt', 'rb') as f: #deserializacion
    flota = pickle.load(f)

  val = u.search(flota,nombre_embarcacion)
  if val == None:
    return print("Error. No se encontró una embarcación con ese nombre.")

  if date == 1: #en el día 1 están en la posición original
    return print(val[0],val[1])

  fecha = u.search(flota,'fecha')
  dias_max = aux.getDays(fecha[3:5]) #calcula cantidad de días en el mes
  if date > dias_max:
    return print("Error. No es una fecha posible.")

  pos = aux.getPos(date,val)

  return print("X: %d Y: %d" %(pos[0],pos[1]))

"---------------------------------------------------------------------------------"
def closer(date):
  return

"---------------------------------------------------------------------------------"
def collision():
  return

"---------------------------------------------------------------------------------"
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
