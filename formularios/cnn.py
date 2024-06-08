import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os
from tkinter import font

def submit_form():
    def build_model(learning_rate, momentum, epochs, train_size, test_size, val_size, hidden_layers, neurons):
        global model
        data = pd.read_csv(data_file_path)

# Separar características (X) y etiquetas (y)
        X = data[['X', 'Y', 'Z', 'Orientation_1_1', 'Orientation_1_2', 'Orientation_1_3',
                'Orientation_2_1', 'Orientation_2_2', 'Orientation_2_3', 'Orientation_3_1',
                'Orientation_3_2', 'Orientation_3_3']].values
        y = data[['Theta1', 'Theta2', 'Theta3']].values

        # Dividir el conjunto de datos en conjuntos de entrenamiento, prueba y validación
        X_train, X_remaining, y_train, y_remaining = train_test_split(X, y, test_size=1-train_size, random_state=42)
        X_val, X_test, y_val, y_test = train_test_split(X_remaining, y_remaining, test_size=test_size, random_state=42)

        # Agregar una dimensión adicional para compatibilidad con Conv1D
        X_train = np.expand_dims(X_train, axis=2)
        X_test = np.expand_dims(X_test, axis=2)
        X_val = np.expand_dims(X_val, axis=2)

        # Definir la arquitectura del modelo Sequential
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(12, 1)))
        model.add(tf.keras.layers.MaxPooling1D(pool_size=2))
        model.add(tf.keras.layers.Flatten())

        # Agregar capas ocultas según el número especificado
        for i in range(hidden_layers):
            model.add(tf.keras.layers.Dense(neurons[i], activation='relu'))

        # Capa de salida con 3 neuronas para las 3 etiquetas
        model.add(tf.keras.layers.Dense(3))

        # Compilar el modelo con el optimizador SGD personalizado
        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum)
        model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

        if val_size > 0:
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_data=(X_val, y_val))
        else:
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_split=0.0)

        # Obtener y mostrar resultados
        results_test = model.evaluate(X_test, y_test)
        results_text.insert(tk.END, "Loss en conjunto de prueba: {}\n".format(results_test[0]))
        results_text.insert(tk.END, "Error absoluto medio en conjunto de prueba (MAE): {}\n".format(results_test[1]))

        if val_size > 0:
            results_val = model.evaluate(X_val, y_val)
            results_text.insert(tk.END, "Loss en conjunto de validación: {}\n".format(results_val[0]))
            results_text.insert(tk.END, "Error absoluto medio en conjunto de validación (MAE): {}\n".format(results_val[1]))

    # Validar que se haya seleccionado un archivo de datos
    if not data_file_path:
        messagebox.showerror("Error", "Por favor, seleccione un archivo de datos.")
        return

    # Validar que los campos de entrada no estén vacíos
    for entry in [learning_rate_entry, momentum_entry, epochs_entry, train_size_entry, test_size_entry, hidden_layers_entry]:
        if not entry.get():
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

    try:
        float(learning_rate_entry.get())
        float(momentum_entry.get())
        int(epochs_entry.get())
        float(train_size_entry.get())
        float(test_size_entry.get())
        int(hidden_layers_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos en los campos correspondientes.")
        return

    if val_size_entry.get():
        try:
            float(val_size_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un valor numérico válido para el tamaño de validación.")
            return

    # Validar que el número de capas ocultas sea mayor que cero
    if int(hidden_layers_entry.get()) <= 0:
        messagebox.showerror("Error", "El número de capas ocultas debe ser mayor que cero.")
        return

    # Validar que la suma de los porcentajes sea igual a 1
    train_size = float(train_size_entry.get())
    test_size = float(test_size_entry.get())
    val_size = float(val_size_entry.get()) if val_size_entry.get() else 0.0

    total_percentage = train_size + test_size + val_size
    if total_percentage != 1.0:
        messagebox.showerror("Error", "La suma de los porcentajes de entrenamiento, prueba y validación debe ser igual a 1.")
        return

    # Obtener los valores de los campos de entrada
    learning_rate = float(learning_rate_entry.get())
    momentum = float(momentum_entry.get())
    epochs = int(epochs_entry.get())

    hidden_layers = int(hidden_layers_entry.get())
    neurons = [int(neuron_entries[i].get()) for i in range(hidden_layers)]

    build_model(learning_rate, momentum, epochs, train_size, test_size, val_size, hidden_layers, neurons)
    messagebox.showinfo("Éxito", "El modelo se ha entrenado con éxito.")

def guardar_modelo():
    global model, data_file_path
    if 'model' in globals():
        # Obtener la información ingresada en el formulario
        learning_rate = float(learning_rate_entry.get())
        momentum = float(momentum_entry.get())
        epochs = int(epochs_entry.get())
        train_size = float(train_size_entry.get())
        test_size = float(test_size_entry.get())
        val_size = float(val_size_entry.get()) if val_size_entry.get() else 0.0
        hidden_layers = int(hidden_layers_entry.get())
        neurons = [int(neuron_entries[i].get()) for i in range(hidden_layers)]
        extra = results_text.get("1.0", "end")

        # Generar un nuevo ID de modelo
        nuevo_numero = 0
        while os.path.exists(f"modelosCNN/modelo_{nuevo_numero:02}.h5"):
            nuevo_numero += 1
        modelo_id = f"modelo_{nuevo_numero:02}"

        # Guardar la información en un DataFrame
        data = {
            'Modelo_ID': [modelo_id],
            'Tasa_de_aprendizaje': [learning_rate],
            'Momento': [momentum],
            'Épocas': [epochs],
            'Tamaño_de_entrenamiento': [train_size],
            'Tamaño_de_prueba': [test_size],
            'Tamaño_de_validación': [val_size],
            'Capas_ocultas': [hidden_layers],
            'Neuronas_por_capa': [neurons],
            'Archivo_de_datos': [data_file_path],
            'Resultado' : [extra]
        }
        df = pd.DataFrame(data)

        # Cargar registros existentes
        log_file_path = os.path.join('modelosCNN', 'log.xlsx')
        if os.path.exists(log_file_path):
            existing_df = pd.read_excel(log_file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        # Guardar el DataFrame en un archivo Excel
        df.to_excel(log_file_path, index=False)

        # Guardar el modelo
        nuevo_nombre = f"{modelo_id}.h5"
        nuevo_path = os.path.join('modelosCNN', nuevo_nombre)
        model.save(nuevo_path)

        messagebox.showinfo("Guardar", f"Modelo guardado como {nuevo_nombre}")

        # Mostrar un mensaje de éxito y reiniciar el formulario
        messagebox.showinfo("Guardar", "Modelo guardado exitosamente.")

        # Reiniciar el formulario
        reset_form()
    else:
        messagebox.showerror("Error", "No hay ningún modelo para guardar.")

def reset_form():
    root.destroy()

def create_dynamic_entries(event=None):
    try:
        num_hidden_layers = int(hidden_layers_entry.get())
    except ValueError:
        messagebox.showerror("Error", "El número de capas ocultas debe ser un entero.")
        return

    global neuron_entries
    neuron_entries = []

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 6:
            widget.grid_forget()

    for i in range(num_hidden_layers):
        neuron_label = tk.Label(root, text=f"Neuronas en la capa {i+1}:")
        neuron_label.grid(row=7+i, column=0)
        neuron_entry = tk.Entry(root, font=("Helvetica", 12))
        neuron_entry.grid(row=7+i, column=1)
        neuron_entries.append(neuron_entry)

    results_text.grid(row=7+len(neuron_entries)+1, column=0, columnspan=4)
    submit_button.grid(row=7+len(neuron_entries)+2, column=0, columnspan=2)
    save_model_button.grid(row=7+len(neuron_entries)+2, column=2, columnspan=2)

def toggle_validation():
    if validation_check.get() == 1:
        val_size_entry.config(state="normal")
    else:
        val_size_entry.delete(0, tk.END)
        val_size_entry.config(state="disabled")

def select_data_file():
    global data_file_path
    data_file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if data_file_path:
        data_file_label.config(text=data_file_path)

# Crear ventana principal
root = tk.Tk()
root.title("Formulario de CNN")

data_file_path = ""

# Definir la fuente predeterminada
font.nametofont("TkDefaultFont").configure(family="Helvetica", size=12)

# Botón para seleccionar el archivo de datos
data_file_button = tk.Button(root, text="Seleccionar archivo de datos", command=select_data_file, font=("Roboto", 12, "bold"), bg="#800040", fg="white")
data_file_button.grid(row=0, column=0)

data_file_label = tk.Label(root, text="")
data_file_label.grid(row=0, column=1)

# Etiquetas y campos de entrada para cada parámetro
tk.Label(root, text="Tasa de aprendizaje:").grid(row=1, column=0)
learning_rate_entry = tk.Entry(root, font=("Helvetica", 12))
learning_rate_entry.grid(row=1, column=1)

tk.Label(root, text="Momento:").grid(row=2, column=0)
momentum_entry = tk.Entry(root, font=("Helvetica", 12))
momentum_entry.grid(row=2, column=1)

tk.Label(root, text="Épocas:").grid(row=3, column=0)
epochs_entry = tk.Entry(root, font=("Helvetica", 12))
epochs_entry.grid(row=3, column=1)

tk.Label(root, text="Tamaño de entrenamiento:").grid(row=4, column=0)
train_size_entry = tk.Entry(root, font=("Helvetica", 12))
train_size_entry.grid(row=4, column=1)

tk.Label(root, text="Tamaño de prueba:").grid(row=5, column=0)
test_size_entry = tk.Entry(root, font=("Helvetica", 12))
test_size_entry.grid(row=5, column=1)

validation_check = tk.IntVar()
validation_checkbox = tk.Checkbutton(root, text="¿Usar datos de validación?", variable=validation_check, command=toggle_validation)
validation_checkbox.grid(row=6, column=0)

tk.Label(root, text="Tamaño de validación (opcional):").grid(row=6, column=1)
val_size_entry = tk.Entry(root, state="disabled", font=("Helvetica", 12))
val_size_entry.grid(row=6, column=2)

tk.Label(root, text="Capas ocultas:").grid(row=7, column=0)
hidden_layers_entry = tk.Entry(root, font=("Helvetica", 12))
hidden_layers_entry.grid(row=7, column=1)

# Botón para enviar el formulario y crear campos de entrada dinámicos
submit_button = tk.Button(root, text="Entrenar Modelo", command=submit_form, font=("Roboto", 12, "bold"), bg="#800040", fg="white")

# Widget Text para mostrar los resultados
results_text = tk.Text(root, height=10, width=50)
results_text.config(font=("Helvetica", 12))

# Botón para guardar el modelo
save_model_button = tk.Button(root, text="Guardar Modelo", command=guardar_modelo, font=("Roboto", 12, "bold"), bg="#800040", fg="white")

# Bind Enter key to create_dynamic_entries
root.bind("<Return>", lambda event: create_dynamic_entries(event) if str(root.focus_get()) == str(hidden_layers_entry) else None)

root.mainloop()

