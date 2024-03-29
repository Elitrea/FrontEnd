import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font
import pandas as pd
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana

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
    
    def principal(self):
        # Elementos del formulario
        # ... (Otros elementos que ya existían en tu código)

        # Modelo de red neuronal
        self.modelo_label = tk.Label(self.cuerpo_principal, text="Red Neuronal:")
        self.modelo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.modelo_label.config(font=("Roboto", 12))

        self.modelos_disponibles = ["Modelo 1", "Modelo 2", "Modelo 3"]
        self.modelo_selector = ttk.Combobox(self.cuerpo_principal, values=self.modelos_disponibles, font=("Roboto", 12))
        self.modelo_selector.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Seleccionar archivo
        self.archivo_label = tk.Label(self.cuerpo_principal, text="Seleccionar Archivo:")
        self.archivo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.archivo_label.config(font=("Roboto", 12))

        self.archivo_selector = tk.Button(self.cuerpo_principal, text="Seleccionar Archivo", command=self.seleccionar_archivo)
        self.archivo_selector.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # ID Prueba
        self.id_prueba_label = tk.Label(self.cuerpo_principal, text="ID Prueba:")
        self.id_prueba_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.id_prueba_label.config(font=("Roboto", 12))

        self.id_prueba_selector = ttk.Combobox(self.cuerpo_principal, values=["ID1", "ID2", "ID3"], font=("Roboto", 12))
        self.id_prueba_selector.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Número de neuronas por capa de entrada
        self.neuronas_entrada_label = tk.Label(self.cuerpo_principal, text="Neuronas Entrada:")
        self.neuronas_entrada_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.neuronas_entrada_label.config(font=("Roboto", 12))

        self.neuronas_entrada_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.neuronas_entrada_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Número de neuronas de la capa de salida
        self.neuronas_salida_label = tk.Label(self.cuerpo_principal, text="Neuronas Salida:")
        self.neuronas_salida_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.neuronas_salida_label.config(font=("Roboto", 12))

        self.neuronas_salida_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.neuronas_salida_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Campos generales de taza de aprendizaje, momento y épocas
        self.taza_aprendizaje_label = tk.Label(self.cuerpo_principal, text="Taza de Aprendizaje:")
        self.taza_aprendizaje_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.taza_aprendizaje_label.config(font=("Roboto", 12))

        self.taza_aprendizaje_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.taza_aprendizaje_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.momento_label = tk.Label(self.cuerpo_principal, text="Momento:")
        self.momento_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.momento_label.config(font=("Roboto", 12))

        self.momento_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.momento_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

        self.epocas_label = tk.Label(self.cuerpo_principal, text="Épocas:")
        self.epocas_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.epocas_label.config(font=("Roboto", 12))

        self.epocas_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.epocas_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # Pregunta sobre el porcentaje
        self.porcentaje_pregunta_label = tk.Label(self.cuerpo_principal, text="¿Desea porcentaje?")
        self.porcentaje_pregunta_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")
        self.porcentaje_pregunta_label.config(font=("Roboto", 12))

        opciones_porcentaje = ["Sí", "No"]
        self.porcentaje_selector = ttk.Combobox(self.cuerpo_principal, values=opciones_porcentaje, font=("Roboto", 12))
        self.porcentaje_selector.grid(row=9, column=1, padx=10, pady=10, sticky="w")
        self.porcentaje_selector.bind("<<ComboboxSelected>>", self.activar_caja_porcentaje)

        self.porcentaje_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12), state="disabled")
        self.porcentaje_entry.grid(row=9, column=2, padx=10, pady=10, sticky="w")
        
        #Pregunta porcentajes de entrenamiento 
        self.id_prueba_label = tk.Label(self.cuerpo_principal, text="Porcentajes:")
        self.id_prueba_label.grid(row=10, column=0, padx=10, pady=10, sticky="w")
        self.id_prueba_label.config(font=("Roboto", 12))

        self.id_prueba_selector = ttk.Combobox(self.cuerpo_principal, values=["80,20", "90,10", "70,30"], font=("Roboto", 12))
        self.id_prueba_selector.grid(row=10, column=1, padx=10, pady=10, sticky="w")

        # Número de capas ocultas y configuración
        self.capas_ocultas_label = tk.Label(self.cuerpo_principal, text="Capas Ocultas:")
        self.capas_ocultas_label.grid(row=11, column=0, padx=10, pady=10, sticky="w")
        self.capas_ocultas_label.config(font=("Roboto", 12))

        self.capas_ocultas_entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
        self.capas_ocultas_entry.grid(row=11, column=1, padx=10, pady=10, sticky="w")

        # Botón para generar configuración dinámica de capas ocultas
        self.generar_configuracion_button = tk.Button(self.cuerpo_principal, text="Generar Configuración", command=self.configuracion_capas)
        self.generar_configuracion_button.grid(row=11, column=2, padx=10, pady=10, sticky="w")

       

        # Resto del formulario
        # ... (Otros elementos que ya existían en tu código)

        # Botón de enviar
        self.enviar_button = tk.Button(self.cuerpo_principal, text="Enviar", command=self.enviar_formulario, font=("Roboto", 14))
        self.enviar_button.grid(row=12, column=0, columnspan=2, pady=10)

        # Botón de guardar modelo
        self.enviar_button = tk.Button(self.cuerpo_principal, text="Guardar modelo", command=self.enviar_formulario, font=("Roboto", 14))
        self.enviar_button.grid(row=13, column=0, columnspan=2, pady=10)

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

            activation_options = ["Función 1", "Función 2", "Función 3"]  # Reemplazar con opciones reales
            activation_selector = ttk.Combobox(self.cuerpo_principal, values=activation_options, font=("Roboto", 12), name=f'activacion_capa_{i + 1}_selector')
            activation_selector.grid(row=10 + i, column=3, padx=10, pady=10, sticky="w")

            # Agregar entry y selector a las listas
            self.config_entries.append(entry)
            self.activation_selectors.append(activation_selector)

    def enviar_formulario(self):
        # Lógica para procesar la información del formulario
        modelo = "Modelo: " + self.modelo_selector.get()
        id_prueba = "ID Prueba: " + self.id_prueba_selector.get()
        num_capas_ocultas = "Número de Capas Ocultas: " + self.capas_ocultas_entry.get()
        
        num_neuronas_capa_x = []
        funciones_activacion_capa_x = []

        for i in range(len(self.config_entries)):
            num_neuronas = self.config_entries[i].get()
            funcion_activacion = self.activation_selectors[i].get()
            num_neuronas_capa_x.append(f'Neuronas Capa {i + 1}: {num_neuronas}')
            funciones_activacion_capa_x.append(f'Activación Capa {i + 1}: {funcion_activacion}')

        taza_aprendizaje = "Taza de Aprendizaje: " + self.taza_aprendizaje_entry.get()
        momento = "Momento: " + self.momento_entry.get()
        epocas = "Épocas: " + self.epocas_entry.get()
        porcentaje = "Porcentaje: " + self.porcentaje_entry.get() if self.porcentaje_selector.get() == "Sí" else "Porcentaje: No aplica"

        # Imprime la información (puedes ajustar esto según tus necesidades)
        print(modelo, id_prueba, num_capas_ocultas)
        print(num_neuronas_capa_x)
        print(funciones_activacion_capa_x)
        print(taza_aprendizaje, momento, epocas, porcentaje)

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