import PySimpleGUI as sg
import re
import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def validar_numeros_y_puntos(event, value, window):
    if value == '' or value == '.' or (value.replace('.', '', 1).isdigit()):
        window[event].update(value)
    else:
        window[event].update(value[:-1])

def gui():

    column1 = [
        [sg.Text('Edad', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputEdad', size=(15, 1), enable_events=True), sg.Text('años')],
        [sg.Text('F. Respiratoria', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputFrecuenciaRespiratoria', size=(15, 1), enable_events=True), sg.Text('r/min')],
        [sg.Text('Volumen Tidal', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputVolumenTidal', size=(15, 1), enable_events=True), sg.Text('mL')],
        [sg.Text('Presión Pausa', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPresionPausa', size=(15, 1), enable_events=True), sg.Text('cmH2O')],
        [sg.Text('Driving Presion', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputDrivingPresion', size=(15, 1), enable_events=True), sg.Text('cmH2O')],
        [sg.Text('PEEP', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPeep', size=(15, 1), enable_events=True), sg.Text('cmH2O')]
    ]

    column2 = [
        [sg.Text('Compliance', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputCompliance', size=(15, 1), enable_events=True), sg.Text('cmH2O')],
        [sg.Text('S. Oxígeno', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputSaturacionOxigeno', size=(15, 1), enable_events=True), sg.Text('%')],
        [sg.Text('Pco2', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPco', size=(15, 1), enable_events=True), sg.Text('mmHg')],
        [sg.Text('PAFI', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPafi', size=(15, 1), enable_events=True), sg.Text('ml/cmH2O')],
        [sg.Text('PH', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPh', size=(15, 1), enable_events=True), sg.Text('X')],
        [sg.Text('P. Arterial', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputPresionArterial', size=(15, 1), enable_events=True), sg.Text('mmHg')]

    ]

    column3 = [
    
        [sg.Text('F. Cardiaca', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputFrecuenciaCardiaca', size=(15, 1), enable_events=True), sg.Text('f/min')],
        [sg.Text('Sodio', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputSodio', size=(15, 1), enable_events=True), sg.Text('mmol/L')],
        [sg.Text('Temperatura', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputTemperatura', size=(15, 1), enable_events=True), sg.Text('°C')],
        [sg.Text('Proteina C', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputProteinaC', size=(15, 1), enable_events=True), sg.Text('mg/dl')],
        [sg.Text('Hematocrito', size=(15, 1), font='Helvetica 12 bold', text_color='navy'), sg.InputText(key='inputHematocrito', size=(15, 1), enable_events=True), sg.Text('%')]
    ]


    frame_layout = [
        [sg.Column(column1), sg.Column(column2), sg.Column(column3)],
        [sg.Button('Inferir'), sg.Button('Limpiar'), sg.Button('Salir')]
    ]

    layout = [
        [sg.Text('Etapa 1', size=(15, 1), background_color='navy', text_color='white', justification='center', pad=((0, 0), (10, 10)))],
        [sg.Frame('', frame_layout, pad=(0, 0))]
    ]

    window = sg.Window('Formulario destete', layout)
    
    return window, column1, column2, column3

def infer(values, column1, column2, column3, scaler, interpreter,data):
    numpy_array = []
    for column in [column1, column2, column3]:
        for row in column:
            key = row[1].Key  # Obtener la clave del InputText
            numpy_array.append(float(values[key]))
            
    numpy_array.append(getPhClass(float(values["inputPh"])))
    numpy_array.append(getVtClass(data,float(values["inputVolumenTidal"])))
    numpy_array.append(getDpClass(data,float(values["inputDrivingPresion"])))
    numpy_array.append(getPeepClass(data,float(values["inputPeep"])))   
    numpy_array.append(getPpausaClass(data,float(values["inputPresionPausa"])))   

    
    numpy_array = np.array([numpy_array], dtype=float)
    
    X_test = scaler.transform(numpy_array)
    
    # Obtener detalles de entrada y salida
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Preprocesar los datos de entrada (ajusta según tu modelo)
    # Suponiendo que X_test es un numpy array con los datos de prueba

    # Realizar inferencia en una muestra de prueba
    input_data = np.array(X_test[0], dtype=np.float32)
    input_data = np.expand_dims(input_data, axis=0)  # Añadir una dimensión para el lote

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Obtener los resultados de la inferencia
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    print(numpy_array)

def getPhClass(ph):
    
    if ph >= 9: 
        return 1
    return 0 

def getVtClass(data,vt):
    seventy_fifth_vt=data["vt"].quantile(0.75)
    twenty_fifth_vt=data["vt"].quantile(0.25)
    data_vt_iqr=seventy_fifth_vt-twenty_fifth_vt
    upper_limit=seventy_fifth_vt+1.5*data_vt_iqr
    lower_limit=twenty_fifth_vt-1.5*data_vt_iqr
    
    if (vt > upper_limit) or (vt < lower_limit):
        return 1
    return 0

def getDpClass(data,dp):

    seventy_fifth_DP=data["DP"].quantile(0.75)
    twenty_fifth_DP=data["DP"].quantile(0.25)
    data_DP_iqr=seventy_fifth_DP-twenty_fifth_DP
    upper_limit=seventy_fifth_DP+1.5*data_DP_iqr
    lower_limit=twenty_fifth_DP-1.5*data_DP_iqr

    if (dp > upper_limit) or (dp < lower_limit):
        return 1
    return 0
    
    
def getPeepClass(data,peep):

    seventy_fifth_PEEP=data["PEEP"].quantile(0.75)
    twenty_fifth_PEEP=data["PEEP"].quantile(0.25)
    data_PEEP_iqr=seventy_fifth_PEEP-twenty_fifth_PEEP
    upper_limit=seventy_fifth_PEEP+1.5*data_PEEP_iqr
    lower_limit=twenty_fifth_PEEP-1.5*data_PEEP_iqr
    if (peep > upper_limit) or (peep < lower_limit):
        return 1
    return 0
    
def getPpausaClass(data,ppausa):

    seventy_fifth_Ppausa=data["Ppausa"].quantile(0.75)
    twenty_fifth_Ppausa=data["Ppausa"].quantile(0.25)
    data_Ppausa_iqr=seventy_fifth_Ppausa-twenty_fifth_Ppausa
    upper_limit=seventy_fifth_Ppausa+1.5*data_Ppausa_iqr
    lower_limit=twenty_fifth_Ppausa-1.5*data_Ppausa_iqr
    if (ppausa > upper_limit) or (ppausa < lower_limit):
        return 1
    return 0
  
def loadData():
     data = pd.read_excel("dataset_weaning.xlsx")
     data["Ph"]=data["Ph"].replace(",",".",regex=True).astype(float)
     return data 

def loadScaler():
    #data = pd.read_excel("dataset_weaning.xlsx")
    #data["Ph"]=data["Ph"].replace(",",".",regex=True).astype(float)
    
    data = loadData()
    
    data.loc[data.Ph>=9,"PhClass"]=1
    data.loc[data.Ph<9,"PhClass"]=0

    seventy_fifth_vt=data["vt"].quantile(0.75)
    twenty_fifth_vt=data["vt"].quantile(0.25)
    data_vt_iqr=seventy_fifth_vt-twenty_fifth_vt
    upper_limit=seventy_fifth_vt+1.5*data_vt_iqr
    lower_limit=twenty_fifth_vt-1.5*data_vt_iqr
    data.loc[(data.vt>upper_limit) | (data.vt<lower_limit),"vtClass"]=1
    data.loc[(data.vt<=upper_limit) & (data.vt>=lower_limit),"vtClass"]=0

    seventy_fifth_DP=data["DP"].quantile(0.75)
    twenty_fifth_DP=data["DP"].quantile(0.25)
    data_DP_iqr=seventy_fifth_DP-twenty_fifth_DP
    upper_limit=seventy_fifth_DP+1.5*data_DP_iqr
    lower_limit=twenty_fifth_DP-1.5*data_DP_iqr
    data.loc[(data.DP>upper_limit) | (data.DP<lower_limit),"DPClass"]=1
    data.loc[(data.DP<=upper_limit) & (data.DP>=lower_limit),"DPClass"]=0


    seventy_fifth_PEEP=data["PEEP"].quantile(0.75)
    twenty_fifth_PEEP=data["PEEP"].quantile(0.25)
    data_PEEP_iqr=seventy_fifth_PEEP-twenty_fifth_PEEP
    upper_limit=seventy_fifth_PEEP+1.5*data_PEEP_iqr
    lower_limit=twenty_fifth_PEEP-1.5*data_PEEP_iqr
    data.loc[(data.PEEP>upper_limit) | (data.PEEP<lower_limit),"PEEPClass"]=1
    data.loc[(data.PEEP<=upper_limit) & (data.PEEP>=lower_limit),"PEEPClass"]=0

    seventy_fifth_Ppausa=data["Ppausa"].quantile(0.75)
    twenty_fifth_Ppausa=data["Ppausa"].quantile(0.25)
    data_Ppausa_iqr=seventy_fifth_Ppausa-twenty_fifth_Ppausa
    upper_limit=seventy_fifth_Ppausa+1.5*data_Ppausa_iqr
    lower_limit=twenty_fifth_Ppausa-1.5*data_Ppausa_iqr
    data.loc[(data.Ppausa>upper_limit) | (data.Ppausa<lower_limit),"PpausaClass"]=1
    data.loc[(data.Ppausa<=upper_limit) & (data.Ppausa>=lower_limit),"PpausaClass"]=0

    data=data[data.dias<50]

    X = data.drop(columns=['dias'])
    y = data['dias']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    
    return scaler

def loadModelInterpreter():

    # Ruta al archivo del modelo .tflite
    model_path = 'weaning_model.tflite'

    # Cargar el modelo
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    return interpreter
    
def main():
    window, column1, column2, column3 = gui()
    data = loadData()
    scaler = loadScaler()
    
    interpreter = loadModelInterpreter()
    
    while True:
        event, values = window.read()
    
        if event == sg.WIN_CLOSED or event == 'Salir': 
            break
        
        if event == 'Limpiar':  
            for key in values:
                window[key]('')
        
        if event == 'Inferir':  
            infer(values, column1, column2, column3, scaler, interpreter, data)
        
        for key in values:
            if event == key:
                validar_numeros_y_puntos(event, values[key],window)
    
    window.close()

if __name__ == '__main__':
    main()
