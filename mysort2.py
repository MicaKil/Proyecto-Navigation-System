#Del Longo, Micaela.

from algo1 import *
from mylinkedlist_mica import *

# Ejercicio 1:
# Implementar los algoritmos MergeSort y QuickSort. Los mismos deben ser implementados como una función que recibe como único parámetro una estructura LinkedList.

#----------------------------------------------------------------
#QuickSort

def partition(start,end,L):
  #Permuta los elementos de la lista L y proporciona un valor end, tal que, 0<=end<length(L), T[start]<=p para todo 0<=start<end, T[end]=p, y T[start]>p para todo end<start<=length(L).
  p_index=start
  p=access(L,p_index) #p toma el valor inicial.
  while start<end:
    while (access(L,start)<=p) and start<length(L)-1:
      start=start+1
      #Se incrementa el puntero start hasta que L[start]>p (mientras L_en_start<=p).
    while access(L,end)>p:
      end=end-1
      #Se decrementa el puntero end hasta que L[end]<=p (mientras L_en_end>p).
    if start<end: #Si start y end no se han "cruzado"...
      swap(L,start,end)
  #Se intercambia el elemento del pivote (p) con el elemento de L en end para colocar al pivote en la posición correcta.
  swap(L,p_index,end)
  return end #Retorna el puntero end, que dividirá la lista en dos.

def quicksortR(start,end,L):
  if start<end:
    p=partition(start,end,L) # p es el índice del pivote
    quicksortR(start,p-1,L) #Ordena los elemento antes de p
    quicksortR(p+1,end,L) #y despues de p.
  else:
    return L
    

def quicksort(L):
  if L.head==None:
    return None
  start=0
  end=length(L)-1
  return quicksortR(start,end,L)


#----------------------------------------------------------------
#Merge Sort

def mergesort(L):
  if length(L)>1:
    m=length(L)//2 #división entera
    #Divido la lista en dos partes.
    Left=LinkedList() #Parte izquierda.
    for i in range(0,m):
      insert(Left,access(L,i),i)
    Right=LinkedList() #Parte derecha.
    k=0
    for j in range(m,length(L)):
      insert(Right,access(L,j),k)
      k=k+1

    mergesort(Left) #Ordena la parte izquierda...
    mergesort(Right) #y la derecha.

    i=0
    j=0
    k=0

    while i<length(Left) and j<length(Right):
      if access(Left,i)<access(Right,j): #Si la izquierda es menor que la derecha...
        update(L,access(Left,i),k) #Guardo en la posición k de la lista el valor izquierdo.
        i=i+1
      else:
        update(L,access(Right,j),k) #Sino guardo el derecho.
        j=j+1
      k=k+1

    #Guardo elementos restantes (si es que hay)
    while i < length(Left):
      update(L,access(Left,i),k)
      i=i+1
      k=k+1
    while j < length(Right):
      update(L,access(Right,j),k)
      j=j+1
      k=k+1


def mergesortARRAY(L):
  l = len(L)
  if l <= 1:
    return L
  
  m1 = l // 2 #división entera
  if l % 2 == 0: # si es par...
    m2 = m1 # el largo de left y Right es igual
  else: #sino
    m2 = m1 + 1 # el largo de Right es mayor e una unidad

  #Divido la lista en dos partes.
  Left = Array(m1, 0) #Parte izquierda.
  for i in range(0,m1):
    Left[i] = L[i]

  Right = Array(m2,0) #Parte derecha.
  k = 0
  for j in range(m1, l): #empiexa donde termina left
    Right[k] = L[j]
    k = k + 1

  mergesortMOD(Left) #Ordena la parte izquierda...
  mergesortMOD(Right) #y la derecha.

  i = 0
  j = 0
  k = 0

  while i < len(Left) and j < len(Right):
    if Left[i] < Right[j]: #Si la izquierda es menor que la derecha...
      L[k] = Left[i]
      i = i + 1
    else:
      L[k] = Right[j]
      j = j + 1
    k = k + 1

  #Guardo elementos restantes (si es que hay)
  while i < len(Left):
    L[k] = Left[i]
    i = i + 1
    k = k + 1
  while j < len(Right):
    L[k] = Right[j]
    j = j + 1
    k = k + 1

  return L

      


