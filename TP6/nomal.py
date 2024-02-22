import random
import datetime
import numpy as np

# Definir la fecha de inicio (abril) y la fecha de finalización (agosto)
fecha_inicio = datetime.datetime(2023, 4, 1)
fecha_fin = datetime.datetime(2023, 8, 31)

# Crear una lista para almacenar los intervalos de arribo junto con la fecha y hora
intervalos = []

# Configurar la media y la desviación estándar para la distribución normal
media = 7  # 10 minutos en segundos
desviacion_estandar = 2  # Desviación estándar ajustable

# Generar intervalos de arribo aleatorios durante cuatro meses con distribución normal
for i in range (0,46371):
    vrandom = int(random.gauss(media, desviacion_estandar))

    intervalos.append(vrandom)

# Nombre del archivo de texto donde se guardarán los intervalos de arribo junto con la fecha y hora
nombre_archivo = "Actual.txt"

# Guardar los intervalos de arribo junto con la fecha y hora en el archivo de texto
with open(nombre_archivo, "w") as archivo:
    for intervalo in intervalos:
        archivo.write(f"{intervalo}|")

print(f"Se han generado intervalos de arribo con distribución normal durante cuatro meses, cerca de la media, en días de semana, y se han guardado en {nombre_archivo}.")
