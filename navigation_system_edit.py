#implementación fuerza bruta

from algo1 import *
import auxiliares as aux
import pickle
import sys

def create(local_path):
  with open(local_path,'r') as f:
    flota_list = f.readlines()
  
  fecha = flota_list[0]
  if not aux.checkDate(fecha):
    return None    

  return #lo puse para no tener problemas con el resto del código... se puede borrar obviously


"================================================================================="
"FUNCIONES SYS MODULE"

# for i in range(len(sys.argv)): #cosas que hice para ver como funcionaba el módulo
#   print (sys.argv[i])

if len(sys.argv) > 1:  
  if sys.argv[1] == "-create":
    create(sys.argv[2]) # el argv 2 debería ser el archivo o la ubicación de este
  else:
    print ("Error") 
