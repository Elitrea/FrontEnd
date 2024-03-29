import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from pyDOE2 import lhs

# Establecer la semilla para reproducibilidad
seed = 42
torch.manual_seed(seed)
np.random.seed(seed)

# Datos de entrenamiento y prueba ficticios
X_train = torch.randn((100, 10))
y_train = torch.randn((100, 1))
X_test = torch.randn((20, 10))
y_test = torch.randn((20, 1))

class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(NeuralNetwork, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size, bias=True)
        self.layer2 = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return x

def train_and_evaluate_neural_network(parameters):
    learning_rate, batch_size, hidden_size = parameters

    model = NeuralNetwork(input_size=X_train.shape[1], hidden_size=int(hidden_size))
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    print(f"\nTraining Neural Network with parameters: Learning Rate={learning_rate}, Batch Size={batch_size}, Hidden Size={hidden_size}\n")

    for epoch in range(10):
        for i in range(0, len(X_train), int(batch_size)):
            batch_X = X_train[i:i+int(batch_size)]
            batch_y = y_train[i:i+int(batch_size)]

            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print(f"Epoch {epoch + 1}, Batch {i // int(batch_size) + 1}, Loss: {loss.item()}")

    with torch.no_grad():
        predictions = model(X_test)
        mse = nn.MSELoss()(predictions, y_test)

    print(f"\nEvaluation on Test Set - MSE: {mse.item()}\n")

    return mse.item()

# Definir los valores de los niveles para cada parámetro
level_values = [[0.001, 0.1], [32, 256], [2, 4]]

# Generar matriz de diseño LHS con valores específicos para los niveles
design_matrix = lhs(3, samples=10, criterion='maximin', iterations=1000)
design_matrix *= (np.array(level_values)[:, 1] - np.array(level_values)[:, 0])
design_matrix += np.array(level_values)[:, 0]

best_performance = float('inf')
best_parameters = None

for parameters in design_matrix:
    performance_metric = train_and_evaluate_neural_network(parameters)

    if performance_metric < best_performance:
        best_performance = performance_metric
        best_parameters = parameters

# Escalar nuevamente para obtener los valores originales
best_parameters_original_values = (best_parameters - np.array(level_values)[:, 0]) / (np.array(level_values)[:, 1] - np.array(level_values)[:, 0])

print("\nMejor combinación de parámetros (Valores originales):", best_parameters_original_values)
print("Mejor métrica de rendimiento (MSE):", best_performance)
