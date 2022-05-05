from algo1 import *
import random
import time

# Para lograr la navegación de los elementos es necesario la creación de la flota
#y para ello se utilizará el siguiente comando: python sistema_navegacion.py -create <local_path>
#<local_path> representa la dirección local de la carpeta que contiene el documento con la información de las embarcaciones y su fecha correspondiente.


def create(local_path):
  with open(local_path,'r') as f:
    contents = f.readlines()
  print(contents) 



"FUNCIONES AUXILIARES"


# las funciones create_flotatxt y random_month no están en pseudo-python porque no va a ser usadas en el programa ppal
# su unico propósito es genera un txt para testeo 
def create_flotatxt(n):
  direccion = ["N","S","E","W","NE","NW","SE","SW"]

  flota_m = []
  flota_m.append(random_month())

  num_flota = []
  coor_flota = []

  for i in range(1,n + 1): #en 0 está la fecha

    #se guardan los nombres y coordenadas en "uso"

    #no hay do - while en python y ni ganas de buscar alternativa inteligente
    num = random.randrange(0,n)
    while num in num_flota: #para no tener barcos con el mismo nombre
      num = random.randrange(0,n)
    num_flota.append(num)

    coor = (random.randrange(10),random.randrange(10))
    while coor in  coor_flota: #o misma coordena 
      coor = (random.randrange(10),random.randrange(10))
    coor_flota.append(coor)

    flota_m.append("(b"+str(num)+","+str(coor[0])+","+str(coor[1])+","+direccion[random.randrange(8)]+")")

  with open('flota.txt', 'w') as f: #si no exite el archivo flota lo crea
    f.write('\n'.join(flota_m))

def random_month():
  mes = random.randint(1,12)
  if mes < 10:
    mes = str(mes)
    mes = "0" + mes 
  else:
    mes = str(mes)
  return mes + "/2022"