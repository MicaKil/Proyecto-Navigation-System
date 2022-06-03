from algo1 import *
import mylinkedlist_mica as mll

# Ejercicio 2 
# A partir de una definición de diccionario como la siguiente:
# dictionary = Array(m,0)
# Crear un módulo de nombre dictionary.py que implemente las siguientes especificaciones de las operaciones elementales para el TAD diccionario .
# Nota: dictionary puede ser redefinido para lidiar con las colisiones por encadenamiento

"----------------------------------------------------------------"
# insert(D,key, value)
# Descripción: Inserta un key en una posición determinada por la función de hash H(k) = k mod 9 en el diccionario (dictionary). Resolver colisiones por encadenamiento.
# En caso de keys duplicados se anexan a la lista.
# Entrada: el diccionario sobre el cual se quiere realizar la inserción  y el valor del key a insertar 
# Salida: Devuelve D

def insert(D,key,value):
    if type(key) == str:
        keyval = 0
        for i in range(len(key)):
            keyval += ord(key[i])
    else:
        keyval = key
    h = keyval % len(D)
    t = (key,value) #creamos la tupla a agregar
    if D[h] == None: #Si no hay nada en D[h]
        D[h] = mll.LinkedList() #Creamos la lista
        mll.add(D[h],t) #se agrega la tupla a la lista
    else:
        mll.add(D[h],t) #agregamos al ppio de la lista a la tupla

    return D
        
"----------------------------------------------------------------"

# search(D,key)
# Descripción: Busca un key en el diccionario
# Entrada: El diccionario sobre el cual se quiere realizar la búsqueda (dictionary) y el valor del key a buscar.
# Salida: Devuelve el value de la key.  Devuelve None si el key no se encuentra.

def search(D,key):
    h = key % len(D)

    if D[h] == None:
        return None
    
    current = D[h].head
    while current != None:
        if current.value[0] == key:
            return current.value[1]
        current = current.nextNode
    return None

"----------------------------------------------------------------"

# delete(D,key)
# Descripción: Elimina un key en la posición determinada por la función de hash (1) del diccionario (dictionary) 
# Postcondición: Se debe marcar como nulo  el key  a eliminar.  
# Entrada: El diccionario sobre el se quiere realizar la eliminación  y el valor del key que se va a eliminar.
# Salida: Devuelve D

def delete(D,key):
    h = key % len(D)

    if D[h] == None:
        return None
    
    #buscamos la key
    if D[h].head.value[0] == key: #si la key se encuentra en la cabecera de la lista
        D[h].head = D[h].head.nextNode
        return D
    #sino buscamos en los nodos siguientes
    current = D[h].head
    while current.nextNode != None: #para guardar el nodo anterior a eliminar
        if current.nextNode.value[0] == key:
            current.nextNode = current.nextNode.nextNode #desvinculamos al nodo
            return D
        current = current.nextNode

    return None

"----------------------------------------------------------------"

def printDic(D):
    l = len(D)
    for i in range(l):
        if D[i] == None and l<10: 
            print(i,": ",sep="")
        elif D[i] != None:
            print(i,": ",sep="", end="")
            printTuple(D[i])

"----------------------------------------------------------------"

def getNode(D,key):
    h = key % len(D)

    if D[h] == None:
        return None
    
    current = D[h].head
    while current != None:
        if current.value[0] == key:
            return current
        current = current.nextNode
    return None

"----------------------------------------------------------------"

def searchTuple(L,key):
    if L.head == None:
        return None
    
    current = L.head
    while current != None:
        if current.value[0] == key:
            return current.value[1]
        current = current.nextNode
    return None

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
        print(")", end = " ")
        CurrentNode = CurrentNode.nextNode #CurrentNode pasa a ser el siguiente nodo.

    print("")


"----------------------------------------------------------------"
# Ejercicio 4
# Implemente un algoritmo lo más eficiente posible que devuelva True o False a la siguiente proposición: dado dos strings s1...sk  y p1...pk, se quiere
#  encontrar si los caracteres de p1...pk corresponden a una permutación de s1...sk. Justificar el coste en tiempo de la solución propuesta.

# Ejemplo 1:
# Entrada: S = ‘hola’ , P = ‘ahlo’
# Salida: True, ya que P es una permutación de S

# Ejemplo 2:
# Entrada: S = ‘hola’ , P = ‘ahdo’
# Salida: Falso, ya que P tiene al caracter ‘d’ que no se encuentra en S por lo que no es una permutación de S

def isPermutation(str1,str2):
    if len(str1) != len(str2): #si las cadenas no tienen el mismo largo
        return False # no son permutaciones
    l = len(str1)

    D = Array(52,mll.LinkedList()) #creamos nuestro diccionario de tamaño igual al largo de str1
    
    for i in range(l):
        insert(D,ord(str1[i]),str1[i])
    for i in range(l):
        D = delete(D,ord(str2[i]))
        if D == None: #si falla en eliminarlo es porque no se encuentra
            return False

    return True #se encontraron todos los elementos

#complejidad O(n) ya que en el peor caso el string tiene n elementos duplicados

"----------------------------------------------------------------"
# Ejercicio 5
# Implemente un algoritmo que devuelva True si la lista que recibe de entrada tiene todos sus elementos únicos, y Falso en caso contrario. Justificar el coste 
# en tiempo de la solución propuesta.
# Ejemplo 1:
# Entrada: L = [1,5,12,1,2]
# Salida: Falso, L no tiene todos sus elementos únicos, el 1 se repite en la 1ra y 4ta posición

def checkDuplicates(list):
    LenLista = mll.length(list)

    D = Array(LenLista,mll.LinkedList())

    current = list.head
    
    while current != None:
        insert(D,current.value,current.value)
        current = current.nextNode

    return myarray.Length(D) == LenLista #si los largos no coinciden entonces hay duplicados

# si n es el largo de la lista entonces O(n+n) es decir O(2n) 
# complejidad O(n) debido al calculo de largo de las estructuras

"----------------------------------------------------------------"
# Ejercicio 6
# Los nuevos códigos postales argentinos tienen la forma cddddccc, donde c indica un carácter (A - Z) y d indica un dígito 0, . . . , 9. Por ejemplo, C1024CWN es 
# el código postal que representa a la calle XXXX a la altura 1024 en la Ciudad de Mendoza. Encontrar e implementar una función de hash apropiada para los códigos 
# postales argentinos.

# String hashing:

# hash(s) = ( s[0] + s[1]*p + ... + s[n-1]*p^(n-1) ) mod m

# It is reasonable to make p a prime number roughly equal to the number of characters in the input alphabet. 
# For example, if the input is composed of only lowercase letters of the English alphabet, p = 31 is a good choice. If the input may contain both uppercase and lowercase letters, 
# then p = 53 is a possible choice.

# m should be a large number since the probability of two random strings colliding is about 1/m
# m = 10^9 + 9 is a large number, but still small enough so that we can perform multiplication of two values using 64-bit integers.
 
def string_hash(s):
    n = len(s)
    p = 53
    m = (10**9) + 9
    h = 0
    for i in range(n):
        h  += (ord(s[i])-ord("a")+1)*(p**(n))
    h = h % m
    return h
    
"----------------------------------------------------------------"
# Ejercicio 7
# Implemente un algoritmo para realizar la compresión básica de cadenas utilizando el recuento de caracteres repetidos. Por ejemplo, la cadena ‘aabcccccaaa’ se 
# convertiría en ‘a2b1c5a3’. Si la cadena "comprimida" no se vuelve más pequeña que la cadena original, su método debería devolver la cadena original. Puedes asumir 
# que la cadena sólo tiene letras mayúsculas y minúsculas (a - z, A - Z). Justificar el coste en tiempo de la solución propuesta.

def compressString(str_input):
    D = Array(len(str_input) + 1,mll.LinkedList()) # largo + 1 para que se coloquen en orden de aparición ya que si l = 10, 10 mod 10 = 0 y se coloca primero  
    
    i = 0
    j = 1 #tenemos al menos UN caracter
    str_output = String("")

    while i < len(str_input):
        if i == len(str_input) - 1 or str_input[i] != str_input[i+1] : #si el siguiente caracter es distinto o si es el último caracter
            str2 = String(str_input[i]) #str2 va a tener el caracter actual
            insert(D,i,str2) #se inserta str2 a nuestro diccionario con key = i para que no se superponga con otra key
            str_output = concat(str_output,str2) #concatenamos str2 a la cadena de salida
            str_output = concat(str_output,String(str(j))) #concatenamos el número de veces que aparece
            j = 1 # j vuelve a ser uno para la próxima iteración
        else: # str_input[i] == str_input[i+1]  #si este se repite...
            j += 1 

        i += 1

    #printDic(D)
    if myarray.Length(D) == len(str_input): #si tienen el mismo largo los caracteres se encuentran alternados
        return str_input

    return str_output

#complejidad O(n). Sólo usé hash - tables para la comparación final ya que las cadenas input y output podrian tener el mismo largo debido a los caracteres numericos
#la comparación se podría haber realizado utilizando otra estructura como linkedlist ya que la operación de add tambien se hace en O(1)

"----------------------------------------------------------------"
# Ejercicio 8
# Se requiere encontrar la primera ocurrencia de un string p1...pk en uno más largo a1...aL. Implementar esta estrategia de la forma más eficiente posible con
#  un costo computacional menor a O(K*L) (solución por fuerza bruta).  Justificar el coste en tiempo de la solución propuesta.

# Ejemplo 1:
# Entrada: S = ‘abracadabra’ , P = ‘cada’
# Salida: 4, índice de la primera ocurrencia de P dentro de S (abracadabra)

def isSubstring(str1,str2): #consideramos a str1 > str2
    l_str1 = len(str1)
    l_str2 = len(str2)

    if l_str1 == l_str2:
        return "Los dos strings tienen el mismo largo."

    if l_str1 < l_str2 :
        return isSubstring(str2,str1)

    D = Array(l_str2 + 1,mll.LinkedList())
    for i in range(l_str2):
        insert(D,i,str2[i])

    t = 0

    for i in range(l_str1):
        if t == l_str2:
            return (i-t)
        if str1[i] == D[t].head.value[1]:
            t += 1
        else:
            t = 0

    return None

# la complejidad es O(n + m) donde n y m serian el tamñaños de los strings 1 y 2 respectivamente.
        
"----------------------------------------------------------------"
# Ejercicio 9
# Considerar los conjuntos de enteros S = {s1, . . . , sn} y T = {t1, . . . , tm}. Implemente un algoritmo que utilice una tabla de hash para determinar 
# si S ⊆ T (S subconjunto de T). ¿Cuál es la complejidad temporal del caso promedio del algoritmo propuesto?

def isSubset(S,T):
    lenS = len(S)
    lenT = len(T)

    if lenT < lenS:
        return isSubset(T,S)

    D = Array(lenT + 1,mll.LinkedList())

    for i in range(lenT):
        insert(D,T[i],T[i])

    for i in range(lenS):
        if search(D,S[i]) == None:
            return False
    
    return True

#si asumimos que S y T son sets y por ende no tienen elementos repetidos entonces
#si n = len T y m = len S, la complejidad es O(n + m) por recorrer ambos sets

#si nos queremos asegurar de que S y T sean propiamente set entonces la complejidad aumenta

"----------------------------------------------------------------"
# Ejercicio 11 (opcional)
# Implementar las operaciones de insert() y delete() dentro de una tabla hash vinculando todos los nodos libres en una lista. Se asume que un slot de la tabla
#  puede almacenar un indicador (flag), un valor, junto a una o dos referencias (punteros). Todas las operaciones de diccionario y manejo de la lista enlazada 
# deben ejecutarse en O(1). La lista debe estar doblemente enlazada o con una simplemente enlazada alcanza? 

# punteros referencia a la posición en la lista
