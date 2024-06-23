import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite

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
X_test = pd.read_csv("X_test.csv").values

# Realizar inferencia en una muestra de prueba
input_data = np.array(X_test[0], dtype=np.float32)
input_data = np.expand_dims(input_data, axis=0)  # Añadir una dimensión para el lote

interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# Obtener los resultados de la inferencia
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Resultado de la inferencia:", output_data)
