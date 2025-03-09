import random
import splashmix.configuracion

#Ésto requiere que cada tipo de creación que hagas tenga un prompt único y se pone aquí de forma muy manual.
#El prompt en forma de variable incluirá los atributos para ese objeto, así mismo si quieres más, trabaja en la parte...
#...donde se define ése objeto. 

#IMPORTANTE: Nombre diccionario dice exactamente que databank usa el objeto en cuestión. 
#Los databanks se alojan en la carpeta data.

#Va a crear los propmts cuando reciba un objeto completo con las características del heroe.
def prompteador(objeto, nombre_diccionario):
    datos = getattr(splashmix.configuracion, nombre_diccionario)
    creacion_seleccionada = datos["creacion"]
 
    if creacion_seleccionada == "Superhero": 
        #PROMPT PARA HEROE
        prompt = f"A {objeto.style} of a superhero like {objeto.subject} " #agregar otros atributos random aquí posteriormente.
        print(prompt)
    
    elif creacion_seleccionada == "Superheroine": 
        #PROMPT PARA HEROE
        prompt = f"A {objeto.style} of a superheroine like {objeto.subject} " #agregar otros atributos random aquí posteriormente.
        print(prompt)
    
    else:        
        prompt = f"""A {objeto.style} of a {objeto.adjective} {objeto.type_girl} {objeto.subject} with {objeto.boobs} and {objeto.hair_style} wearing {objeto.wardrobe_top}, 
                {objeto.wardrobe_accesories}, {objeto.wardrobe_bottom}, {objeto.wardrobe_shoes}, {objeto.situacion} at {objeto.place} {objeto.complemento}"""   
        print(prompt)      
    return prompt

#Va a crear el prompt cuando nen lugar del objeto tenemos simplemente el nombre de un heroe (cuando se obtiene de lista.)
def fraseador(nombre_heroe, nombre_diccionario):
    datos = getattr(splashmix.configuracion, nombre_diccionario)
    creacion_seleccionada = datos["creacion"]

    #En el fraseador, el estilo viene directo de aquí: 
    estilos_posibles = ["watercolor"] #"glow and sparks watercolor luminous art"
    estilo = random.choice(estilos_posibles)
     
    if creacion_seleccionada == "Superhero": 
        #PROMPT PARA HEROE
        prompt = f"A {estilo} of a superhero like {nombre_heroe} " #agregar otros atributos random aquí posteriormente.
        print(prompt)
    
    elif creacion_seleccionada == "Superheroine": 
        #PROMPT PARA HEROE
        prompt = f"A {estilo} of a superheroine like {nombre_heroe} " #agregar otros atributos random aquí posteriormente.
        print(prompt)
      
    return prompt