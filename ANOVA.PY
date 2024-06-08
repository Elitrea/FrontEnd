import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
import statsmodels.api as sm

# Leer el archivo CSV
df = pd.read_csv('datosTest.csv')

# Calcular las medias y desviaciones estándar de los entrenamientos
df['Media'] = df[['Entrenamiento1', 'Entrenamiento2', 'Entrenamiento3', 'Entrenamiento4']].mean(axis=1)
df['DesviacionEstandar'] = df[['Entrenamiento1', 'Entrenamiento2', 'Entrenamiento3', 'Entrenamiento4']].std(axis=1)

# Ajustar el modelo ANOVA
model = ols('Media ~ Parametro1 + Parametro2 + Parametro3 + Parametro4', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# Mostrar la tabla ANOVA
print(anova_table)

# Graficar las medias
plt.figure(figsize=(12, 6))
sns.barplot(x='Parametro1', y='Media', hue='Parametro2', data=df)
plt.title('Media de los Resultados de los Entrenamientos')
plt.show()

# Graficar las desviaciones estándar
plt.figure(figsize=(12, 6))
sns.barplot(x='Parametro1', y='DesviacionEstandar', hue='Parametro2', data=df)
plt.title('Desviación Estándar de los Resultados de los Entrenamientos')
plt.show()

# Matriz de correlación
corr = df[['Parametro1', 'Parametro2', 'Parametro3', 'Parametro4', 'Media']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Matriz de Correlación de los Parámetros y la Media')
plt.show()

# Encontrar el índice del entrenamiento con la media más alta
indice_mejor_entrenamiento = df['Media'].idxmax()

# Obtener los nombres de los entrenamientos
mejores_entrenamientos = df.loc[indice_mejor_entrenamiento, ['Entrenamiento1', 'Entrenamiento2', 'Entrenamiento3', 'Entrenamiento4']]

print("Los mejores entrenamientos fueron:")
print(mejores_entrenamientos)

# Encontrar el índice del entrenamiento con la media más alta
indice_mejor_entrenamiento = df['Media'].idxmax()

# Obtener los valores de los parámetros para el mejor entrenamiento
valores_mejores_parametros = df.loc[indice_mejor_entrenamiento, ['Parametro1', 'Parametro2', 'Parametro3', 'Parametro4']]

print("Los valores de los parámetros que corresponden al mejor entrenamiento fueron:")
print(valores_mejores_parametros)
