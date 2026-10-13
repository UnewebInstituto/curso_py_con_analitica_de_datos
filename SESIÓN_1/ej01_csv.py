import csv
import statistics

# Listas para almacenar los valores de cada columna
ages = []
experiences = []
salaries = []
# Ruta del archivo CSV
archivo_csv = "./Salary_Data_Test.csv"

# Abrir el archivo CSV manejando posibles marcas de orden de bytes (BOM)
with open(archivo_csv, mode='r', encoding='utf-8', errors='ignore') as archivo:
  content = archivo.read().lstrip('\ufeff')
  lines = content.splitlines()
  lector = csv.reader(lines)

  # Leer la cabecera para identificar los índices de las columnas
  header = next(lector)
  age_idx = header.index('Age')
  exp_idx = header.index('Years of Experience')
  sal_idx = header.index('Salary')

  # Recorrer el archivo fila por fila y extraer los datos numéricos
  for fila in lector:
    if len(fila) <= max(age_idx, exp_idx, sal_idx):
      continue
    try:
      if fila[age_idx].strip():
        ages.append(float(fila[age_idx]))
      if fila[exp_idx].strip():
        experiences.append(float(fila[exp_idx]))
      if fila[sal_idx].strip():
        salaries.append(float(fila[sal_idx]))
    except ValueError:
      continue  # Salta filas que tengan errores de conversión


# Función auxiliar para calcular las métricas estadísticas requeridas
def calcular_metricas(datos):
  n = len(datos)
  media = sum(datos) / n
  mediana = statistics.median(datos)
  minimo = min(datos)
  maximo = max(datos)
  desv_std = statistics.stdev(datos) if n > 1 else 0
  return {
      'media': media,
      'mediana': mediana,
      'min': minimo,
      'max': maximo,
      'std': desv_std,
  }


# Obtener resultados para cada variable
stats_age = calcular_metricas(ages)
stats_exp = calcular_metricas(experiences)
stats_sal = calcular_metricas(salaries)

# Imprimir resultados formateados
print('--- EDAD (Age) ---')
print(
    f"Media: {stats_age['media']:.2f} | Mediana: {stats_age['mediana']:.2f}"
    f" | Mín: {stats_age['min']:.2f} | Máx: {stats_age['max']:.2f} | Desv.Std:"
    f" {stats_age['std']:.2f}"
)

print('\n--- AÑOS DE EXPERIENCIA (Years of Experience) ---')
print(
    f"Media: {stats_exp['media']:.2f} | Mediana: {stats_exp['mediana']:.2f}"
    f" | Mín: {stats_exp['min']:.2f} | Máx: {stats_exp['max']:.2f} | Desv.Std:"
    f" {stats_exp['std']:.2f}"
)

print('\n--- SALARIO (Salary) ---')
print(
    f"Media: ${stats_sal['media']:,.2f} | Mediana:"
    f" ${stats_sal['mediana']:,.2f} | Mín: ${stats_sal['min']:,.2f} | Máx:"
    f" ${stats_sal['max']:,.2f} | Desv.Std: ${stats_sal['std']:,.2f}"
)
