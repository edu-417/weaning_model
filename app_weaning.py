#PySimpleGUI_License = "e2yGJrMKaBWRNpljbRn3NClhV5HQlIw6ZvSeIJ6oI3kdRJlcd5m1Vzsybo3iBzl0c1iFIcsvIokmxupkY728VruqcI26VaJ9RYCKIw6oMGTpcFxlONT1cqyLNWzlUhzeM7SuwCiLT2GUlIjXZPWa5xzCZIU3RHl1cpGPxJvte8WQ1rl7b5nJRNWGZuXpJTzxa2W69NulICjqoNx1LtC9JjObYDWh1RlpRPmplUyScO3fQlikO6ioJIZ5bXmXd9yEa0WRQhg3SWmk9chTbmihIzsIInko5WhbbbWPVFMiYgX2Nm0UIIjwoiieWkW6F05YYNSABpDyY7WmxklQcCm280itLGCMJuDFb3201QwWYhWh575sIPj9oyilIkiQwMiMQ232VtzNdeGD9atpZNXpJxJyRkCEI16eIwjzIM3kOGTegu1KIzilwviLRQG2Fe0kZ0UylnzUcu3oVPlxZYCXIT6hIAjYAV2rL2zjM9wNL3zdIiwPMEjKQJiCLQCaJwE9Y6X5R7lfRpXDhCwLaYXPJNlScEy9In68IZjqA12gLAz9MLwrLIzKIhwHMajXUriXLgCXJ6FubRWvFfpEbyEvFOkYZzHYJxlCcG3AMmi5OEibJI56bUmedhyqa8WGRaqvbs2zF3u7QNGwdvtRYwWdlGsQLZmBN6vCbBSOIJsjIVkKlaQ6QsWORGkac7mSVjzsciyWID6IIVjdEt3ROESD4y2sLAjZIE4jLLjRE1w5OXCqJV9j72aebfb032f89112a789c51dc981997f94d41f62a41af89eb9cf3eb601fa46df7e514a1063b6541df659367ee5d4695940a75aebbe608d4b4afe8ff4f75e33a26e60e8619a3acf2613eb5258bece0698185407b043133e7d4b2bd347b436b10b6861165d9a2199f45d4767839e8829fffc54ad8310792cc7ce2b2e7d3046dfb70d55ed6a9b7b43be60debc12b56124c1a26a17bf8732769b713f1992c86a14bf30690bb146676cae46d4ce7708e895afaa20cde2ce2b420368ffca0d75a7b5dcd46c99d49cca790ac7b696dae798e2b9302eea0d82fa765c0d98aae6a2213443a5a3f44da488e4665f2e8c1c818011911075697997dc995bc3c3de5f8687d4513ab44c8737b736b856d847680c34272b3ae49c202eebe4b8727721f203490d98af7ee0ce9c82aa7a5cbfb6071aebef7cbf9e16b0ad52eee8b54563a539087e92332b1c75a405f1f0b63ae7dbb78c1c08493e5507d91e48384e8d4e11c6f46744b7ebb08991737576d008ae052e3b4b1cf4f3edd370bbe4706c6723f5c33855983bdb7a82c6d379a370bc320173b7159b21f01434240fb90987c22f12a9ee43cd44d9921e89f230349b1f3188f7669a64a5c28480e138b882e6bc2b96164c654ed4c632a4e500dd5dd2c1438266515c567bd21657421c98590cbee64d19bcdf58a988d83ac71a64aea9015d36c4d22bb503421b7162209c06f6f839c96c7f0f9b"



import PySimpleGUI as sg


column1 = [
    [sg.Text('Edad', size=(15, 1)), sg.InputText(key='inputEdad', size=(25, 1))],
    [sg.Text('Hematocrito', size=(15, 1)), sg.InputText(key='inputHematocrito', size=(25, 1))],
    [sg.Text('Proteina C', size=(15, 1)), sg.InputText(key='inputProteinaC', size=(25, 1))],
    [sg.Text('Sodio', size=(15, 1)), sg.InputText(key='inputSodio', size=(25, 1))],
    [sg.Text('PH', size=(15, 1)), sg.InputText(key='inputPh', size=(25, 1))],
    [sg.Text('Pco2', size=(15, 1)), sg.InputText(key='inputPco', size=(25, 1))]
]

column2 = [
    [sg.Text('PAFI', size=(15, 1)), sg.InputText(key='inputPafi', size=(25, 1))],
    [sg.Text('Volumen Tidal', size=(15, 1)), sg.InputText(key='inputVolumenTidal', size=(25, 1))],
    [sg.Text('Compliance', size=(15, 1)), sg.InputText(key='inputCompliance', size=(25, 1))],
    [sg.Text('PEEP', size=(15, 1)), sg.InputText(key='inputPeep', size=(25, 1))],
    [sg.Text('Driving Presion', size=(15, 1)), sg.InputText(key='inputDrivingPresion', size=(25, 1))],
    [sg.Text('Presión Pausa', size=(15, 1)), sg.InputText(key='inputPresionPausa', size=(25, 1))]
]

column3 = [
    [sg.Text('F. Respiratoria', size=(15, 1)), sg.InputText(key='inputFrecuenciaRespiratoria', size=(25, 1))],
    [sg.Text('F. Cardiaca', size=(15, 1)), sg.InputText(key='inputFrecuenciaCardiaca', size=(25, 1))],
    [sg.Text('P. Arterial', size=(15, 1)), sg.InputText(key='inputPresionArterial', size=(25, 1))],
    [sg.Text('S. Oxígeno', size=(15, 1)), sg.InputText(key='inputSaturacionOxigeno', size=(25, 1))],
    [sg.Text('Temperatura', size=(15, 1)), sg.InputText(key='inputTemperatura', size=(25, 1))]
]


frame_layout = [
    [sg.Column(column1), sg.Column(column2), sg.Column(column3)],
    [sg.Button('Guardar'), sg.Button('Limpiar'), sg.Button('Salir')]
]


layout = [
    [sg.Text('Etapa 1', size=(15, 1), background_color='black', text_color='white', justification='center', pad=((0, 0), (10, 10)))],
    [sg.Frame('', frame_layout, pad=(0, 0))]
]


window = sg.Window('Formulario destete', layout)


while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == 'Salir': 
        break
    
    if event == 'Limpiar':  
        for key in values:
            window[key]('')
    
    if event == 'Guardar':  
        # 
        print(values)

window.close()

