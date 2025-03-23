import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from firebase_admin import auth

# Use the application default credentials.
cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def obtenDato(coleccion, dato, info):
    #Colección es la base donde está, dato es el índice con el que buscaremos e info es el resultado que estamos buscando. 
    #Future: Tentativamente ésta parte podría solo hacerse una vez y vivir en la app para ser reutilizado.
    ###
    #Primero debemos definir la referencia al documento, o sea a la hoja de usuario.
    doc_ref = db.collection(coleccion).document(dato)
    #Éste es el documento que tiene los datos de ella.
    documento = doc_ref.get()
    ###

    #Recuerda la conversión a diccionario.
    diccionario = documento.to_dict()

    return diccionario.get(info)

def editaDato(coleccion, dato, info, contenido):

    #Primero debemos definir la referencia al documento, o sea a la hoja de usuario.
    doc_ref = db.collection(coleccion).document(dato)
    
    doc_ref.update({
        # 'quote': quote,
        info: contenido,
    })

def verificar_token(id_token):
    """Verifica el token de ID de Firebase."""
    try:
        # Verifica el token y decodifica la información del usuario
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid  # Retorna el UID del usuario si el token es válido
    except auth.InvalidIdTokenError as e:
        print(f"Token inválido: {e}")
        return None  # Retorna None si el token es inválido


