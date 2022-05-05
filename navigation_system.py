from algo1 import *

# Para lograr la navegación de los elementos es necesario la creación de la flota
#y para ello se utilizará el siguiente comando: python sistema_navegacion.py -create <local_path>
#<local_path> representa la dirección local de la carpeta que contiene el documento con la información de las embarcaciones y su fecha correspondiente.


def create(local_path):
  with open(local_path,'r') as f:
    contents = f.readlines()
  print contents 
