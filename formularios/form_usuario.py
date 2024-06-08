import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from config import COLOR_BARRA_SUPERIOR, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA, COLOR_MENU_LATERAL
import util.util_ventana as util_ventana


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

    def select_data_file(self):
        self.data_file_path = filedialog.askopenfilename(filetypes=[("Model files", "*.h5")])
        if self.data_file_path:
            self.data_file_label.config(text=self.data_file_path)


    def enviar_formulario(self):
        # Validar que se haya seleccionado un archivo
        if not hasattr(self, 'data_file_path') or not self.data_file_path:
            messagebox.showerror("Error", "Por favor, selecciona un archivo de datos.")
            return

        # Validar coordenadas
        coordenadas = [entry.get() for entry in self.coordenadas_entries]
        if not self.validar_coordenadas(coordenadas):
            messagebox.showerror("Error de validación", "Las coordenadas deben ser valores numéricos.")
            return

        # Procesar la información del formulario
        modelo = "Modelo: " + self.data_file_label.cget("text")

        coordenadas_text = []
        trayectoria_actual = []
        for i, entry in enumerate(self.coordenadas_entries):
            label_text = self.coordenadas_labels[i].cget("text")
            coordenada = f"{label_text.strip(':')} {entry.get()}"
            trayectoria_actual.append(coordenada)
            
            # Cada 3 entradas, agregar el conjunto al resultado final
            if (i + 1) % 3 == 0:
                coordenadas_text.append(" ".join(trayectoria_actual))
                trayectoria_actual = []

        # Puedes realizar las acciones necesarias con la información
        print(modelo, *coordenadas_text)

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