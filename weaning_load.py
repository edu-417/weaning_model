import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = pd.read_excel("dataset_weaning.xlsx")
data["Ph"]=data["Ph"].replace(",",".",regex=True).astype(float)

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
X_test = scaler.transform(X_test)




# Ruta al archivo del modelo .tflite
model_path = 'weaning_model.tflite'

# Cargar el modelo
interpreter = tflite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

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

print("output_data : ",output_data)


