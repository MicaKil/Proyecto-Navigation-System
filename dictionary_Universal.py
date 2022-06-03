from algo1 import *
import mylinkedlist_mica as mll
import sympy
import random

#p lo suficientemente grande como para que las keys sean menores a p
# p > m 
# a pertence a [1,p-1] y b pertenece a [0,p-1] 
# h = ((ak + b) mod p) mod m

c = 100
L_ab = mll.LinkedList()

"----------------------------------------------------------------"

def insert(D,key,value):
    p = sympy.nextprime(len(D))

    if mll.length(L_ab) < c:
        a = random.randrange(1,p)
        b = random.randrange(0,p)
        mll.add(L_ab,(a,b))
    else:
        index = random.randrange(0,c)
        (a,b) = mll.access(L_ab,index)

    if type(key) == str:
        keyval = 0
        for i in range(len(key)):
            keyval += ord(key[i])
    else:
        keyval = key

    position = ((a*keyval+b) % p) % len(D)

    t = (key,value) #creamos la tupla a agregar
    if D[position] == None: #Si no hay nada en D[h]
        D[position] = mll.LinkedList() #Creamos la lista
        mll.add(D[position],t) #se agrega la tupla a la lista
    else:
        mll.add(D[position],t) #agregamos al ppio de la lista a la tupla

    return D
        
"----------------------------------------------------------------"

def search(D,key):
    p = sympy.nextprime(len(D))

    result = None
    current = L_ab.head
    while result == None and current != None:
        (a,b) = current.value
        position = ((a*key+b) % p) % len(D)
        if D[position] != None:
            result = SearchTuple(D[position],key)
        current = current.nextNode
    return result
"----------------------------------------------------------------"

def delete(D,key):
    p = sympy.nextprime(len(D))

    result = None
    current = L_ab.head
    while result == None and current != None:
        (a,b) = current.value
        position = ((a*key+b) % p) % len(D)
        if D[position] != None:
            result = deleteTuple(D[position],key)
        current = current.nextNode
    return result


"----------------------------------------------------------------"

def getListNode(L,key):
    if L.head == None:
        return None
    
    current = L.head
    while current != None:
        if current.value[0] == key:
            return current.value[1]
        current = current.nextNode
    return None


"----------------------------------------------------------------"
# busca en una lista con tuplas, devueleve el valor si lo encuentra
# y none en el caso contrario
def SearchTuple(L,key):
    if L.head == None:
        return None
    
    current = L.head
    while current != None:
        if current.value[0] == key:
            return current.value[1]
        current = current.nextNode
    return None

"----------------------------------------------------------------"
#borra en una lista con tuplas, devueleve el valor a borrar si
#  lo borra y none en el caso contrario
def deleteTuple(L,key):
    if L == None:
        return None
    
    #buscamos la key
    if L.head.value[0] == key: #si la key se encuentra en la cabecera de la lista
        val =  L.head.value[1]
        L.head = L.head.nextNode
        return val
    #sino buscamos en los nodos siguientes
    current = L.head
    while current.nextNode != None: #para guardar el nodo anterior a eliminar
        if current.nextNode.value[0] == key:
            val =  current.nextNode.value[1]
            current.nextNode = current.nextNode.nextNode #desvinculamos al nodo
            return val
        current = current.nextNode

    return None