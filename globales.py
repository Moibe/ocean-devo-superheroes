import gradio as gr

nombre_diccionario = "datos_superheroe"

#MAIN
version = "8.18.21"
env = "dev"
aplicacion = "superheroes-dev" #como se llama en tu repo y tu dominio.

seleccion_api = "eligeQuotaOCosto" #eligeQuotaOCosto , eligeAOB o eligeGratisOCosto
max_size = 20
#Quota o Costo
api_zero = ("Moibe/InstantID2", "quota")
api_cost = ("Moibe/InstantID2-B", "costo")

interface_api_name = "/generate_image" #El endpoint al que llamará client.


process_cost = 30

seto = "splashmix"
work = "picswap"
app_path = "/superheroes-dev"
server_port=7880
tema = gr.themes.Default()
flag = "never"

neural_wait = 6
mensajes_lang = "en"