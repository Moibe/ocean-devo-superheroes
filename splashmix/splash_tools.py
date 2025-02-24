import os
import random
import globales
import importlib
import splashmix.configuracion
import time

def creadorObjeto(objetoACrear, databank):
    #Regresa un objeto creación con sus características.
    
    #De objetosCreación, importa el que indique splashmix.configuración:
    clase = getattr(importlib.import_module("splashmix.objetosCreacion"), objetoACrear)
    
    #Crea ese objeto para regresarlo.    
    creacion = clase(archivo_databank=databank) #Podrías agregar parametros para que así sea hecho desde su concepción: style="anime", adjective="naughty"
    #print("Ésto es la creación creada por la clase: ", creacion)
    #Pero por ahora se ponen de forma fija hasta después de creado. 
    #Future: Checar si cambiarlo a éste punto mejora rendimiento.
    return creacion

def randomNull(probabilidad, lista):
    # Generamos un número aleatorio entre 0 y 1
    numero_random = random.random()
    # Si la probabilidad es menor a 0.2 (20%), no guardamos el color
    if numero_random < probabilidad:
        result = ""  #No habrá dicho atributo. Antes ponía None, pero ahora "" para no afectar cuando genera texto para prompt.
    else:
        result = random.choice(lista) #Si eligirá un atributo de la lista.
    return result

def getPosition(carpeta_positions):
    """
    Regresa una posición del cuerpo humano para ser utilizada por el proceso de Stable Diffusion.

    Parameters:
    dataframe (dataframe): El dataframe en el que estuvimos trabajando.

    Returns:
    bool: True si se guardó el archivo correctamente.
    """

    ruta_carpeta = os.path.join("images", "positions", carpeta_positions)
        
    try: 
        lista_archivos = os.listdir(ruta_carpeta)
        #Selecciona una imagen aleatoriamente.
        posicion_aleatoria = random.choice(lista_archivos)
        ruta_posicion = os.path.join(ruta_carpeta, posicion_aleatoria)
        print("Ésto es ruta posición: ", ruta_posicion)
        return ruta_posicion     
    except Exception as e: 
        print("No hay carpeta de posiciones:", e)
        return e   

if __name__ == "__main__":
    getPosition()