import splashmix.static_databanks

#Indíca de q biblioteca se obtendrán los generales, por ahora: estilo.
general_databank = splashmix.static_databanks.general_data 

#Diccionarios que contienen las opciones de cada objeto disponible:
superhero = {
    "creacion": "Superhero",
    "selected_databank": splashmix.static_databanks.Superhero,
    "positions_path": "superheroes"
}

superheroine = {
    "creacion": "Superheroine",
    "selected_databank": splashmix.static_databanks.Superheroine,
    "positions_path": "superheroines"
}