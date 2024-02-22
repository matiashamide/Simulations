import random
import datetime
import numpy as np

# Definir la fecha de inicio (abril) y la fecha de finalización (agosto)
fecha_inicio = datetime.datetime(2023, 4, 1)
fecha_fin = datetime.datetime(2023, 8, 31)

# Crear una lista para almacenar los intervalos de arribo junto con la fecha y hora
intervalos_arribo_datetime = []

# Configurar la media y la desviación estándar para la distribución normal
media_segundos = 20
desviacion_estandar_segundos = 4

# Generar intervalos de arribo aleatorios durante cuatro meses con distribución normal
for i in range(0 , 13716):
    intervalo_segundos = int(random.gauss(media_segundos, desviacion_estandar_segundos))
    intervalo = datetime.timedelta(seconds=intervalo_segundos)
    # Calcular la fecha y hora de arribo sumando el intervalo
    fecha_arribo = fecha_inicio + intervalo
    
    # Verificar si la fecha de arribo corresponde a un día de semana (lunes a viernes)
    
    intervalos_arribo_datetime.append((intervalo, fecha_arribo))
    
    # Avanzar a la siguiente fecha
    fecha_inicio += intervalo

# Nombre del archivo de texto donde se guardarán los intervalos de arribo junto con la fecha y hora
nombre_archivo = "actualFecha.txt"

# Guardar los intervalos de arribo junto con la fecha y hora en el archivo de texto
with open(nombre_archivo, "w") as archivo:
    for intervalo, fecha_arribo in intervalos_arribo_datetime:
        archivo.write(f"{fecha_arribo}\n")

print(f"Se han generado intervalos de arribo con distribución normal durante cuatro meses, cerca de la media, en días de semana, y se han guardado en {nombre_archivo}.")
