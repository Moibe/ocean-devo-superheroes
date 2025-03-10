import inputs
import globales
import funciones
import sulkuFront
import autorizador
import gradio as gr

def iniciar():    
    app_path = globales.app_path
    main.queue(max_size=globales.max_size)
    #Con autorizador
    main.launch(auth=autorizador.authenticate, root_path=app_path, server_port=globales.server_port)
    #Paso directo 
    #main.launch(root_path=app_path, server_port=globales.server_port)

#Credit Related Elements
html_credits = gr.HTML(visible=globales.credits_visibility)
lbl_console = gr.Label(label="AI Terminal " + globales.version +  " messages", value="", container=True)
btn_buy = gr.Button("Get Credits", visible=False, size='lg')

#Customizable Inputs and Outputs
input1, gender, hero, result = inputs.inputs_selector(globales.seto)  

#Otros Controles y Personalizaciones
nombre_posicion = gr.Label(label="Posición", visible=globales.posicion_marker)

with gr.Blocks(theme=globales.tema, css="footer {visibility: hidden}") as main:   
    
    main.load(sulkuFront.precarga, None, html_credits) if globales.acceso != "libre" else None
       
    with gr.Row():
        demo = gr.Interface(
            fn=funciones.perform,
            inputs=[input1, gender, hero], 
            outputs=[result, lbl_console, html_credits, btn_buy, nombre_posicion], 
            flagging_mode=globales.flag
            )
iniciar()