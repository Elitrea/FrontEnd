import random
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, font, Text, Scrollbar
import pandas as pd
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana
import numpy as np
import itertools
from tkinter import messagebox
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os
import csv
from datetime import datetime
import seaborn as sns
from statsmodels.formula.api import ols
import statsmodels.api as sm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


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
        # Definir la fuente predeterminada
        font.nametofont("TkDefaultFont").configure(family="Helvetica", size=12)

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

        red_neuronal_options = ["MLP"]  # Reemplazar con opciones reales
        self.red_neuronal_selector = ttk.Combobox(self.cuerpo_principal, values=red_neuronal_options, font=("Roboto", 12))
        self.red_neuronal_selector.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.red_neuronal_selector.current(0)
        self.red_neuronal_selector.config(state='disabled')


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

        # Selector de Variables
        self.labelVariables = tk.Label(self.cuerpo_principal, text="Variables:")
        self.labelVariables.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.labelVariables.config(font=("Roboto", 12))

        variables_options = ["4"]  # Reemplazar con opciones reales
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

            self.campos_variables[i]["selector_nombre"].config(state='disabled')

            # Almacena la opción seleccionada
            selected_options.append(self.campos_variables[i]["selector_nombre"].get())

            # Label y Entry para Valores de Variable
            #self.campos_variables[i]["label_valores"].grid(row=4 + i, column=2, padx=10, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_1"].grid(row=4 + i, column=1, padx=5, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_2"].grid(row=4 + i, column=2, padx=5, pady=10, sticky="w")
            self.campos_variables[i]["entry_valores_3"].grid(row=4 + i, column=3, padx=5, pady=10, sticky="w")
    
    def optimizar(self):
        # Validar que los selectores no estén vacíos
        if self.red_neuronal_selector.get() == "" or \
        self.porcentaje_selector.get() == "" or \
        self.variables_selector.get() == "":
            tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        # Lógica para procesar la información del formulario de optimización
        red_neuronal = "Red Neuronal: " + self.red_neuronal_selector.get()
        porcentaje_validacion = "Porcentaje de Validación: " + self.porcentaje_selector.get()
        porcentaje = self.porcentaje_selector_opciones.get()
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
            if not valores_variable_1.replace('.', '', 1).isdigit() or \
            not valores_variable_2.replace('.', '', 1).isdigit() or \
            not valores_variable_3.replace('.', '', 1).isdigit():
                tk.messagebox.showerror("Error", "Las entradas de valores deben ser números.")
                return  # Detener la ejecución

            variables.append(f'Variable {i + 1}: {nombre_variable}, Valores: {valores_variable_1}, {valores_variable_2}, {valores_variable_3}')

        # Generar la matriz de pruebas
        resultado, matriz_resultado= self.generar_matriz_pruebas(variables)

        # Mostrar la salida en forma de tabla debajo del botón "Optimizar"
        self.mostrar_salida_tabla(resultado,matriz_resultado,porcentaje)

    def mostrar_salida_tabla(self, resultado, matriz_resultado, porcentaje):
        # Crear un nuevo Toplevel para mostrar la tabla
        ventana_tabla = tk.Toplevel(self)
        ventana_tabla.title("Resultado de Optimización")

        # Crear el encabezado de la tabla
        encabezado = ["Variable" + str(i + 1) for i in range(int(self.variables_selector.get()))]
        encabezado.insert(0, "Combinación")
        encabezado.append("G1")
        encabezado.append("G2")
        encabezado.append("G3")
        encabezado.append("G4")
        encabezado.append("Average")  # Nueva columna para el resultado

        # Crear el widget Treeview
        tree = ttk.Treeview(ventana_tabla, columns=encabezado, show="headings", selectmode="none")
        tree.pack(padx=10, pady=10)

        # Añadir el encabezado
        for col in encabezado:
            tree.heading(col, text=col)

        # Ajustar el ancho de las columnas
        for col in encabezado:
            tree.column(col, width=80)  # Ajustar el ancho a 80 píxeles

        # Dividir las líneas en una lista
        lineas = resultado.strip().split("\n")

        datos = []

        # Añadir las filas a la tabla
        for i, linea in enumerate(lineas, start=1):
            # Obtener los valores de la fila
            valores_fila = linea.split("\t")

            # Llamar al método entrenar() para cada celda de las columnas G1, G2, G3 y G4
            resultados_entrenamiento = []

            for col_index in range(4):  # Repetir 4 veces para las 4 columnas
                # Obtener los valores específicos de matriz_resultado usando los índices proporcionados por los bucles for
                learning_rate = matriz_resultado[i-1][2] 
                momentum = matriz_resultado[i-1][3] 
                neurons = [int(matriz_resultado[i-1][0]), int(matriz_resultado[i-1][1])]

                # Calcular otros parámetros fijos
                valores = [int(x) for x in porcentaje.split(',')]  
                if len(valores) == 2:
                    train_size = valores[0] / 100
                    test_size = valores[1] / 100
                    val_size = 0.0
                elif len(valores) == 3:
                    train_size = valores[0] / 100
                    val_size = valores[1] / 100
                    test_size = valores[2] / 100
                else:
                    train_size = test_size = val_size = 0.0  # Valores por defecto si el formato no es el esperado

                hidden_layers = 2

                # Llamar a la función entrenarSequential() con los parámetros obtenidos
                resultado_entrenamiento = self.entrenarFalse(learning_rate, momentum, train_size, test_size, val_size, hidden_layers, neurons)
                resultados_entrenamiento.append(resultado_entrenamiento)

            # Calcular el promedio de G1, G2, G3 y G4
            promedio = sum(resultados_entrenamiento) / 4

            # Añadir la fila a la tabla junto con los valores de G1, G2, G3, G4 y el promedio
            fila = [i, *valores_fila, *resultados_entrenamiento, promedio]
            tree.insert("", "end", values=fila)
            datos.append(fila)

        # Ajustar la posición de la ventana
        ventana_tabla.geometry("+{}+{}".format(self.winfo_rootx() + 250, self.winfo_rooty() + 420))

        # Crear el DataFrame con los datos extraídos
        df = pd.DataFrame(datos, columns=encabezado)
        self.mostrar_resultados_anova(df)

    def mostrar_resultados_anova(self, df):
        # Crear ventana principal
        resultados_window = tk.Toplevel(self)
        resultados_window.title("Resultados ANOVA")

        # Crear un frame para los resultados
        frame_resultados = tk.Frame(resultados_window)
        frame_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un widget ScrolledText para mostrar los resultados
        text_resultados = scrolledtext.ScrolledText(frame_resultados, wrap=tk.WORD, width=50, height=10)
        text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Calcular las medias y desviaciones estándar de los entrenamientos
        df['Media'] = df[['G1', 'G2', 'G3', 'G4']].mean(axis=1)
        df['DesviacionEstandar'] = df[['G1', 'G2', 'G3', 'G4']].std(axis=1)

        # Calcular la desviación estándar de cada variable
        desviaciones_estandar = df[['G1', 'G2', 'G3', 'G4']].std()

        # Matriz de correlación
        corr = df[['Variable1', 'Variable2', 'Variable3', 'Variable4', 'Media']].corr()

        # Crear una figura para las gráficas
        fig, axs = plt.subplots(2, 1, figsize=(10, 20), gridspec_kw={'height_ratios': [4, 4]})

        # Graficar las desviaciones estándar de cada variable
        axs[0].bar(desviaciones_estandar.index, desviaciones_estandar.values)
        axs[0].set_title('Desviación Estándar de Cada Variable')
        axs[0].set_ylim(0, max(desviaciones_estandar.values) * 1.2)  # Ajustar el límite del eje Y
        axs[0].set_ylabel('Desviación Estándar')

        # Graficar la matriz de correlación
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=axs[1])
        axs[1].set_title('Matriz de Correlación de los Parámetros y la Media')

        # Ajustar el espacio entre las subgráficas
        plt.subplots_adjust(hspace=0.4, top=0.95, bottom=0.05, left=0.05, right=0.95)

        # Crear un frame para la figura de la gráfica
        fig_frame = tk.Frame(resultados_window, width=800, height=500)
        fig_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Mostrar la figura con las gráficas
        canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Crear una barra de desplazamiento para la figura
        toolbar = NavigationToolbar2Tk(canvas, fig_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Encontrar el índice del entrenamiento con la media más alta
        indice_mejor_entrenamiento = df['Media'].idxmax()

        # Obtener los nombres de los entrenamientos
        mejores_entrenamientos = df.loc[indice_mejor_entrenamiento, ['G1', 'G2', 'G3', 'G4']]
        text_resultados.insert(tk.END, "Los mejores entrenamientos fueron:\n")
        text_resultados.insert(tk.END, f"{mejores_entrenamientos}\n")

        # Obtener los valores de los parámetros para el mejor entrenamiento
        valores_mejores_parametros = df.loc[indice_mejor_entrenamiento, ['Variable1', 'Variable2', 'Variable3', 'Variable4']]
        text_resultados.insert(tk.END, "Los valores de los parámetros que corresponden al mejor entrenamiento fueron:\n")
        text_resultados.insert(tk.END, f"{valores_mejores_parametros}\n")

        # Mostrar la figura con las gráficas
        canvas = FigureCanvasTkAgg(fig, master=frame_resultados)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crear una barra de desplazamiento para la figura
        toolbar = NavigationToolbar2Tk(canvas, frame_resultados)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def mostrar_graficas(self, parent_window, df, anova_table):
        # Crear una nueva ventana para mostrar la figura con las gráficas
        fig_window = tk.Toplevel(parent_window)
        fig_window.title("Gráficas ANOVA")

        # Crear un frame para los resultados
        frame_resultados = tk.Frame(fig_window)
        frame_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear un widget ScrolledText para mostrar los resultados
        text_resultados = scrolledtext(frame_resultados, wrap=tk.WORD, width=100, height=20)
        text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Verificar nombres de columnas
        text_resultados.insert(tk.END, f"Columnas del DataFrame: {df.columns}\n")

        # Mostrar la tabla ANOVA
        text_resultados.insert(tk.END, f"\nResultados del ANOVA:\n{anova_table}\n")

        # Calcular las medias y desviaciones estándar de los entrenamientos
        df['Media'] = df[['G1', 'G2', 'G3', 'G4']].mean(axis=1)
        df['DesviacionEstandar'] = df[['G1', 'G2', 'G3', 'G4']].std(axis=1)

        # Crear una figura de Matplotlib con subgráficos y espacio entre ellos
        fig, axs = plt.subplots(3, 1, figsize=(8, 12), sharex=True, gridspec_kw={'hspace': 0.5})

        # Graficar las medias
        sns.barplot(x='Variable1', y='Media', hue='Variable2', data=df, ax=axs[0])
        axs[0].set_title('Media de los Resultados de los Entrenamientos')

        sns.barplot(x='Variable1', y='DesviacionEstandar', hue='Variable2', data=df, ax=axs[1])
        axs[1].set_title('Desviación Estándar de los Resultados de los Entrenamientos')

        # Matriz de correlación
        corr = df[['Variable1', 'Variable2', 'Variable3', 'Variable4', 'Media']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=axs[2])
        axs[2].set_title('Matriz de Correlación de los Parámetros y la Media')

        # Ajustar el espacio entre las subgráficas
        plt.tight_layout()  # Ajustar el diseño para evitar superposiciones

        # Mostrar la figura en la ventana
        canvas = FigureCanvasTkAgg(fig, master=frame_resultados)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crear una barra de desplazamiento para la figura
        toolbar = NavigationToolbar2Tk(canvas, frame_resultados)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def guardar_resultado(self, matriz_resultado, resultado_entrenamiento):
        # Encabezados para las columnas de la matriz_resultado
        encabezados_matriz = ["Neuronas Capa 1", "Neuronas Capa 2", "Taza de Aprendizaje", "Momento"]

        # Convertir la matriz_resultado en DataFrame con los encabezados correspondientes
        df_matriz_resultado = pd.DataFrame(matriz_resultado, columns=encabezados_matriz)

        # Convertir los valores en resultado_entrenamiento a números (si es posible)
        try:
            resultado_entrenamiento = [float(valor) for valor in resultado_entrenamiento]
        except ValueError:
            messagebox.showerror("Error", "Los valores en resultado_entrenamiento no son numéricos.")
            return

        # Calcular el promedio de G1, G2, G3 y G4 para cada fila de la matriz_resultado
        promedio = sum(resultado_entrenamiento) / 4

        # Agregar la columna de promedio a la matriz_resultado
        df_matriz_resultado["Average"] = promedio

        # Abrir el diálogo de guardar archivo y obtener la ruta de destino
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivo Excel", "*.xlsx")])

        if ruta_guardado:
            try:
                # Guardar el DataFrame en un archivo Excel en la ruta especificada
                df_matriz_resultado.to_excel(ruta_guardado, index=False)
                messagebox.showinfo("Guardado", "Los datos se han guardado correctamente en el archivo Excel.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al intentar guardar el archivo: {str(e)}")
        else:
            messagebox.showinfo("Cancelado", "La operación de guardado ha sido cancelada.")

    def entrenarFalse(self, learning_rate, momentum, train_size, test_size, val_size, hidden_layers, neurons):
        return random.random()

    def entrenarSequential(self, learning_rate, momentum, train_size, test_size, val_size, hidden_layers, neurons):
            print("Valores recibidos:")
            print("Learning Rate:", learning_rate)
            print("Momentum:", momentum)
            print("Train Size:", train_size)
            print("Test Size:", test_size)
            print("Validation Size:", val_size)
            print("Hidden Layers:", hidden_layers)
            print("Neurons:", neurons)
            
            # Cargar los datos desde el archivo CSV
            data = pd.read_csv('Prueba3_3_2_Datos.csv')

            # Separar características (X) y etiquetas (y)
            X = data[['X', 'Y', 'Z', 'Orientation_1_1', 'Orientation_1_2', 'Orientation_1_3',
                    'Orientation_2_1', 'Orientation_2_2', 'Orientation_2_3', 'Orientation_3_1',
                    'Orientation_3_2', 'Orientation_3_3']].values
            y = data[['Theta1', 'Theta2', 'Theta3']].values

            # Dividir el conjunto de datos en conjuntos de entrenamiento, prueba y validación
            X_train, X_remaining, y_train, y_remaining = train_test_split(X, y, test_size=1-train_size, random_state=42)
            X_val, X_test, y_val, y_test = train_test_split(X_remaining, y_remaining, test_size=test_size, random_state=42)

            # Definir la arquitectura del modelo Sequential
            model = tf.keras.Sequential()

            # Agregar capas ocultas según el número especificado
            for i in range(hidden_layers):
                if i == 0:
                    # Primera capa oculta con especificación de la forma de entrada
                    model.add(tf.keras.layers.Dense(neurons[i], activation='relu', input_shape=(X_train.shape[1],)))
                else:
                    model.add(tf.keras.layers.Dense(neurons[i], activation='relu'))

            # Capa de salida con 3 neuronas para las 3 etiquetas
            model.add(tf.keras.layers.Dense(3))

            # Compilar el modelo con el optimizador SGD personalizado
            optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate,momentum=momentum)
            model.compile(loss='mean_squared_error', optimizer=optimizer, metrics=['accuracy'])

            # Entrenar el modelo con datos de entrenamiento y validación
            history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

            # Evaluar el rendimiento del modelo en el conjunto de prueba
            loss_test, _ = model.evaluate(X_test, y_test)
            rmse_test = np.sqrt(loss_test)

            # Determinar el siguiente número consecutivo para el modelo
            numero_consecutivo = self.obtener_siguiente_consecutivo()

            # Guardar el modelo entrenado en formato .h5
            ruta_modelo_h5 = os.path.join('ModelosTaguchi', f'modelo_entrenado_{numero_consecutivo}.h5')
            model.save(ruta_modelo_h5)

            # Guardar información del modelo en el archivo de registro
            modelo_info = {
                "ID": f"Modelo_{numero_consecutivo}",
                "Learning Rate": learning_rate,
                "Momentum": momentum,
                "Train Size": train_size,
                "Test Size": test_size,
                "Validation Size": val_size,
                "Hidden Layers": hidden_layers,
                "Neurons": neurons,
                "RMSE Test": rmse_test
            }
            self.guardar_en_registro(modelo_info)

            return rmse_test
    
    def guardar_en_registro(self, modelo_info):
        # Nombre del archivo de registro
        archivo_registro = os.path.join('ModelosTaguchi', 'logTaguchi.xlsx')

        # Verificar si el archivo ya existe
        existe_archivo = os.path.exists(archivo_registro)

        # Crear DataFrame con la información del modelo
        df_modelo = pd.DataFrame([modelo_info])

        # Si el archivo ya existe, abrirlo y agregar el nuevo modelo
        if existe_archivo:
            # Leer el archivo existente
            df_registros = pd.read_excel(archivo_registro)
            # Concatenar el nuevo registro al DataFrame existente
            df_registros = pd.concat([df_registros, df_modelo], ignore_index=True)
            # Escribir el DataFrame actualizado en el archivo Excel
            df_registros.to_excel(archivo_registro, index=False)
        else:
            # Si el archivo no existe, escribir el DataFrame directamente en el archivo Excel
            df_modelo.to_excel(archivo_registro, index=False)

    def obtener_siguiente_consecutivo(self):
        # Obtener la lista de modelos existentes
        modelos_existentes = [nombre for nombre in os.listdir('ModelosTaguchi') if nombre.startswith('modelo_entrenado_') and nombre.endswith('.h5')]

        # Si no hay modelos existentes, el siguiente número consecutivo es 1
        if not modelos_existentes:
            return 1

        # Encontrar el número más alto entre los modelos existentes y sumar 1
        numero_consecutivo = max([int(nombre.split('_')[-1].split('.')[0]) for nombre in modelos_existentes]) + 1

        return numero_consecutivo

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

        return resultado, matriz_resultado

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