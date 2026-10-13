import statistics
import openpyxl

# Ruta del archivo de Excel de entrada
archivo_excel = './Salary_Data_Test.xlsx'

# Listas para almacenar los valores extraídos de Excel
ages = []
experiences = []
salaries = []

try:
  # 1. Cargar el libro de trabajo de Excel
  wb = openpyxl.load_workbook(archivo_excel, data_only=True)
  ws = wb.active  # Selecciona la hoja activa

  # 2. Leer la cabecera (primera fila) para identificar dinámicamente los índices de las columnas
  header = [cell.value for cell in ws[1]]
  age_idx = header.index('Age')
  exp_idx = header.index('Years of Experience')
  sal_idx = header.index('Salary')

  # 3. Recorrer las filas de Excel omitiendo la cabecera (comenzando desde la fila 2)
  for row in ws.iter_rows(min_row=2, values_only=True):
    # Validar que la fila tenga suficientes columnas
    if row is None or len(row) <= max(age_idx, exp_idx, sal_idx):
      continue

    age = row[age_idx]
    experience = row[exp_idx]
    salary = row[sal_idx]

    # Conversión y almacenamiento seguro (filtrando nulos o vacíos)
    try:
      if age is not None and str(age).strip():
        ages.append(float(age))
      if experience is not None and str(experience).strip():
        experiences.append(float(experience))
      if salary is not None and str(salary).strip():
        salaries.append(float(salary))
    except (ValueError, TypeError):
      continue  # Salta filas con datos anómalos o texto corrupto

except Exception as e:
  print(f'Error al leer el archivo de Excel: {e}')
  exit()


# 4. Función auxiliar para calcular las métricas estadísticas (módulo statistics)
def calcular_metricas(datos):
  n = len(datos)
  if n == 0:
    return None
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


# 5. Obtener resultados estadísticos para cada variable
stats_age = calcular_metricas(ages)
stats_exp = calcular_metricas(experiences)
stats_sal = calcular_metricas(salaries)

# 6. Imprimir resultados formateados en consola
if stats_age and stats_exp and stats_sal:
  print('--- EDAD (Age) [Desde Excel] ---')
  print(
      f"Media: {stats_age['media']:.2f} | Mediana: {stats_age['mediana']:.2f}"
      f" | Mín: {stats_age['min']:.2f} | Máx: {stats_age['max']:.2f} |"
      f" Desv.Std: {stats_age['std']:.2f}"
  )

  print('\n--- AÑOS DE EXPERIENCIA (Years of Experience) ---')
  print(
      f"Media: {stats_exp['media']:.2f} | Mediana: {stats_exp['mediana']:.2f}"
      f" | Mín: {stats_exp['min']:.2f} | Máx: {stats_exp['max']:.2f} |"
      f" Desv.Std: {stats_exp['std']:.2f}"
  )

  print('\n--- SALARIO (Salary) ---')
  print(
      f"Media: ${stats_sal['media']:,.2f} | Mediana:"
      f" ${stats_sal['mediana']:,.2f} | Mín: ${stats_sal['min']:,.2f} | Máx:"
      f" ${stats_sal['max']:,.2f} | Desv.Std: ${stats_sal['std']:,.2f}"
  )
else:
  print('No se pudieron calcular las métricas (listas vacías o sin datos).')