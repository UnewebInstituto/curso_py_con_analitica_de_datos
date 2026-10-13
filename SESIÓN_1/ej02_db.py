import statistics
import psycopg2

# Configuración de la conexión a PostgreSQL
# (Ajusta estos parámetros según los datos de tu servidor local o remoto)
db_config = {
    'dbname': 'db_bm_py_analitica_curso',
    'user': 'postgres',
    'password': '1234567',
    'host': 'localhost',
    'port': '5432',
}

# Listas para almacenar los valores extraídos de la BD
ages = []
experiences = []
salaries = []

try:
  # 1. Conexión a la base de datos PostgreSQL
  conexion = psycopg2.connect(**db_config)
  cursor = conexion.cursor()

  # 2. Consulta SQL para extraer los datos de la tabla salary_data
  consulta = """
        SELECT age, years_of_experience, salary 
        FROM salary_data 
        WHERE age IS NOT NULL 
          AND years_of_experience IS NOT NULL 
          AND salary IS NOT NULL;
    """

  cursor.execute(consulta)
  registros = cursor.fetchall()

  # 3. Recorrer los registros de la base de datos y llenar las listas
  for fila in registros:
    # Como la consulta ya trae el orden exacto, los mapeamos por índice
    age, years_of_experience, salary = fila

    # Conversión y almacenamiento seguro
    try:
      ages.append(float(age))
      experiences.append(float(years_of_experience))
      salaries.append(float(salary))
    except (ValueError, TypeError):
      continue  # Salta filas con datos anómalos

  cursor.close()
  conexion.close()

except Exception as e:
  print(f'Error al conectar o consultar la base de datos: {e}')
  exit()


# 4. Función auxiliar para calcular las métricas estadísticas (la misma de antes)
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

# 6. Imprimir resultados formateados
if stats_age and stats_exp and stats_sal:
  print('--- EDAD (Age) [Desde PostgreSQL] ---')
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