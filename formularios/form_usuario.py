import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
import serial.tools.list_ports
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana
import numpy as np
from tensorflow.keras.models import load_model
import time
import serial



class UsuarioForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Formulario Usuario')
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.principal()
        
    def config_window(self):
        # Configuración inicial de la ventana
        self.title('Usuario')
        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Configurar el ancho y alto de la ventana para cubrir toda la pantalla
        self.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
        # Definir la fuente predeterminada
        font.nametofont("TkDefaultFont").configure(family="Helvetica", size=12)
    
    def paneles(self):
        # Crear paneles
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL, width=150)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Usuario")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=20)
        self.labelTitulo.pack(side=tk.LEFT)

    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        # Botones del menú lateral
        botones_info = [
            ("Usuario", "\uf007", self.abrir_ventana_usuario),
            ("Entrenamiento", "\uf0c0", self.abrir_ventana_entrenamiento),
            ("Taguchi", "\uf03e", self.abrir_ventana_taguchi)
        ]

        for text, icon, command in botones_info:
            button = tk.Button(self.menu_lateral, command=command)
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)
    
    def principal(self):
        # Botón para seleccionar archivo
        data_file_button = tk.Button(self.cuerpo_principal, text="Seleccionar archivo de datos", command=self.select_data_file, font=("Roboto", 12, "bold"), bg="#800040", fg="white")
        data_file_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Etiqueta para mostrar el nombre del archivo seleccionado
        self.data_file_label = tk.Label(self.cuerpo_principal, text="Ningún archivo seleccionado", font=("Roboto", 12))
        self.data_file_label.grid(row=0, column=2, columnspan=3, padx=10, pady=10, sticky="w")

        # Combobox para seleccionar el puerto COM
        com_label = tk.Label(self.cuerpo_principal, text="Seleccionar puerto COM:", font=("Roboto", 12))
        com_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="w")

        self.combobox_com = ttk.Combobox(self.cuerpo_principal, values=self.get_available_com_ports(), font=("Roboto", 12))
        self.combobox_com.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

        coordenadas_labels_text = ["X", "Y", "Z"]
        self.coordenadas_labels = []
        for i, text in enumerate(coordenadas_labels_text):
            label = tk.Label(self.cuerpo_principal, text=f"Coordenada {text}:")
            label.grid(row=6, column=i * 2, padx=10, pady=(10, 5), sticky="w")
            label.config(font=("Roboto", 12))
            self.coordenadas_labels.append(label)

        # Entradas de coordenadas
        self.coordenadas_entries = []
        for i in range(3):
            entry = tk.Entry(self.cuerpo_principal, font=("Roboto", 12))
            entry.grid(row=7, column=i * 2 + 1, padx=5, pady=(8, 5), sticky="w")
            self.coordenadas_entries.append(entry)

        # Botón de enviar
        self.enviar_button = tk.Button(self.cuerpo_principal, text="Enviar", command=self.enviar_formulario, font=("Roboto", 12, "bold"), bg="#800040", fg="white")
        self.enviar_button.grid(row=10, column=1, columnspan=2, pady=(10, 5), sticky="w")

    def get_available_com_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def select_data_file(self):
        self.data_file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.h5")])
        if self.data_file_path:
            self.data_file_label.config(text=self.data_file_path)
            self.model = load_model(self.data_file_path)


    def enviar_formulario(self):
        # Validar que se haya seleccionado un archivo
        if not hasattr(self, 'data_file_path') or not self.data_file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo de datos.")
            return

        # Validar que se haya seleccionado un puerto COM
        selected_com_port = self.combobox_com.get()
        if not selected_com_port:
            messagebox.showerror("Error", "Por favor, selecciona un puerto COM.")
            return

        # Validar coordenadas
        coordenadas = [entry.get() for entry in self.coordenadas_entries]
        if not self.validar_coordenadas(coordenadas):
            messagebox.showerror("Error de validación", "Las coordenadas deben ser valores numéricos.")
            return

        # Convertir coordenadas a float
        x, y, z = map(float, coordenadas)

        # Organizar las entradas y orientaciones en una matriz
        orientation_1 = [1, 0, 0]
        orientation_2 = [0, 1, 0]
        orientation_3 = [0, 0, 1]
        X = np.array([[x, y, z] + orientation_1 + orientation_2 + orientation_3])

        # Utilizar el modelo para hacer predicciones
        prediction = self.model.predict(X)

        # Convertir las predicciones de radianes a grados
        prediccion_grados = self.radianes_a_grados(prediction)

        # Asignar los valores de la predicción en grados a variables individuales
        valor_prediccion_0, valor_prediccion_1, valor_prediccion_2 = prediccion_grados[0]

        # Ajustar los valores negativos sumando 180
        if valor_prediccion_0 < 0:
            valor_prediccion_0 += 180
        if valor_prediccion_1 < 0:
            valor_prediccion_1 += 180
        if valor_prediccion_2 < 0:
            valor_prediccion_2 += 180

        # Verificar si algún valor de predicción está fuera del rango permitido (0 a 180 grados)
        if valor_prediccion_0 > 180 or valor_prediccion_1 > 180 or valor_prediccion_2 > 180:
            messagebox.showerror("Error", "Valores fuera del rango")
            return

        # Establecer la conexión con Arduino
        try:
            arduino = serial.Serial(selected_com_port, 9600, timeout=1)
            time.sleep(2)  # Esperar a que se establezca la conexión
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo establecer conexión con Arduino: {e}")
            return

        # Enviar las predicciones a los servos
        try:
            arduino.write(f'{int(valor_prediccion_0)},{int(valor_prediccion_1)},{int(valor_prediccion_2)}\n'.encode())
            arduino.close()
        except Exception as e:
            messagebox.showerror("Error de envío", f"No se pudo enviar los datos a Arduino: {e}")
            return

        messagebox.showinfo("Éxito", "Coordenadas enviadas correctamente a Arduino")

    def validar_coordenadas(self, coordenadas):
        if len(coordenadas) != 3:
            return False
        try:
            for coord in coordenadas:
                float(coord)
        except ValueError:
            return False
        return True


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
        # Cambiar estilo al pasar el ratón por encima
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
    
    # Función para convertir radianes a grados
    def radianes_a_grados(self, radianes):
        return radianes * 57.2958


if __name__ == "__main__":
    app = UsuarioForm()
    app.mainloop()