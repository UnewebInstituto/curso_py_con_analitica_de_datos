import csv

# Ruta del archivo CSV de abandono de clientes
archivo_csv = './Bank Customer Churn Prediction.csv'

# Variables contadoras
total_clientes = 0
clientes_retenidos = 0  # Churn = 0
clientes_abandonaron = 0  # Churn = 1

try:
  # 1. Apertura del archivo CSV manejando posibles marcas de orden de bytes (BOM)
  with open(archivo_csv, mode='r', encoding='utf-8', errors='ignore') as archivo:
    content = archivo.read().lstrip('\ufeff')
    lines = content.splitlines()
    lector = csv.reader(lines)

    # 2. Leer la cabecera para identificar dinámicamente el índice de la columna 'churn'
    header = next(lector)
    churn_idx = header.index('churn')

    # 3. Recorrer el archivo fila por fila
    for fila in lector:
      # Validar que la fila tenga suficientes columnas
      if len(fila) <= churn_idx:
        continue

      try:
        # Extraer el valor de la columna churn y convertirlo a entero (0 o 1)
        valor_churn = int(fila[churn_idx].strip())

        total_clientes += 1

        if valor_churn == 0:
          clientes_retenidos += 1
        elif valor_churn == 1:
          clientes_abandonaron += 1

      except ValueError:
        # Salta filas que tengan errores de conversión o datos corruptos
        continue

  # 4. Cálculo de porcentajes
  if total_clientes > 0:
    pct_retenidos = (clientes_retenidos / total_clientes) * 100
    pct_abandonaron = (clientes_abandonaron / total_clientes) * 100

    # 5. Imprimir resultados formateados
    print('--- ANÁLISIS DE FUGA DE CLIENTES (CHURN) ---')
    print(f'Total de clientes analizados: {total_clientes:,}')
    print(
        f'Clientes Retenidos (0): {clientes_retenidos:,} ({pct_retenidos:.2f}%)'
    )
    print(
        f'Clientes que Abandonaron (1): {clientes_abandonaron:,} ({pct_abandonaron:.2f}%)'
    )
  else:
    print('No se encontraron registros válidos para procesar.')

except Exception as e:
  print(f'Ocurrió un error al procesar el archivo CSV: {e}')