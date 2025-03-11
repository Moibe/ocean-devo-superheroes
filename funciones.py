import tools
import random
import bridges
import globales
import fireWhale
import sulkuFront
import gradio as gr
import gradio_client
import splashmix.prompter as prompter
import splashmix.splash_tools as splash_tools
import splashmix.configuracion as configuracion

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#PERFORM es la app INTERNA que llamará a la app externa.
def perform(input1, gender, hero, request: gr.Request):   

    nombre_posicion = ""
    
    if globales.acceso == "login": 
        usuario = request.username
    else:        
        usuario = globales.usuario 

    tokens = fireWhale.obtenDato('usuarios', usuario, 'tokens')
    
    #1: Reglas sobre autorización si se tiene el crédito suficiente.
    #autorizacion = sulkuPypi.authorize(tokens, globales.work)
    if tokens >= globales.costo_work: 
        try: 
            gender = gender or "superhero" #default es superhero.
            resultado, nombre_posicion = mass(input1, gender, hero)
            #El resultado ya viene destuplado.
            print("Resultado de mass se ve así: ", resultado)
        except Exception as e:                              
            info_window, resultado, html_credits = sulkuFront.aError(usuario, tokens, excepcion = tools.titulizaExcepDeAPI(e))
            return resultado, info_window, html_credits, btn_buy, nombre_posicion          
    else:
        #Si no hubo autorización.
        info_window, resultado, html_credits = sulkuFront.noCredit(usuario)
        return resultado, info_window, html_credits, btn_buy, nombre_posicion
       
    #Primero revisa si es imagen!: 
    if "image.webp" in resultado:
        #Si es imagen, debitarás.
        resultado = tools.renombra_imagen(hero, resultado)
        accion = "no-debitar" if globales.acceso == "libre" else "debita"
        html_credits, info_window = sulkuFront.presentacionFinal(usuario, accion)
    else: 
        #Si no es imagen es un texto que nos dice algo.
        info_window, resultado, html_credits = sulkuFront.aError(usuario, tokens, excepcion = resultado)
        return resultado, info_window, html_credits, btn_buy, nombre_posicion           
           
    #Lo que se le regresa oficialmente al entorno.
    return resultado, info_window, html_credits, btn_buy, nombre_posicion

#MASS es la que ejecuta la aplicación EXTERNA
def mass(input1, gender, hero):
        
    api, tipo_api = tools.eligeAPI(globales.seleccion_api)  
    client = gradio_client.Client(api, hf_token=bridges.hug)

    #Adquisición Databank Particular para ese objeto y género....
    nombre_databank = gender
    datos = getattr(configuracion, nombre_databank)
    
    #Posición
    imagenSource = gradio_client.handle_file(input1)
    carpeta_positions = datos["positions_path"]  
    imagenPosition = gradio_client.handle_file(splash_tools.getPosition(carpeta_positions)) 

    nombre_posicion = imagenPosition['path']
    
    #Ésta parte es para obtener el nombre de la posición y guardarla en el log.
    #nombre_posicion = imagenPosition['path'].rsplit("\\", 1)[1] 
      
    #Objeto a Crear
    creacion_seleccionada = datos["creacion"]
    #selected_databank = datos["selected_databank"] #Se usa cuando viene de objeto no de dropdown.
    #creacion=splash_tools.creadorObjeto(creacion_seleccionada, selected_databank) #Se usa solo si se arma como objeto random.
    #1) Aquí podrías pasarle style="anime".
    #2) Aquí con los parámetros que te estuviera pasando por ejemplo via input.
    #En éste ejemplo haríamos que siempre sea ánime. #creacion.style = "Anime"
    
    #Prompt, que también usará que objeto és y su género.
    #prompt = prompter.prompteador(creacion, gender)    
    #Fraseador se usa cuando traemos el que heroe es directo del dropdownlist.
    prompt = prompter.fraseador(hero, gender)

    try:        
        result = client.predict(
                imagenSource,
                imagenPosition,
                prompt=prompt,
                #negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, 3d, drones, drone, buildings in background",
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
            #sulkuPypi.updateQuota(globales.process_cost) #Ahora se usará fireWhale, son más líneas porque la api hacia todo.
            #Pero si es menos tiempo de proceso hacerlo con Firestore.
            quota_actual = fireWhale.obtenDato("quota", "quota", "segundos")
            #print("La quota actual que hay es: ", quota_actual)
            quota_nueva = quota_actual - globales.process_cost
            print("La quota nueva es: ", quota_nueva)
            fireWhale.editaDato("quota", "quota", "segundos", quota_nueva)
        #No debitas la cuota si no era gratis, solo aplica para Zero.  
        
        result = tools.desTuplaResultado(result)
        return result, nombre_posicion

    except Exception as e:
        print("Hubo un error al ejecutar MASS:", e)
        #Errores al correr la API.
        #La no detección de un rostro es mandado aquí?! Siempre?
        mensaje = tools.titulizaExcepDeAPI(e)        
        return mensaje