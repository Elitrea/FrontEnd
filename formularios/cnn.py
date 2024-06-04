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

        # Entrenar el modelo con datos de entrenamiento y validación
        history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_val, y_val))

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
