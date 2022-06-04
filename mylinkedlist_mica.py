#Del Longo, Micaela
from algo1 import *

class Node:
  value = None 
  nextNode = None 

class LinkedList:
  head = None

  def __str__(self):
    #Permite hacer un print a una estructura LinkedList
    str_list = ""
    current = self.head
    while current != None:
      str_list =  str_list + str(current.value) + " "
      current = current.nextNode
    return(str_list)


def printv(L): #imprime una lista de forma vertical
  if L == None:
    return None
  if L.head == None:
    return None
  CurrentNode = L.head #Inicializamos CurrentNode.
  while CurrentNode != None:
    CurrentVal = CurrentNode.value
    CurrentVal = getVal(CurrentVal)
    if type(CurrentVal) == tuple:
      printTuple(CurrentVal)
    else:
      print(CurrentVal)
    CurrentNode = CurrentNode.nextNode #CurrentNode pasa a ser el siguiente nodo.

def printh(L): #imprime una lista de forma horizontal
  if L == None:
    print("None")
    return None
  if L.head == None:
    print("Lista vacía")
    return None
  CurrentNode = L.head #Inicializamos CurrentNode.
  while CurrentNode != None:
    CurrentVal = CurrentNode.value
    CurrentVal = getVal(CurrentVal)
    print(CurrentVal, end = " ")
    CurrentNode = CurrentNode.nextNode #CurrentNode pasa a ser el siguiente nodo.
  print("")

def printh_viejo(L): #imprime una lista de forma horizontal
  if L == None:
    return None
  if L.head == None:
    return None
  CurrentNode = L.head #Inicializamos CurrentNode.
  while CurrentNode != None:
    CurrentVal = CurrentNode.value
    CurrentVal = getVal(CurrentVal)
    if type(CurrentVal) == tuple:
      printTuple(CurrentVal)
    else:
      print(CurrentVal, end = " ")
    CurrentNode = CurrentNode.nextNode #CurrentNode pasa a ser el siguiente nodo.
  print("")

#add(L,element)
#Descripción: Agrega un elemento al comienzo de L, siendo L una LinkedList que representa el TAD secuencia.
#Entrada: La Lista sobre la cual se quiere agregar el elemento (LinkedList) y el valor del elemento (element) a agregar.
#Salida: No hay salida definida

def add(L,element):
  NewNode = Node()
  NewNode.value = element
  if L.head == None:
    L.head = NewNode
  else:
    NewNode.nextNode = L.head
    L.head = NewNode

#search(L,element)
#Descripción: Busca un elemento de la lista que representa el TAD secuencia .
#Entrada: La lista sobre el cual se quiere realizar la búsqueda (Linkedlist) y el valor del elemento (element) a buscar.
#Salida: Devuelve la posición donde se encuentra la primera instancia del elemento. Devuelve None si el elemento no se encuentra.

def search(L,element):
  if L.head == None:
    return None  
  CurrentNode = L.head
  i = 0
  while i<length(L):
    if getVal(CurrentNode.value) == getVal(element):
      return i 
    CurrentNode = CurrentNode.nextNode
    i = i + 1
  return None
   
def searchC(L,element):   
  if L.head == None:
    return None
  CurrentNode = L.head
  i = 0
  while i < length(L):
    if len(element) == len(String(CurrentNode.value)): #si las palabras tienen el mismo largo chequeamos
      if strcmp(String(CurrentNode.value),element):
        return  i
    CurrentNode = CurrentNode.nextNode
    i = i + 1
  return None

#insert(L,element,position)
#Descripción: Inserta un elemento en una posición determinada de la lista que representa el TAD secuencia .
#Entrada: La lista sobre el cual se quiere realizar la inserción (Linkedlist ) y el valor del elemento ( element ) a insertar y la posición ( position ) donde se quiere insertar.
#Salida: Si pudo insertar con éxito devuelve la posición donde se inserta el elemento. En caso contrario devuelve None . Devuelve None si la posición a insertar es mayor que el número de elementos en la lista.

def insert(L,element,position):
  if position>length(L) or position<0:
    return None
  elif position == 0:
    add(L,element)
  else:
    CurrentNode = L.head
    i = 0
    while CurrentNode.nextNode != None and i<(position-1):
      CurrentNode = CurrentNode.nextNode
      i = i + 1
    if CurrentNode.value != None:
      NewNode = Node()
      NewNode.value = element
      NewNode.nextNode = CurrentNode.nextNode
      CurrentNode.nextNode = NewNode
  return position 

#delete(L,element)
#Descripción: Elimina un elemento de la lista que representa el TAD secuencia .
#Poscondición: Se debe desvincular el Node a eliminar.
#Entrada: La lista sobre el cual se quiere realizar la eliminación (Linkedlist) y el valor del elemento (element) a eliminar.
#Salida : Devuelve la posición donde se encuentra el elemento a eliminar. Devuelve None si el elemento a eliminar no se encuentra.

def delete(L,element):
  if L.head == None:
    return None
  position = search(L,getVal(element))
  if position != None:
    if position == 0:
      L.head = L.head.nextNode
    else:
      CurrentNode = L.head
      for i in range(0,position-1):
        CurrentNode = CurrentNode.nextNode
      CurrentNode.nextNode = CurrentNode.nextNode.nextNode
  return position

#length(L)
#Descripción: Calcula el número de elementos de la lista que representa el TAD secuencia.
#Entrada: La lista sobre la cual se quiere calcular el número de elementos.
#Salida: Devuelve el número de elementos.

def length(L):
  if L.head == None:
    return 0
  CurrentNode = Node()
  CurrentNode = L.head
  largo = 1
  while CurrentNode.nextNode != None:
    CurrentNode = CurrentNode.nextNode
    largo = largo + 1
  return largo

#access(L,position)
#Descripción: Permite acceder a un elemento de la lista en una posición determinada.
#Entrada: La lista (LinkedList) y la position del elemento al cual se quiere acceder.
#Salida: Devuelve el valor de un elemento en una position de la lista, devuelve None si no existe elemento para dicha posición.

def access(L,position):
  if L.head == None:
    return None
  CurrentNode = Node()
  CurrentNode = L.head
  if position >= length(L) or position<0:
    return None
  else:
    for i in range(0,position):
      CurrentNode = CurrentNode.nextNode
    element = CurrentNode.value
  return element

#update(L,element,position)
#Descripción: Permite cambiar el valor de un elemento de la lista en una posición determinada
#Entrada: La lista (LinkedList) y la position sobre la cual se quiere asignar el valor de element.
#Salida: Devuelve None si no existe elemento para dicha posición. Caso contrario devuelve la posición donde pudo hacer el update.

def update(L,element,position):
  if L.head == None:
    return None
  if position >= length(L) or position<0:
    return None
  else:
    CurrentNode = Node()
    CurrentNode = L.head
    for i in range(0,position):
      CurrentNode = CurrentNode.nextNode
    CurrentNode.value = element
  return position

#------------------------------------------------------------------------------
#Swap

def swap(L,pos1,pos2): #Intercambia los nodos Node1 y Node2.
  Node1 = access(L,pos1)
  Node2 = access(L,pos2)
  update(L,Node1,pos2)
  update(L,Node2,pos1)

#------------------------------------------------------------------------------
#Inverse
#Ordena de manera inversa los elementos de una lista.
def inverse(L):
  l = length(L)-1
  i = 0 
  while i<l:
    j = 1
    while j <= (l-i):
      A = access(L,j-1)
      B = access(L,j)
      update(L,A,j)
      update(L,B,j-1)
      j = j + 1
    i = i + 1

#------------------------------------------------------------------------------
def clear(L):
  L.head = None
  return L

#------------------------------------------------------------------------------
def getVal(CurrentVal):
  while type(CurrentVal) != int and type(CurrentVal) != str and type(CurrentVal) != float and type(CurrentVal) != tuple:
    CurrentVal = CurrentVal.value
  return CurrentVal

#------------------------------------------------------------------------------
def printTuple(CurrentVal):
  print("(",end = "")
  for i in range(len(CurrentVal)):
    if i < len(CurrentVal) - 1 :
      print(getVal(CurrentVal[i]), end = ", ")
    else:
      print(getVal(CurrentVal[i]), end = ")")
  print("")