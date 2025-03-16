import gradio as gr

app_path = "/superheroes-dev"
server_port=7880

#MAIN
version = "13.24.27" #Fix Mantins option.
#env = "dev"
#aplicacion = "superheroes-dev" #como se llama en tu repo y tu dominio.

nombre_diccionario = "datos_superheroe"

seleccion_api = "eligeQuotaOCosto" #eligeQuotaOCosto , eligeAOB o eligeGratisOCosto
max_size = 20
#Quota o Costo
api_zero = ("Moibe/InstantID2", "quota")
api_cost = ("Moibe/InstantID2-B", "costo")

interface_api_name = "/generate_image" #El endpoint al que llamará client.

process_cost = 18

seto = "splashmix"
work = "picswap"
costo_work = 1 #Se integró costo_work para definir aquí directamente lo que cueta picswap, y dejar de usar la var work.

tema = gr.themes.Default()
flag = "never"

neural_wait = 4
mensajes_lang = "es"

acceso = "login"  #login, metrado o libre, login para medición y acceso normal, metrado para no usar login pero si medir los créditos, para eso se utilizará el parámetro global de usuario, y libre no tiene login ni metrado.
usuario = "ella"
credits_visibility = True

posicion_marker = False