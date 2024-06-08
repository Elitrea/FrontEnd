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
        self.title('Formulario Entrenamiento')
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
        self.labelTitulo = tk.Label(self.barra_superior, text="Entrenamiento")
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
        
    def toggle_validation():
        if validation_check.get() == 1:
            val_size_entry.config(state="normal")
        else:
            val_size_entry.delete(0, tk.END)
            val_size_entry.config(state="disabled")
            
    def principal(self):
        # Crear un frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Lista de descripciones para los botones
        descripciones = [
            "Red neuronal con capas densas simple",
            "Red neuronal con capas densas y retroalimentación entre capas",
            "Red neuronal convolucional CNN"
        ]

        # Crear los botones y etiquetas de descripción correspondientes
        for i, btn_text in enumerate(["MLP Básica", "MLP FeedFowarding", "CNN"]):
            btn = tk.Button(main_frame, text=btn_text, font=("Roboto", 12, "bold"), bg="#800040", fg="white", command=self.accion_btn1 if i == 0 else self.accion_btn2 if i == 1 else self.accion_btn3)
            btn.grid(row=0, column=i, padx=50, pady=30, sticky="nsew")
            
            # Etiqueta de descripción
            descripcion_label = tk.Label(main_frame, text=descripciones[i], font=("Helvetica", 12), wraplength=200, justify="center")
            descripcion_label.grid(row=1, column=i, padx=50, pady=30, sticky="nsew")

        # Configurar el sistema de pesos para que los elementos se expandan y se centren
        main_frame.grid_rowconfigure((0, 1, 2), weight=1)
        main_frame.grid_columnconfigure((0, 1), weight=1)



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

        if opcion_seleccionada == "Sí":
            self.porcentaje_entry.config(state="normal")
        else:
            self.porcentaje_entry.delete(0, tk.END)
            self.porcentaje_entry.config(state="disabled")

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