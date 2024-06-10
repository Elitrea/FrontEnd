import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os
from tkinter import font


def submit_form():
    def build_model(learning_rate, momentum, epochs, train_size, test_size, val_size, hidden_layers, activations, neurons):
        global model
        data = pd.read_csv(data_file_path)

        X = data[['X', 'Y', 'Z', 'Orientation_1_1', 'Orientation_1_2', 'Orientation_1_3',
                  'Orientation_2_1', 'Orientation_2_2', 'Orientation_2_3', 'Orientation_3_1',
                  'Orientation_3_2', 'Orientation_3_3']]
        y = data[['Theta1', 'Theta2', 'Theta3']]

        # Dividir los datos según los tamaños proporcionados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        if val_size > 0:
            X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=val_size/(train_size+val_size), random_state=42)

        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)
        if val_size > 0:
            X_val = np.array(X_val)
            y_val = np.array(y_val)

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Dense(neurons[0], input_shape=(12,), activation=activations[0]))
        for i in range(1, hidden_layers):
            model.add(tf.keras.layers.Dense(neurons[i], activation=activations[i]))
        model.add(tf.keras.layers.Dense(3))

        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum)
        model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

        if val_size > 0:
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_data=(X_val, y_val))
        else:
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_split=0.0)

        loss_test, accuracy_test = model.evaluate(X_test, y_test)
        results_text.insert(tk.END, "Loss en conjunto de prueba: {}\n".format(loss_test))
        results_text.insert(tk.END, "Precisión en conjunto de prueba: {}\n".format(accuracy_test))

        if val_size > 0:
            loss_val, accuracy_val = model.evaluate(X_val, y_val)
            results_text.insert(tk.END, "Loss en conjunto de validación: {}\n".format(loss_val))
            results_text.insert(tk.END, "Precisión en conjunto de validación: {}\n".format(accuracy_val))

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

    # Validar que nde los porcentajes sea igual a 1
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
    activations = [activation_entries[i].get() for i in range(hidden_layers)]

    build_model(learning_rate, momentum, epochs, train_size, test_size, val_size, hidden_layers, activations, neurons)
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
        activations = [activation_entries[i].get() for i in range(hidden_layers)]
        extra = results_text.get("1.0", "end")

        # Generar un nuevo ID de modelo
        nuevo_numero = 0
        while os.path.exists(f"modelosMLPFF/modelo_{nuevo_numero:02}.h5"):
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
            'Funciones_de_activación': [activations],
            'Archivo_de_datos': [data_file_path],
            'Resultado' : [extra]
        }
        df = pd.DataFrame(data)

        # Cargar registros existentes
        log_file_path = os.path.join('modelosMLPFF', 'log.xlsx')
        if os.path.exists(log_file_path):
            existing_df = pd.read_excel(log_file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        # Guardar el DataFrame en un archivo Excel
        df.to_excel(log_file_path, index=False)

        # Guardar el modelo
        nuevo_nombre = f"{modelo_id}.h5"
        nuevo_path = os.path.join('modelosMLPFF', nuevo_nombre)
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

    global neuron_entries, activation_entries
    neuron_entries = []
    activation_entries = []

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 6:
            widget.grid_forget()

    for i in range(num_hidden_layers):
        neuron_label = tk.Label(root, text=f"Neuronas en la capa {i+1}:")
        neuron_label.grid(row=7+i, column=0)
        neuron_entry = tk.Entry(root, font=("Helvetica", 12))
        neuron_entry.grid(row=7+i, column=1)
        neuron_entries.append(neuron_entry)

        activation_label = tk.Label(root, text=f"Activación en la capa {i+1}:")
        activation_label.grid(row=7+i, column=2)
        activation_option = tk.StringVar(root)
        activation_option.set("relu")  # Valor por defecto
        activation_menu = tk.OptionMenu(root, activation_option, "relu", "sigmoid", "tanh")
        activation_menu.grid(row=7+i, column=3)
        activation_entries.append(activation_option)

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
root.title("Formulario de MLP FeedFowarding")

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
