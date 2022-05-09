from algo1 import *
import random
import pickle

"---------------------------------------------------------------------------------"
"FUNCIONES PICKLE"

#copie y pegué para poder acceder a estas luego en caso de ser necesario

  # with open('flota.txt', 'wb') as f: #lo serializamos
  #   pickle.dump(flota_m,f)

  # with open('flota.txt', 'rb') as f: #deserializacion
  #   flota_d = pickle.load(f)

"---------------------------------------------------------------------------------"

#se fija que la fecha ingresada (string) tenga el formato correcto dd/mm/yyyy
def checkDate(date):
  if date[2] == date[5] == "/":
    mes = int(date[3:5]) #no toma el valor en la posición 5
    if mes>0 and mes<13:
      dia = date[0:2]
      year = date[6:10]
      if dia == '01' and year == '2022':
        return True

  print("Error: La fecha no comple con el formato especificado.")
  return False #no cumple con el formato

#devuelve la cantidad de días en un mes
def getDays(month): 
  if month == "02":
    return 28
  month = int(month)
  if month % 2 == 0: #si es mes par
    if month < 8: #antes de agosto
      return 30
    else: #desde agosto
      return 31
  else:
    if month < 8: #antes de agosto
      return 31
    else: #desde agosto
      return 30
    


"---------------------------------------------------------------------------------"
# las funciones create_flotatxt y random_month no están en pseudo-python porque no va a ser usadas en el programa ppal
# su unico propósito es generar un txt para testeo 
def create_flotatxt(n):
  direccion = ["N","S","E","W","NE","NW","SE","SW"]

  flota_m = []
  flota_m.append(random_month())

  num_flota = []
  coor_flota = []

  for i in range(1,n + 1): #en 0 está la fecha
    #se guardan los nombres y coordenadas en "uso"
    #no hay do - while en python y ni ganas de buscar alternativa inteligente
    num = random.randrange(0,n+1)
    while num in num_flota: #para no tener barcos con el mismo nombre
      num = random.randrange(0,n+1)
    num_flota.append(num)

    coor = (random.randrange(n),random.randrange(n))
    while coor in  coor_flota: #o misma coordena 
      coor = (random.randrange(n),random.randrange(n))
    coor_flota.append(coor)

    flota_m.append("(b"+str(num)+","+str(coor[0])+","+str(coor[1])+","+direccion[random.randrange(8)]+")")

  with open('flota.txt', 'w') as f: #si no exite el archivo flota lo crea
    f.write('\n'.join(flota_m))

# genera un mes random para la lista de los barcos
def random_month():
  mes = random.randint(1,12)
  if mes < 10:
    mes = str(mes)
    mes = "0" + mes 
  else:
    mes = str(mes)
  return "01/"+ mes + "/2022"
  