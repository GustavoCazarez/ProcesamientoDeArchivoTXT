"""
PROYECTO: Análisis Exploratorio de Datos Climatológicos - Estación Acatitán
LIBRERÍAS UTILIZADAS: 
- Pandas: Para la manipulación de estructuras de datos tabulares.
- Numpy: Para el manejo de valores nulos y operaciones matemáticas.
"""

import pandas as pd
import numpy as np

def cargar_datos(ruta_archivo):
    """Carga los datos desde un TXT ignorando encabezados y manejando codificación."""
    columnas = ['FECHA', 'PRECIP', 'EVAP', 'TMAX', 'TMIN']
    return pd.read_csv(ruta_archivo, sep=r'\s+', skiprows=19, names=columnas, 
                       na_values='Nulo', engine='python', encoding='latin-1')

def limpiar_clima(df):
    """Realiza la limpieza, conteo de faltantes e imputación por media."""
    
    # 1. Limpieza de Fechas: Convertimos y eliminamos filas de texto basura (guiones)
    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['FECHA'])
    
    # 2. Conteo de faltantes: Se crea columna sumando nulos antes de rellenar
    df['TOTAL_FALTANTES'] = df[['PRECIP', 'EVAP', 'TMAX', 'TMIN']].isnull().sum(axis=1)
    
    # 3. Imputación: Rellenar nulos con la media para mantener la consistencia estadística
    for col in ['PRECIP', 'EVAP', 'TMAX', 'TMIN']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].mean())
        
    return df

def ejecutar_analisis():
    """Función principal que orquesta el proceso."""
    archivo = '25001.txt'
    
    # Paso 1: Carga
    raw_data = cargar_datos(archivo)
    
    # Paso 2: Limpieza y Procesamiento
    df_limpio = limpiar_clima(raw_data)
    
    # Paso 3: Mostrar resultados (Ejemplos)
    print("Muestra de datos procesados (Primeras 5 filas):")
    print(df_limpio.head())
    
    # Paso 4: Exportación
    df_limpio.to_csv('datos_procesados_acatitan.csv', index=False)
    print("\nÉxito: Se ha generado el archivo 'datos_procesados_acatitan.csv'")

if __name__ == "__main__":
    ejecutar_analisis()