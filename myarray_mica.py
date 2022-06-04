#Del Longo, Micaela.
from algo1 import *

#access(Array,index)

def Access(arreglo,index):
  return arreglo[index]

# print(Array)
def printArray(Array):
  for i in range(len(Array)):
    print(i,Array[i])

#search(Array,element)
#Descripción: Busca un elemento en el Array que representa el TAD secuencia,
#Entrada: el Arreglo sobre el cual se quiere realizar la búsqueda (Array) y el elemento (element) a buscar.
#Salida: Devuelve el índice donde se encuentra la primera instancia del elemento. Devuelve None si el elemento no se encuentra dentro del array.

def Search(arreglo,element):
  i=0
  flag=False
  while i<len(arreglo) and flag==False:
    if arreglo[i]==element:
      posicion=i
      flag=True 
    i=i+1
  if flag==False:
    return None

  return posicion

#insert(Array,element,position)
#Descripción:Inserta un elemento en una posición determinada de un Array que representa el TAD secuencia.
#Poscondición: Se desplazan todos los demás elementos hacia el final. El elemento en la última posición del Array se pierde.
#Entrada: el arreglo (Array) sobre el cual se va a hacer la inserción, el elemento (element) y la posición (position) donde se quiere insertar.
#Salida: Si pudo insertar con éxito devuelve la posición donde se inserta el elemento. En caso contrario devuelve None. Devuelve None si la posición a insertar es mayor que el número de elementos en el array.

def Insert(arreglo,element,position):
  if position>=len(arreglo):
    return None
  elif type(element)!=type(arreglo[0]):
    return None
  else:
    for i in range(len(arreglo)-1,position-1,-1):
      arreglo[i]=arreglo[i-1]
    arreglo[position]=element

  return arreglo


#delete(Array,element)
#Descripción: Elimina un elemento del arreglo que representa el TAD secuencia.
#Poscondición: Se desplazan los elementos restantes y se rellena con None hacia el final.
#Entrada: el arreglo sobre el cual se quiere realizar la eliminación (Array) y el elemento (element) a eliminar.
#Salida: Devuelve la posición donde se encuentra el elemento a eliminar. Devuelve None si el elemento a eliminar no se encuentra.

def Delete(arreglo,element):
  posicion=Search(arreglo,element)
  if posicion==None:
    return None
  else:
    for i in range(posicion,len(arreglo)-1):
      arreglo[i]=arreglo[i+1]
    arreglo[len(arreglo)-1]=None
  
  return arreglo


#length(Array)
#Descripción: Calcula el número de elementos activos que hay en la secuencia
#Entrada: El arreglo sobre el cual se quiere calcular el número de elementos
#Salida: El número de elementos distintos a None

def Length(arreglo):
  length=0
  for i in range(0,len(arreglo)):
    if arreglo[i]!=None:
      length=length+1
  
  return length