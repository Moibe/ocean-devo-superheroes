import sets

def inputs_selector(set):
    # Obtener la configuración según el valor de 'set'
    config = sets.configuraciones.get(set)

    # Si la configuración existe, usarla
    if config:
        if len(config) == 2:
            input1 = config["input1"]
            result = config["result"]
            return input1, result
        elif len(config) == 4:
            input1 = config["input1"]
            input2 = config["gender"]
            input3 = config["hero"]
            result = config["result"]
            
            return input1, input2, input3, result
    else:
        print("Set no válido")