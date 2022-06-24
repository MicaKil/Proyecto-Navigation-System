#Del Longo, Micaela.
from algo1 import *
from mylinkedlist_mica import *

class PriorityQueue:
  head = None

class PriorityNode:
  value = None
  nextNode = None
  priority = None

#enqueue_priority(Q,element,priority)
#Descripción: Agrega un elemento a Q con la prioridad priority (entero), siendo Q una estructura de tipo PriorityQueue.
#Entrada: La cola Q sobre la cual se quiere agregar el elemento (PriorityQueue), el valor del elemento (element) a agregar y un número que indica la prioridad.
#Salida: Devuelve la posición donde se insertó el elemento.

def enqueue_priority(Q,element,priority):
  NewNode = PriorityNode()
  NewNode.value = element
  NewNode.priority = priority
  position = 0
  if Q.head == None:
    Q.head = NewNode
  else:
    CurrentNode = PriorityNode()
    CurrentNode = Q.head
    while CurrentNode != None:
      if CurrentNode.priority > NewNode.priority:
        position = position + 1
      CurrentNode = CurrentNode.nextNode
    if position == 0:
      NewNode.nextNode = Q.head
      Q.head = NewNode
    else:
      CurrentNode = Q.head
      i = 0
      while CurrentNode.nextNode != None and i<(position-1):
        CurrentNode = CurrentNode.nextNode
        i = i+1
      if CurrentNode.value != None:
        NewNode.nextNode = CurrentNode.nextNode
        CurrentNode.nextNode = NewNode
  return position
       
#dequeue_priority(Q)
#Descripción: Extrae el primer elemento de la cola Q con la mayor prioridad (un valor mayor del campo priority, indica una mayor prioridad), siendo Q una estructura de tipo PriorityQueue.
#Poscondición: Se debe desvincular el Node a eliminar.
#Entrada: La cola sobre el cual se quiere realizar la eliminación (PriorityQueue).
#Salida: Devuelve el elemento con mayor prioridad. Devuelve None si la cola está vacía.

def dequeue_priority(Q):
  if Q.head == None:
    return None
  CurrentNode = PriorityNode()
  CurrentNode = Q.head
  MaxPriority = PriorityNode()
  MaxPriority = Q.head
  position = 0
  while CurrentNode != None:
    if CurrentNode.priority>MaxPriority.priority:
      MaxPriority = CurrentNode
      position = position+1
    CurrentNode = CurrentNode.nextNode
  if position == 0:
    Q.head = Q.head.nextNode
  else:
    CurrentNode = Q.head
    for i in range(0,position-1):
      CurrentNode = CurrentNode.nextNode
    CurrentNode.nextNode = CurrentNode.nextNode.nextNode
  return MaxPriority.value

def update_priority(Q,element,new_priority):
  if delete(Q,element) == None:
    print("Error: update_priority")
    return None
  enqueue_priority(Q,element,new_priority)