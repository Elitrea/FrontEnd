import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os   

def build_model(learning_rate, momentum, train_size, test_size, val_size, hidden_layers, neurons):
    global model

    data = pd.read_csv(data_file_path)

    X = data[['X', 'Y', 'Z', 'Orientation_1_1', 'Orientation_1_2', 'Orientation_1_3',
            'Orientation_2_1', 'Orientation_2_2', 'Orientation_2_3', 'Orientation_3_1',
            'Orientation_3_2', 'Orientation_3_3']].values
    y = data[['Theta1', 'Theta2', 'Theta3']].values

    X_train, X_remaining, y_train, y_remaining = train_test_split(X, y, test_size=1-train_size, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_remaining, y_remaining, test_size=test_size, random_state=42)

    model = tf.keras.Sequential()

    for i in range(hidden_layers):
        if i == 0:
            model.add(tf.keras.layers.Dense(neurons[i], activation='relu', input_shape=(X_train.shape[1],)))
        else:
            model.add(tf.keras.layers.Dense(neurons[i], activation='relu'))

    model.add(tf.keras.layers.Dense(3))

    optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum)
    model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

    loss_test, _ = model.evaluate(X_test, y_test)
    rmse_test = np.sqrt(loss_test)

    global model_info
    model_info = {
        "Learning Rate": learning_rate,
        "Momentum": momentum,
        "Train Size": train_size,
        "Test Size": test_size,
        "Validation Size": val_size,
        "Hidden Layers": hidden_layers,
        "Neurons": neurons,
        "RMSE Test": rmse_test
    }

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

def submit_form():
    global data_file_path

    if not data_file_path:
        messagebox.showerror("Error", "Por favor, seleccione un archivo de datos.")
        return

    for entry in [learning_rate_entry, train_size_entry, test_size_entry, hidden_layers_entry]:
        if not entry.get():
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return

    try:
        float(learning_rate_entry.get())
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

    train_size = float(train_size_entry.get())
    test_size = float(test_size_entry.get())
    val_size = float(val_size_entry.get()) if val_size_entry.get() else 0.0

    total_percentage = train_size + test_size + val_size
    if total_percentage != 1.0:
        messagebox.showerror("Error", "La suma de los porcentajes de entrenamiento, prueba y validación debe ser igual a 1.")
        return

    learning_rate = float(learning_rate_entry.get())
    hidden_layers = int(hidden_layers_entry.get())
    neurons = [int(neuron_entries[i].get()) for i in range(hidden_layers)]
    momentum = float(momentum_entry.get()) 

    build_model(learning_rate, momentum, train_size, test_size, val_size, hidden_layers, neurons)
    messagebox.showinfo("Éxito", "El modelo se ha entrenado con éxito.")

def guardar_modelo():
    global model, data_file_path, model_info
    if 'model' in globals():
        learning_rate = model_info["Learning Rate"]
        train_size = model_info["Train Size"]
        test_size = model_info["Test Size"]
        val_size = model_info["Validation Size"]
        hidden_layers = model_info["Hidden Layers"]
        neurons = model_info["Neurons"]
        rmse_test = model_info["RMSE Test"]

        nuevo_numero = 0
        while os.path.exists(f"modelos/modelo_{nuevo_numero:02}.h5"):
            nuevo_numero += 1
        modelo_id = f"modelo_{nuevo_numero:02}"

        data = {
            'Modelo_ID': [modelo_id],
            'Tasa_de_aprendizaje': [learning_rate],
            'Tamaño_de_entrenamiento': [train_size],
            'Tamaño_de_prueba': [test_size],
            'Tamaño_de_validación': [val_size],
            'Capas_ocultas': [hidden_layers],
            'Neuronas_por_capa': [neurons],
            'RMSE_prueba': [rmse_test],
            'Archivo_de_datos': [data_file_path]
        }
        df = pd.DataFrame(data)

        log_file_path = os.path.join('modelos', 'log.xlsx')
        if os.path.exists(log_file_path):
            existing_df = pd.read_excel(log_file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(log_file_path, index=False)

        nuevo_nombre = f"{modelo_id}.h5"
        nuevo_path = os.path.join('modelos', nuevo_nombre)
        model.save(nuevo_path)

        messagebox.showinfo("Guardar", f"Modelo guardado como {nuevo_nombre}")

        messagebox.showinfo("Guardar", "Modelo guardado exitosamente. El formulario se ha reiniciado.")

        reset_form()
    else:
        messagebox.showerror("Error", "No hay ningún modelo para guardar.")

def reset_form():
    for entry in [learning_rate_entry, train_size_entry, test_size_entry, hidden_layers_entry, val_size_entry]:
        entry.delete(0, tk.END)
    data_file_label.config(text="")
    validation_check.set(0)
    create_dynamic_entries()

def create_dynamic_entries(event=None):
    try:
        num_hidden_layers = int(hidden_layers_entry.get())
    except ValueError:
        messagebox.showerror("Error", "El número de capas ocultas debe ser un entero.")
        return

    global neuron_entries
    neuron_entries = []

    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 5:
            widget.grid_forget()

    for i in range(num_hidden_layers):
        neuron_label = tk.Label(root, text=f"Neuronas en la capa {i+1}:")
        neuron_label.grid(row=6+i, column=0)
        neuron_entry = tk.Entry(root)
        neuron_entry.grid(row=6+i, column=1)
        neuron_entries.append(neuron_entry)

    results_text.grid(row=6+len(neuron_entries)+1, column=0, columnspan=2)
    submit_button.grid(row=6+len(neuron_entries)+1, column=2, columnspan=2)
    save_model_button.grid(row=6+len(neuron_entries)+2, column=0, columnspan=4)

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

root = tk.Tk()
root.title("Formulario de Entrenamiento de Modelo")

data_file_path = ""

data_file_button = tk.Button(root, text="Seleccionar archivo de datos", command=select_data_file)
data_file_button.grid(row=0, column=0)

data_file_label = tk.Label(root, text="")
data_file_label.grid(row=0, column=1)

tk.Label(root, text="Tasa de aprendizaje:").grid(row=1, column=0)
learning_rate_entry = tk.Entry(root)
learning_rate_entry.grid(row=1, column=1)

tk.Label(root, text="Tamaño de entrenamiento:").grid(row=2, column=0)
train_size_entry = tk.Entry(root)
train_size_entry.grid(row=2, column=1)

tk.Label(root, text="Tamaño de prueba:").grid(row=3, column=0)
test_size_entry = tk.Entry(root)
test_size_entry.grid(row=3, column=1)

validation_check = tk.IntVar()
validation_checkbox = tk.Checkbutton(root, text="¿Usar datos de validación?", variable=validation_check, command=toggle_validation)
validation_checkbox.grid(row=4, column=0)

tk.Label(root, text="Tamaño de validación (opcional):").grid(row=4, column=1)
val_size_entry = tk.Entry(root, state="disabled")
val_size_entry.grid(row=4, column=2)

tk.Label(root, text="Momentum:").grid(row=5, column=0)
momentum_entry = tk.Entry(root)
momentum_entry.grid(row=5, column=1)

tk.Label(root, text="Capas ocultas:").grid(row=6, column=0)
hidden_layers_entry = tk.Entry(root)
hidden_layers_entry.grid(row=6, column=1)


submit_button = tk.Button(root, text="Entrenar Modelo", command=submit_form)
results_text = tk.Text(root, height=10, width=50)
save_model_button = tk.Button(root, text="Guardar Modelo", command=guardar_modelo)

root.bind("<Return>", lambda event: create_dynamic_entries(event) if str(root.focus_get()) == str(hidden_layers_entry) else None)

root.mainloop()