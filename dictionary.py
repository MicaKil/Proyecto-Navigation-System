"Implementación de hash-table con direccionamiento abierto usando double hashing"

from algo1 import *
import mylinkedlist_mica as mll
import math

"----------------------------------------------------------------"

def insert(D,key,value,m): #O(2n)
    m = len(D)

    if type(key) == str:
        keyval = string_hash(key)
    else:
        keyval = key

    t = (key,value) #creamos la tupla a agregar

    h1 = keyval % m
    h = doublehash(D, h1, keyval, m)
    if h == None:
        #print("No se pudo insertar con double hashing", key, keyval)
        h = linearprob(D, h1, m)
        #print("Insertado en: ", h)
    if h == None:
        print("No se pudo insertar:", key)
        return None
    D[h] = t
    return D

#-----------------------------------------------------------------

# doble hashea hasta encontrar una casilla vacia
def doublehash(D, h1, keyval, m):
    m1 = m - 1
    h2 = 1 + (keyval % m1)
    i = 0
    while i < m:
        h = (h1 + i*h2) % m
        if D[h] == None:
            return h
        i += 1
    return None

#-----------------------------------------------------------------

def string_hash(s):
    n = len(s)
    p = 131 # el primo despues de 128 (128 por los caracteres en el ascii)
    keyval = 0
    for i in range(n):
        #keyval  += (ord(s[i]))
        keyval  += (ord(s[i]) - ord("a") + 1) * (p**(n - i))
    return keyval
    
#-----------------------------------------------------------------

def linearprob(D, h1, m):
    i = 0
    while i < m:
        h = (h1 + i) % m
        if D[h] == None: 
            return h 
        i += 1
    return None

"----------------------------------------------------------------"

def search(D,key): #O(2n)
    m = len(D)
    if type(key) == str:
        keyval = string_hash(key)
    else:
        keyval = key
    h1 = keyval % m
    val = doublehashSearch(D, h1, keyval, key, m)    
    if val == None:
        val = linearprobSearch(D, h1, key, m)
    if val == None:
        #print("No se pudo encontrar:", key)
        return None
    return val

#-----------------------------------------------------------------
# doble hashea hasta encontrar una casilla vacia
def doublehashSearch(D, h1, keyval, key, m):
    m1 = m - 1
    h2 = 1 + (keyval % m1)
    i = 0
    while i < m:
        h = (h1 + i*h2) % m
        if D[h] != None and D[h][0] == key:
            return D[h][1] 
        i += 1
    return None

#-----------------------------------------------------------------
def linearprobSearch(D, h1, key, m):
    i = 0
    while i < m:
        h = (h1 + i) % m
        if D[h] != None and D[h][0] == key: 
            return D[h][1] 
        i += 1
    return None

"----------------------------------------------------------------"
# "No lo testee porque de momento no lo vamos a usar"
# def delete(D,key):
#     m = len(D)
#     if type(key) == str:
#         keyval = string_hash(key)
#     else:
#         keyval = key
#     h1 = keyval % m
#     m1 = m - 1
#     h2 = 1 + (keyval % m1)
#     i = 0
#     while i < m:
#         h = (h1 + i*h2) % m
#         if D[h] != None and D[h][0] == key: 
#             val = D[h][1]
#             D[h] = copy.deepcopy(None)
#             return val
#         else:
#             i += 1
#     #O(100*len(D))
#     return None

"----------------------------------------------------------------"
def printDic(D):
    l = len(D)
    for i in range(l):
        if D[i] == None and l<10: 
            print(i,": ",sep="", end="")
        elif D[i] != None:
            print(i,": ",sep="", end="")
            print(D[i])

#---------------------------------------------------------------------------------
def next_prime(n):
  while is_prime(n) == False:
    n += 1
  return n

def is_prime(n):
  for i in range(2,int(math.sqrt(n))+1):
    if (n%i) == 0:
      return False
  return True