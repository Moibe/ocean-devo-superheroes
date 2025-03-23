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

head = """

<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
    

"""
js = """

function haz(){

const firebaseConfig = {
    apiKey: "AIzaSyAq9PXaK2yBv5WJPCxN2ftYsIS6xmEJMTQ",
    authDomain: "glassboilerplate.firebaseapp.com",
    projectId: "glassboilerplate",
    storageBucket: "glassboilerplate.firebasestorage.app",
    messagingSenderId: "1059418877993",
    appId: "1:1059418877993:web:39af816079c772b8822c38"
  };
firebase.initializeApp(firebaseConfig);
// Provider de Google
const provider = new firebase.auth.GoogleAuthProvider();


// Listener para detectar el estado de autenticación
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // El usuario ha iniciado sesión
        //updateUI(user);

        // El usuario ha iniciado sesión
        console.log("Usuario autenticado:", user.uid);

        // Redirigir a hola.html
        //window.location.href = "hola.html";
    } else {
        // El usuario ha cerrado sesión o no ha iniciado sesión
        //updateUI(null);
        console.log("Usuario no autenticado:");
    }
})
}

"""

with gr.Blocks(theme=globales.tema, head=head, js=js, css="footer {visibility: hidden}") as main:   
    
    main.load(sulkuFront.precarga, None, html_credits) if globales.acceso != "libre" else None
       
    with gr.Row():
        demo = gr.Interface(
            fn=funciones.perform,
            inputs=[input1, gender, hero], 
            outputs=[result, lbl_console, html_credits, btn_buy, nombre_posicion], 
            flagging_mode=globales.flag
            )
iniciar()