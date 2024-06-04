import subprocess
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana
import os

class EntrenamientoForm(tk.Tk):   
    def __init__(self):
        super().__init__()
        self.config_entries = []
        self.activation_selectors = []
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.principal()
        global data_file_path
        data_file_path = ""


    def config_window(self):
        # Configuracion incial de la ventana
        self.title('Entrenamiento')
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Configurar el ancho y alto de la ventana para cubrir toda la pantalla
        self.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    
    def paneles(self):
        # Crear paneles
        self.barra_superior = tk.Frame(
            self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(
            self, bg=COLOR_CUERPO_PRINCIPAL, width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Entrenamiento")
        self.labelTitulo.config(fg="#fff", font=(
            "Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=20)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón de menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        # Botones del menú lateral
        self.buttonInterfazUsuario = tk.Button(self.menu_lateral, command=self.abrir_ventana_usuario)
        self.buttonInterfazEntrenamiento = tk.Button(self.menu_lateral, command=self.abrir_ventana_entrenamiento)
        self.buttonInterfazTaguchi = tk.Button(self.menu_lateral, command=self.abrir_ventana_taguchi)
        buttons_info = [
            ("Usuario", "\uf007", self.buttonInterfazUsuario),
            ("Entrenamiento", "\uf007", self.buttonInterfazEntrenamiento),
            ("Taguchi", "\uf03e", self.buttonInterfazTaguchi)
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)
            
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
            while os.path.exists(f"modelos/modelo_{nuevo_numero:02}.h5"):
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
            log_file_path = os.path.join('modelos', 'log.xlsx')
            if os.path.exists(log_file_path):
                existing_df = pd.read_excel(log_file_path)
                df = pd.concat([existing_df, df], ignore_index=True)

            # Guardar el DataFrame en un archivo Excel
            df.to_excel(log_file_path, index=False)

            # Guardar el modelo
            nuevo_nombre = f"{modelo_id}.h5"
            nuevo_path = os.path.join('modelos', nuevo_nombre)
            model.save(nuevo_path)

            messagebox.showinfo("Guardar", f"Modelo guardado como {nuevo_nombre}")

            # Mostrar un mensaje de éxito y reiniciar el formulario
            messagebox.showinfo("Guardar", "Modelo guardado exitosamente. El formulario se ha reiniciado.")

            # Reiniciar el formulario
            reset_form()
        else:
            messagebox.showerror("Error", "No hay ningún modelo para guardar.")

    def reset_form():
        # Limpiar los campos de entrada
        for entry in [learning_rate_entry, momentum_entry, epochs_entry, train_size_entry, test_size_entry, hidden_layers_entry, val_size_entry]:
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

        global neuron_entries, activation_entries
        neuron_entries = []
        activation_entries = []

        for widget in root.grid_slaves():
            if int(widget.grid_info()["row"]) > 6:
                widget.grid_forget()

        for i in range(num_hidden_layers):
            neuron_label = tk.Label(root, text=f"Neuronas en la capa {i+1}:")
            neuron_label.grid(row=7+i, column=0)
            neuron_entry = tk.Entry(root)
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

    def principal(self):
        # Crear un frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Estilo personalizado para los botones
        style = ttk.Style()
        style.configure("Custom.TButton", padding=20, font=("Helvetica", 16), background=COLOR_MENU_LATERAL, foreground=COLOR_MENU_LATERAL)

        # Crear tres botones en el frame principal con el estilo personalizado
        btn1 = ttk.Button(main_frame, text="MLP Básica", style="Custom.TButton", command=self.accion_btn1)
        btn1.pack(side='left', padx=50)

        btn2 = ttk.Button(main_frame, text="MLP FeedFowarding", style="Custom.TButton", command=self.accion_btn2)
        btn2.pack(side='left', padx=50)

        btn3 = ttk.Button(main_frame, text="CNN", style="Custom.TButton", command=self.accion_btn3)
        btn3.pack(side='left', padx=50)

    def accion_btn1(self):
        try:
            # Ejecutar el archivo mlp.py
            subprocess.Popen(["python", "formularios\mlpBasic.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo mlp.py no se encontró.")
    def accion_btn2(self):
        try:
            # Ejecutar el archivo mlp.py
            subprocess.Popen(["python", "formularios\mlpFeedfowarding.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo mlp.py no se encontró.")

    def accion_btn3(self):
        try:
            # Ejecutar el archivo mlp.py
            subprocess.Popen(["python", "formularios\cnn.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo mlp.py no se encontró.")


    def activar_caja_porcentaje(self, event):
        opcion_seleccionada = self.porcentaje_selector.get()
        if opcion_seleccionada == "Sí":
            self.porcentaje_entry.config(state="normal")
        else:
            self.porcentaje_entry.delete(0, tk.END)
            self.porcentaje_entry.config(state="disabled")

    def enviar_formulario(self):
        # Lógica para procesar la información del formulario
        modelo = "Modelo: " + self.modelo_selector.get()
        id_prueba = "ID Prueba: " + self.id_prueba_selector.get()  # Agregado
        num_capas_ocultas = "Número de Capas Ocultas: " + self.capas_ocultas_entry.get()  # Agregado
        num_neuronas_capa_x = []  # Lista para almacenar el número de neuronas en cada capa oculta
        funciones_activacion_capa_x = []  # Lista para almacenar la función de activación en cada capa oculta

        for i in range(1, int(self.capas_ocultas_entry.get()) + 1):
            num_neuronas = getattr(self, f'config_entry_{i}').get()  # Ajustar aquí
            funcion_activacion = getattr(self, f'activacion_capa_{i}_selector').get()  # Ajustar aquí
            num_neuronas_capa_x.append(f'Neuronas Capa {i}: {num_neuronas}')
            funciones_activacion_capa_x.append(f'Activación Capa {i}: {funcion_activacion}')

        taza_aprendizaje = "Taza de Aprendizaje: " + self.taza_aprendizaje_entry.get()  # Agregado
        momento = "Momento: " + self.momento_entry.get()  # Agregado
        epocas = "Épocas: " + self.epocas_entry.get()  # Agregado
        porcentaje = "Porcentaje: " + self.porcentaje_entry.get() if self.porcentaje_selector.get() == "Sí" else "Porcentaje: No aplica"

        # Imprime la información (puedes ajustar esto según tus necesidades)
        print(modelo, id_prueba, num_capas_ocultas)
        print(num_neuronas_capa_x)
        print(funciones_activacion_capa_x)
        print(taza_aprendizaje, momento, epocas, porcentaje)

    def configuracion_capas(self):
        # Generar dinámicamente los campos según el número de capas ocultas
        num_capas = int(self.capas_ocultas_entry.get())

        # Limpiar configuraciones anteriores si existen
        for widget in self.cuerpo_principal.winfo_children():
            if "config_entry" in widget.winfo_name() or "activacion_capa" in widget.winfo_name():
                widget.destroy()

        for i in range(num_capas):
            # Número de neuronas capa X
            label_text = f"Neuronas Capa {i + 1}:"
            label = tk.Label(self.cuerpo_principal, text=label_text)
            label.grid(row=10 + i, column=0, padx=10, pady=10, sticky="w")
            label.config(font=("Roboto", 12))

            entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12), name=f'config_entry_{i + 1}')
            entry.grid(row=10 + i, column=1, padx=10, pady=10, sticky="w")

            # Función de activación
            label_activation_text = f"Activación Capa {i + 1}:"
            label_activation = tk.Label(self.cuerpo_principal, text=label_activation_text)
            label_activation.grid(row=10 + i, column=2, padx=10, pady=10, sticky="w")
            label_activation.config(font=("Roboto", 12))

            activation_options = ["sigmoid 1", "tanh"]  # Reemplazar con opciones reales
            activation_selector = ttk.Combobox(self.cuerpo_principal, values=activation_options, font=("Roboto", 12), name=f'activacion_capa_{i + 1}_selector')
            activation_selector.grid(row=10 + i, column=3, padx=10, pady=10, sticky="w")

            # Agregar entry y selector a las listas
            self.config_entries.append(entry)
            self.activation_selectors.append(activation_selector)

    # Procesar la información del formulario
    def procesar_informacion(self):
        # Lógica para procesar la información del formulario
        modelo = "Modelo: " + self.modelo_selector.get()
        id_prueba = "ID Prueba: " + self.id_prueba_selector.get()
        num_capas_ocultas_str = self.capas_ocultas_entry.get()
        # Extraer solo el número de la cadena
        num_capas_ocultas = int(num_capas_ocultas_str.split()[0])

        
        num_neuronas_capa_x = []
        funciones_activacion_capa_x = []

        for i in range(len(self.config_entries)):
            num_neuronas = self.config_entries[i].get()
            funcion_activacion = self.activation_selectors[i].get()
            num_neuronas_capa_x.append(f'Neuronas Capa {i + 1}: {num_neuronas}')
            funciones_activacion_capa_x.append(f'Activación Capa {i + 1}: {funcion_activacion}')

        # Extraer solo el valor numérico de la tasa de aprendizaje
        taza_aprendizaje_str = self.taza_aprendizaje_entry.get()
        taza_aprendizaje = float(taza_aprendizaje_str.split(':')[1].strip())

        momento = "Momento: " + self.momento_entry.get()
        epocas = "Épocas: " + self.epocas_entry.get()
        porcentaje = "Porcentaje: " + self.porcentaje_entry.get() if self.porcentaje_selector.get() == "Sí" else "Porcentaje: No aplica"

        # Construir un diccionario con la estructura deseada
        informacion_procesada = {
            "modelo": modelo,
            "id_prueba": id_prueba,
            "num_capas_ocultas": num_capas_ocultas,
            "configuracion_capas": {
                f'Neuronas Capa {i + 1}': self.config_entries[i].get() for i in range(len(self.config_entries))
            },
            "activaciones_capas": {
                f'Activación Capa {i + 1}': self.activation_selectors[i].get() for i in range(len(self.activation_selectors))
            },
            "taza_aprendizaje": taza_aprendizaje,
            "momento": momento,
            "epocas": epocas,
            "porcentaje": porcentaje
        }

        return informacion_procesada

    def enviar_formulario(self):
        # Procesar la información del formulario
        info_procesada = self.procesar_informacion()

        # Llamar a otro método y pasarle la información procesada
        self.otro_metodo(info_procesada)
    
    def otro_metodo(self, info_procesada):
        # Obtener el archivo seleccionado
        file_path = self.selected_file_path
        
        # Check si se ha seleccionado un archivo
        if not file_path:
            print("No se ha seleccionado ningún archivo.")
            return

        # Leer los datos del archivo CSV
        data = pd.read_csv(file_path)

        # Dividir datos en entrada (X) y salida (y)
        X = data[['X', 'Y', 'Z', 'Orientation_1_1', 'Orientation_1_2', 'Orientation_1_3',
                  'Orientation_2_1', 'Orientation_2_2', 'Orientation_2_3', 'Orientation_3_1',
                  'Orientation_3_2', 'Orientation_3_3']]
        y = data[['Theta1', 'Theta2', 'Theta3']]

        # Dividir datos en conjunto de entrenamiento y conjunto de prueba
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Convertir datos a matrices numpy
        X_train = np.array(X_train)
        X_val = np.array(X_val)
        y_train = np.array(y_train)
        y_val = np.array(y_val)

        # Función para construir el modelo con los parámetros dados
        
        def build_model(X_train, y_train, X_val, y_val, learning_rate, momentum, epochs, hidden_layers, activations):
            # Definir el modelo
            model = tf.keras.Sequential()
            # Agregar la primera capa densa al modelo con la activación de la primera capa oculta
            model.add(tf.keras.layers.Dense(64, input_shape=(12,), activation=list(activations.values())[0]))

            # Agregar capas ocultas adicionales con sus respectivas activaciones
            for i in range(1, hidden_layers):
                model.add(tf.keras.layers.Dense(64, activation=list(activations.values())[i]))

            # Agregar la capa de salida con 3 neuronas para Theta1, Theta2 y Theta3
            model.add(tf.keras.layers.Dense(3))

            # Compilar el modelo
            optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum)
            model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])  # Agregar métrica de precisión

            # Entrenar el modelo
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_data=(X_val, y_val))

            # Evaluar el modelo en el conjunto de validación
            loss_val, accuracy_val = model.evaluate(X_val, y_val)
            print("Loss en conjunto de validación:", loss_val)
            print("Precisión en conjunto de validación:", accuracy_val)

            # Guardar el modelo entrenado
            model.save('modelo_entrenado.h5')

        # Llamar a la función para construir y entrenar el modelo con los parámetros proporcionados
        build_model(X_train, y_train, X_val, y_val, info_procesada['taza_aprendizaje'], info_procesada['momento'], info_procesada['epocas'], info_procesada['num_capas_ocultas'], info_procesada['activaciones_capas'])
    
    def seleccionar_archivo(self):
        file_path = filedialog.askopenfilename()

        # Check if a file was selected
        if file_path:
            df = pd.read_csv(file_path)
            print(f"Archivo seleccionado: {file_path}")
            print(df)

            # Create a label to display the selected file
            self.archivo_seleccionado_label = tk.Label(self.cuerpo_principal, text=f"Archivo Seleccionado: {file_path}")
            self.archivo_seleccionado_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")
            self.archivo_seleccionado_label.config(font=("Roboto", 12))

            # Save the file_path so that it can be accessed later if needed
            self.selected_file_path = file_path

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"   {icon}  {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el raton por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar el estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')
    
    def toggle_panel(self):
        # Alternar visibilidad de menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def abrir_ventana_entrenamiento(self):
        from formularios.form_entrenamiento import EntrenamientoForm
        # Verificar si ya hay una instancia de EntrenamientoForm
        if not hasattr(self, 'entrenamiento_form'):
            # Crear una nueva instancia solo si no existe
            self.entrenamiento_form = EntrenamientoForm()

        # Ocultar y destruir la instancia actual de UsuarioForm
        self.withdraw()
        self.destroy()
        
        # Configurar la nueva instancia en el cuerpo principal
        self.cuerpo_principal.configure(width=150)
        self.entrenamiento_form.pack_forget()
        self.cuerpo_principal = self.entrenamiento_form
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def abrir_ventana_taguchi(self):
        from formularios.form_taguchi import TaguchiForm
        # Verificar si ya hay una instancia de EntrenamientoForm
        if not hasattr(self, 'taguchi_form'):
            # Crear una nueva instancia solo si no existe
            self.taguchi_form = TaguchiForm()
        
        # Ocultar y destruir la instancia actual de UsuarioForm
        self.withdraw()
        self.destroy()

        # Configurar la nueva instancia en el cuerpo principal
        self.cuerpo_principal.configure(width=150)
        self.entrenamiento_form.pack_forget()
        self.cuerpo_principal = self.entrenamiento_form
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def abrir_ventana_usuario(self):
        from formularios.form_usuario import UsuarioForm
        # Verificar si ya hay una instancia de EntrenamientoForm
        if not hasattr(self, 'usuario_form'):
            # Crear una nueva instancia solo si no existe
            self.usuario_form = UsuarioForm()
        # Ocultar y destruir la instancia actual de UsuarioForm
        self.withdraw()
        self.destroy()

        # Configurar la nueva instancia en el cuerpo principal
        self.cuerpo_principal.configure(width=150)
        self.entrenamiento_form.pack_forget()
        self.cuerpo_principal = self.entrenamiento_form
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)