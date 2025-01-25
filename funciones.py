import bridges
import globales
import sulkuPypi
import sulkuFront
import gradio as gr
import gradio_client
import splashmix.prompter as prompter
import tools
import random
import time
import splashmix.splash_tools as splash_tools
import splashmix.configuracion as configuracion

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, gender, request: gr.Request):          

    nombre_posicion = ""
    tokens = sulkuPypi.getTokens(sulkuPypi.encripta(request.username).decode("utf-8"), globales.env)
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if autorizacion is True:
        try: 
            gender = gender or "superhero" #default es superhero.
            resultado, nombre_posicion = mass(input1, gender)
            #El resultado ya viene destuplado.
        except Exception as e:
            print("Excepción en mass: ", e)                     
            info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy, nombre_posicion          
    else:
        #Si no hubo autorización.
        info_window, resultado, html_credits = sulkuFront.noCredit(request.username)
        return resultado, info_window, html_credits, btn_buy, nombre_posicion
       
    #Primero revisa si es imagen!: 
    if "image.webp" in resultado:
        #Si es imagen, debitarás.
        html_credits, info_window = sulkuFront.presentacionFinal(request.username, "debita")
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(request.username, tokens, excepcion = resultado)
        return resultado, info_window, html_credits, btn_buy, nombre_posicion           
           
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy, nombre_posicion

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, gender):
    
    api, tipo_api = tools.eligeAPI(globales.seleccion_api)  
    client = gradio_client.Client(api, hf_token=bridges.hug)
    #client = gradio_client.Client("https://058d1a6dcdbaca0dcf.gradio.live/")  #MiniProxy

    #Adquisición Databank Particular para ese objeto y género....
    nombre_databank = gender
    datos = getattr(configuracion, nombre_databank)
    
    #Posición
    imagenSource = gradio_client.handle_file(input1)
    carpeta_positions = datos["positions_path"]  
    imagenPosition = gradio_client.handle_file(splash_tools.getPosition(carpeta_positions)) 

    print("Salí de el handlefile e imagePosition es: ", imagenPosition)
    nombre_posicion = imagenPosition['path']

    print("El nombre posición es: ", nombre_posicion)
    
    #Ésta parte es para obtener el nombre de la posición y guardarla en el log.
    #nombre_posicion = imagenPosition['path'].rsplit("\\", 1)[1] 

    print("Hice el split y ahora tengo un nombre posición: ", nombre_posicion)
  
    #Objeto a Crear
    creacion_seleccionada = datos["creacion"]
    selected_databank = datos["selected_databank"]
    creacion=splash_tools.creadorObjeto(creacion_seleccionada, selected_databank) 
    #1) Aquí podrías pasarle style="anime".
    #2) Aquí con los parámetros que te estuviera pasando por ejemplo via input.
    #En éste ejemplo haríamos que siempre sea ánime. #creacion.style = "Anime"
    
    #Prompt, que también usará que objeto és y su género.
    prompt = prompter.prompteador(creacion, gender) 
     

    try:        
        result = client.predict(
                imagenSource,
                imagenPosition,
                prompt=prompt,
                negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, 3d, drones, drone, buildings in background",
                style_name="(No style)", #ver lista en styles.txt
                num_steps=30,
                identitynet_strength_ratio=0.8,
                adapter_strength_ratio=0.8,
                #pose_strength=0.4,
                canny_strength=0.4,
                depth_strength=0.4,
                controlnet_selection=["depth"], #pueden ser ['pose', 'canny', 'depth'] #Al parecer pose ya no.
                guidance_scale=5,
                seed=random.randint(0, 2147483647), 
                scheduler="EulerDiscreteScheduler",
                enable_LCM=False,
                enhance_face_region=True,
                api_name=globales.interface_api_name
        )

        # result = client.predict(
		# p="Full Body",
		# api_name="/generate"
        # )
        
        #CON MINIPROXY
        # result = client.predict(
		# input1=gradio_client.handle_file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),
		# api_name="/predict"
        # )

        # #Si viene del miniproxy, hay que rehacer la tupla.
        # result = ast.literal_eval(result)  

        if tipo_api == "quota":
            print("Si era de quota, voy a debitar.")
            sulkuPypi.updateQuota(globales.process_cost)
        #No debitas la cuota si no era gratis, solo aplica para Zero.  
        
        result = tools.desTuplaResultado(result)
        return result, nombre_posicion

    except Exception as e:
        print("Hubo un error al ejecutar MASS:", e)
        #Errores al correr la API.
        #La no detección de un rostro es mandado aquí?! Siempre?
        mensaje = tools.titulizaExcepDeAPI(e)        
        return mensaje