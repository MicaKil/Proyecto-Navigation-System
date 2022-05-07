from algo1 import *
import random
import pickle
import sys

# Para lograr la navegación de los elementos es necesario la creación de la flota
#y para ello se utilizará el siguiente comando: python sistema_navegacion.py -create <local_path>
#<local_path> representa la dirección local de la carpeta que contiene el documento con la información de las embarcaciones y su fecha correspondiente.


def create(local_path):
  # código para probar sys (puede ser borrado)
  with open(local_path,'r') as f:
    flota_list = f.readlines()
  print(flota_list) 

  return #lo puse para no tener problemas con el resto del código... se puede borrar obviously


"---------------------------------------------------------------------------------"
"FUNCIONES SYS ARGV"

# for i in range(len(sys.argv)): #cosas que hice para ver como funcionaba el módulo
#   print (sys.argv[i])

if len(sys.argv) > 1:  
  if sys.argv[1] == "-create":
    create(sys.argv[2]) # el argv 2 debería ser el archivo o la ubicación de este


"---------------------------------------------------------------------------------"
"FUNCIONES PICKLE"

#copie y pegué para poder acceder a estas luego en caso de ser necesario

  # with open('flota.txt', 'wb') as f: #lo serializamos
  #   pickle.dump(flota_m,f)

  # with open('flota.txt', 'rb') as f: #deserializacion
  #   flota_d = pickle.load(f)



"---------------------------------------------------------------------------------"
"---------------------------------------------------------------------------------"
"FUNCIONES AUXILIARES"

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