import gradio as gr
import globales
import tools
import lists.lists as lista

mensajes, sulkuMessages = tools.get_mensajes(globales.mensajes_lang)

print("La longitud de la lista de superheroinas es: ", len(lista.super_heroines))
print("La longitud de la lista de superheroes es: ", len(lista.super_heroes))

configuraciones = {
    "splashmix": {
        "input1": gr.Image(label=mensajes.label_input1, type="filepath"),
        "gender": gr.Radio([(f"{mensajes.lbl_superheroine} 🦸🏻", "superheroine"), (f"{mensajes.lbl_superhero} 🦸🏽‍♂️", "superhero")], label=mensajes.lbl_transform), #, info="Select one")
        "hero": gr.Dropdown(lista.super_heroines + lista.super_heroes, label="Hero", info=mensajes.lbl_choose),
        "result": gr.Image(label=mensajes.label_resultado, type="filepath"),
    }
}