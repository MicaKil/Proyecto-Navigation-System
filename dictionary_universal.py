"Implementación de hash-table con función de hash universal y direccionamiento abierto usando linear probing"

from algo1 import *
import mylinkedlist_mica as mll
import sympy #para obtener un número primo
import pickle
import random

#p lo suficientemente grande como para que las keys sean menores a p
# p > m 
# a pertence a [1,p-1] y b pertenece a [0,p-1] 
# h = ((ak + b) mod p) mod m

c = 100
"----------------------------------------------------------------"

def insert(D,key,value):
    m = len(D)
    p = sympy.nextprime(m)

    with open('lista_ab.txt', 'rb') as f: #deserializacion
        L = pickle.load(f)

    if mll.length(L) < c:
        a = random.randrange(1,p)
        b = random.randrange(0,p)
        mll.add(L,(a,b))
        with open('lista_ab.txt', 'wb') as f: #lo serializamos
            pickle.dump(L,f)
    else:
        index = random.randrange(0,c)
        (a,b) = mll.access(L,index)

    if type(key) == str:
        keyval = 0
        for i in range(len(key)):
            keyval += ord(key[i])
    else:
        keyval = key

    t = (key,value) #creamos la tupla a agregar

    i = 0
    h1 = (a*keyval+b) % p
    
    while i < m:
        h = (h1 + i) % m
        if D[h] == None: #Si no hay nada en D[h]
            D[h] = mll.LinkedList() #Creamos la lista
            mll.add(D[h],t) #se agrega la tupla a la lista
            return D
        else:
            i += 1    

    return None
        
"----------------------------------------------------------------"

def search(D,key):
    with open('lista_ab.txt', 'rb') as f: #deserializacion
        L = pickle.load(f)

    m = len(D)
    p = sympy.nextprime(m)

    if type(key) == str:
        keyval = 0
        for i in range(len(key)):
            keyval += ord(key[i])
    else:
        keyval = key

    result = None
    current = L.head
    while result == None and current != None:
        (a,b) = current.value
        h1 = (a*keyval+b) % p
        i = 0
        while i < m:
            h = (h1 + i) % m
            if D[h] != None and D[h].head.value[0] == key: 
                return D[h].head.value[1] 
            else:
                i += 1
        current = current.nextNode
    #O(100*len(D))
    return result

"----------------------------------------------------------------"
# "No lo testee porque de momento no lo vamos a usar"
def delete(D,key):
    with open('lista_ab.txt', 'rb') as f: #deserializacion
        L = pickle.load(f)

    p = sympy.nextprime(len(D))
    m = len(D)

    if type(key) == str:
        keyval = 0
        for i in range(len(key)):
            keyval += ord(key[i])
    else:
        keyval = key

    result = None
    current = L.head
    while result == None and current != None:
        (a,b) = current.value
        h1 = (a*keyval+b) % p
        i = 0
        while i < m:
            h = (h1 + i) % m
            if D[h] != None and D[h].head.value[0] == key: 
                val =  D[h].head.value[1]
                D[h].head = D[h].head.nextNode
                return val
            else:
                i += 1

        current = current.nextNode
    return result

"----------------------------------------------------------------"
def printDic(D):
    l = len(D)
    for i in range(l):
        if D[i] == None and l<10: 
            print(i,": ",sep="", end="")
        elif D[i] != None:
            print(i,": ",sep="", end="")
            print(D[i].head.value)
            #printTuple(D[i])

"----------------------------------------------------------------"
def printTuple(L): #imprime listas con elementos tupla
    CurrentNode = L.head #Inicializamos CurrentNode.
    while CurrentNode != None:
        print("(", end = "")
        for i in range(len(CurrentNode.value)):
            if i == len(CurrentNode.value) - 1:
                print(CurrentNode.value[i], end = "")
            else:
                print(CurrentNode.value[i], end = ", ")
        print(")", end = "")
        CurrentNode = CurrentNode.nextNode #CurrentNode pasa a ser el siguiente nodo.

    print("")
