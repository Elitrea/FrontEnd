import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import font
import pandas as pd
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana
import numpy as np
import itertools

class TaguchiForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Formulario Taguchi')
        self.config_entries = []
        self.activation_selectors = []
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.principal()

    def config_window(self):
        # Configuracion incial de la ventana
        self.title('Taguchi')
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
        self.labelTitulo = tk.Label(self.barra_superior, text="Taguchi")
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
        # Selector de Red Neuronal
        self.labelRedNeuronal = tk.Label(self.cuerpo_principal, text="Red Neuronal:")
        self.labelRedNeuronal.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.labelRedNeuronal.config(font=("Roboto", 12))

        red_neuronal_options = ["Sequential", "Deep Learning"]  # Reemplazar con opciones reales
        self.red_neuronal_selector = ttk.Combobox(self.cuerpo_principal, values=red_neuronal_options, font=("Roboto", 12))
        self.red_neuronal_selector.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Selector de Porcentaje de Validación
        self.labelPorcentajeValidacion = tk.Label(self.cuerpo_principal, text="¿Porcentaje de Validación?")
        self.labelPorcentajeValidacion.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.labelPorcentajeValidacion.config(font=("Roboto", 12))

        self.porcentaje_selector = ttk.Combobox(self.cuerpo_principal, values=["No", "Sí"], font=("Roboto", 12))
        self.porcentaje_selector.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.porcentaje_selector.bind("<<ComboboxSelected>>", self.mostrar_campos_porcentaje)

        # Selector de Porcentaje
        self.labelPorcentaje = tk.Label(self.cuerpo_principal, text="Porcentaje:")
        self.labelPorcentaje.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.labelPorcentaje.config(font=("Roboto", 12))

        porcentaje_options_no = ["80,20", "90,10"]  # Reemplazar con opciones reales
        porcentaje_options_si = ["80,10,10", "70,20,10"]  # Reemplazar con opciones reales

        self.porcentaje_selector_opciones = ttk.Combobox(self.cuerpo_principal, font=("Roboto", 12))
        self.porcentaje_selector_opciones.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.porcentaje_selector_opciones.config(state=tk.DISABLED)

        # Selector de Variables
        self.labelVariables = tk.Label(self.cuerpo_principal, text="Variables:")
        self.labelVariables.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.labelVariables.config(font=("Roboto", 12))

        variables_options = ["3", "4"]  # Reemplazar con opciones reales
        self.variables_selector = ttk.Combobox(self.cuerpo_principal, values=variables_options, font=("Roboto", 12))
        self.variables_selector.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.variables_selector.bind("<<ComboboxSelected>>", self.mostrar_campos_variables)

        # Campos dinámicos para Variables
        self.campos_variables = []
        for i in range(4):  # Crear hasta 4 campos, puedes ajustar según necesidad
            self.campos_variables.append({
                #"label": tk.Label(self.cuerpo_principal, text=f"Variable {i+1} Nombre:"),
                "selector_nombre": ttk.Combobox(self.cuerpo_principal, font=("Roboto", 12)),
                "label_valores": tk.Label(self.cuerpo_principal, text=f"Variable {i+1} Valores:"),
                "entry_valores_1": tk.Entry(self.cuerpo_principal, font=("Roboto", 12)),
                "entry_valores_2": tk.Entry(self.cuerpo_principal, font=("Roboto", 12)),
                "entry_valores_3": tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
            })
            # Establecer un valor predeterminado de "0" en las cajas de texto
            self.campos_variables[i]["entry_valores_1"].insert(0, "0")
            self.campos_variables[i]["entry_valores_2"].insert(0, "0")
            self.campos_variables[i]["entry_valores_3"].insert(0, "0")

        # Botón de Optimizar
        self.optimizar_button = tk.Button(self.cuerpo_principal, text="Optimizar", command=self.optimizar, font=("Roboto", 12, "bold"), bg="#800040", fg="white")
        self.optimizar_button.grid(row=10, column=0, columnspan=2, pady=10)

    def mostrar_campos_porcentaje(self, event):
        # Mostrar o desactivar el selector de porcentaje según la selección del usuario
        if self.porcentaje_selector.get() == "Sí":
            opciones_porcentaje_si = ["80,10,10", "70,20,10"]  # Opciones cuando la respuesta es 'Sí'
            self.porcentaje_selector_opciones["values"] = opciones_porcentaje_si
            self.porcentaje_selector_opciones.config(state=tk.NORMAL)
        else:
            opciones_porcentaje_no = ["80,20", "90,10"]  # Opciones cuando la respuesta es 'No'
            self.porcentaje_selector_opciones["values"] = opciones_porcentaje_no
            self.porcentaje_selector_opciones.set("")  # Limpiar selección
            self.porcentaje_selector_opciones.config(state=tk.NORMAL)

    def mostrar_campos_variables(self, event):
        # Mostrar campos dinámicamente según la cantidad de variables seleccionadas
        num_variables = int(self.variables_selector.get())

        # Lista de opciones para el selector de nombre de variable (puedes personalizar según tus necesidades)
        opciones_nombres_variable = ["Neuronas capa 1", "Neuronas capa 2", "Taza de aprendizaje", "Momento"]

        # Lista para rastrear las opciones ya seleccionadas
        selected_options = []

        for i in range(4):  # Ocultar todos los campos primero
            #self.campos_variables[i]["label"].grid_forget()
            self.campos_variables[i]["selector_nombre"].grid_forget()
            self.campos_variables[i]["label_valores"].grid_forget()
            self.campos_variables[i]["entry_valores_1"].grid_forget()
            self.campos_variables[i]["entry_valores_2"].grid_forget()
            self.campos_variables[i]["entry_valores_3"].grid_forget()

        for i in range(num_variables):  # Mostrar solo los necesarios
            # Label y Selector para Nombre de Variable
            #self.campos_variables[i]["label"].grid(row=4 + i, column=0, padx=10, pady=10, sticky="w")
            self.campos_variables[i]["selector_nombre"].grid(row=4 + i, column=0, padx=10, pady=10, sticky="w")

            # Configuración del Selector de Nombre de Variable
            opciones = [opt for opt in opciones_nombres_variable if opt not in selected_options]  # Eliminar opciones ya seleccionadas
            self.campos_variables[i]["selector_nombre"]["values"] = opciones
            self.campos_variables[i]["selector_nombre"].current(0)  # Seleccionar la primera opción por defecto

            # Almacena la opción seleccionada
            selected_options.append(self.campos_variables[i]["selector_nombre"].get())

            # Label y Entry para Valores de Variable
            #self.campos_variables[i]["label_valores"].grid(row=4 + i, column=2, padx=10, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_1"].grid(row=4 + i, column=1, padx=5, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_2"].grid(row=4 + i, column=2, padx=5, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_3"].grid(row=4 + i, column=3, padx=5, pady=10, sticky="w")
    
    def optimizar(self):
        # Lógica para procesar la información del formulario de optimización
        red_neuronal = "Red Neuronal: " + self.red_neuronal_selector.get()
        porcentaje_validacion = "Porcentaje de Validación: " + self.porcentaje_selector.get()
        porcentaje = "Porcentaje: " + self.porcentaje_selector_opciones.get()
        variables = []
        selected_names = set()  # Conjunto para rastrear nombres de variables seleccionados
        for i in range(int(self.variables_selector.get())):
            nombre_variable = self.campos_variables[i]["selector_nombre"].get()
            # Valida si el nombre de la variable está duplicado
            if nombre_variable in selected_names:
                tk.messagebox.showerror("Error", f"La variable '{nombre_variable}' está duplicada.")
                return  # Detener la ejecución
            else:
                selected_names.add(nombre_variable)

            valores_variable_1 = self.campos_variables[i]["entry_valores_1"].get()
            valores_variable_2 = self.campos_variables[i]["entry_valores_2"].get()
            valores_variable_3 = self.campos_variables[i]["entry_valores_3"].get()

            # Valida si las entradas de valores son números
            if not valores_variable_1.isdigit() or not valores_variable_2.isdigit() or not valores_variable_3.isdigit():
                tk.messagebox.showerror("Error", "Las entradas de valores deben ser números.")
                return  # Detener la ejecución

            variables.append(f'Variable {i + 1}: {nombre_variable}, Valores: {valores_variable_1}, {valores_variable_2}, {valores_variable_3}')

        # Generar la matriz de pruebas
        resultado = self.generar_matriz_pruebas(variables)

        # Mostrar la salida en forma de tabla debajo del botón "Optimizar"
        self.mostrar_salida_tabla(resultado)

    def mostrar_salida_tabla(self, resultado):
        # Crear un nuevo marco para la tabla
        self.frame_tabla = tk.Frame(self.cuerpo_principal, bg=COLOR_CUERPO_PRINCIPAL)
        self.frame_tabla.grid(row=11, column=0, columnspan=2, pady=10)

        # Crear el encabezado de la tabla
        encabezado = ["Variable " + str(i + 1) for i in range(int(self.variables_selector.get()))]
        encabezado.insert(0, "Combinación")
        encabezado.append("G1")
        encabezado.append("G2")
        encabezado.append("G3")
        encabezado.append("G4")
        encabezado.append("Average")  # Nueva columna para el resultado
        encabezado.append("S/N")  # Nueva columna para el resultado
        encabezado = tuple(encabezado)

        # Crear el widget Treeview
        self.tree = ttk.Treeview(self.frame_tabla, columns=encabezado, show="headings", selectmode="none")
        self.tree.grid(row=0, column=0)

        # Añadir el encabezado
        for col in encabezado:
            self.tree.heading(col, text=col)

        # Ajustar el ancho de las columnas
        for col in encabezado:
            self.tree.column(col, width=80)  # Ajustar el ancho a 80 píxeles

        # Dividir las líneas en una lista
        lineas = resultado.strip().split("\n")

        # Añadir las filas a la tabla
        for i, linea in enumerate(lineas, start=1):
            resultado_entrenamiento = self.entrenar()  # Llamar al método entrenar
            self.tree.insert("", "end", values=(i, *linea.split("\t"), resultado_entrenamiento))  # Añadir resultado de entrenamiento

        # Añadir barra de desplazamiento
        scroll_y = tk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scroll_y.set)

    def entrenar(self):
        # Lógica para entrenar el modelo
        # Por ahora solo retorna 1, reemplazar con la lógica real de entrenamiento
        return 1
    
    def generar_matriz_pruebas(self, variables):
        # Obtener los niveles ingresados por el usuario para cada variable
        niveles_usuario = []
        for campo in self.campos_variables:
            niveles_usuario.append([
                float(campo["entry_valores_1"].get()),
                float(campo["entry_valores_2"].get()),
                float(campo["entry_valores_3"].get())
            ])

        if len(variables) == 3:
            # Crear la matriz con las posiciones especificadas para 3 variables
            matriz_resultado = [
                [niveles_usuario[0][0], niveles_usuario[1][0], niveles_usuario[2][0]],
                [niveles_usuario[0][0], niveles_usuario[1][1], niveles_usuario[2][1]],
                [niveles_usuario[0][0], niveles_usuario[1][2], niveles_usuario[2][2]],
                [niveles_usuario[0][1], niveles_usuario[1][0], niveles_usuario[2][1]],
                [niveles_usuario[0][1], niveles_usuario[1][1], niveles_usuario[2][2]],
                [niveles_usuario[0][1], niveles_usuario[1][2], niveles_usuario[2][0]],
                [niveles_usuario[0][2], niveles_usuario[1][0], niveles_usuario[2][2]],
                [niveles_usuario[0][2], niveles_usuario[1][1], niveles_usuario[2][0]],
                [niveles_usuario[0][2], niveles_usuario[1][2], niveles_usuario[2][1]],
            ]
        elif len(variables) == 4:
            # Crear la matriz con las posiciones especificadas para 4 variables
            matriz_resultado = [
                [niveles_usuario[0][0], niveles_usuario[1][0], niveles_usuario[2][0], niveles_usuario[3][0]],
                [niveles_usuario[0][0], niveles_usuario[1][1], niveles_usuario[2][1], niveles_usuario[3][1]],
                [niveles_usuario[0][0], niveles_usuario[1][2], niveles_usuario[2][2], niveles_usuario[3][2]],
                [niveles_usuario[0][1], niveles_usuario[1][0], niveles_usuario[2][1], niveles_usuario[3][2]],
                [niveles_usuario[0][1], niveles_usuario[1][1], niveles_usuario[2][2], niveles_usuario[3][0]],
                [niveles_usuario[0][1], niveles_usuario[1][2], niveles_usuario[2][0], niveles_usuario[3][1]],
                [niveles_usuario[0][2], niveles_usuario[1][0], niveles_usuario[2][2], niveles_usuario[3][1]],
                [niveles_usuario[0][2], niveles_usuario[1][1], niveles_usuario[2][0], niveles_usuario[3][2]],
                [niveles_usuario[0][2], niveles_usuario[1][2], niveles_usuario[2][1], niveles_usuario[3][0]],
            ]
        else:
            tk.messagebox.showerror("Error", "La cantidad de variables debe ser 3 o 4.")
            return ""

        # Formar el resultado como una cadena
        resultado = ""
        for fila in matriz_resultado:
            resultado += '\t'.join(map(str, fila)) + '\n'

        return resultado

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
        self.taguchi_form.pack_forget()
        self.cuerpo_principal = self.taguchi_form
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def abrir_ventana_usuario(self):
        from formularios.form_usuario import UsuarioForm
        # Verificar si ya hay una instancia de UsuarioForm
        if not hasattr(self, 'usuario_form'):
            # Crear una nueva instancia solo si no existe
            self.usuario_form = UsuarioForm()
        # Ocultar y destruir la instancia actual de TaguchiForm
        self.withdraw()
        self.destroy()

        # Configurar la nueva instancia en el cuerpo principal
        self.cuerpo_principal.configure(width=150)
        self.usuario_form.pack_forget()
        self.cuerpo_principal = self.usuario_form
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)