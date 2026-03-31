"""
Procesamiento de 
archivo Txt 
"""

import pandas as pd
import numpy as np

def cargar_datos(ruta_archivo):
    """carga los datos desde un TXT ignorando encabezados y manejando codificación."""
    columnas = ['FECHA', 'PRECIP', 'EVAP', 'TMAX', 'TMIN']
    return pd.read_csv(ruta_archivo, sep=r'\s+', skiprows=19, names=columnas, 
                       na_values='Nulo', engine='python', encoding='latin-1')

def limpiar_clima(df):
    """realiza la limpieza"""
    
    #limpieza de Fechas
    df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['FECHA'])
    
    # se crea columna sumando nulos antes de rellenar
    df['TOTAL_FALTANTES'] = df[['PRECIP', 'EVAP', 'TMAX', 'TMIN']].isnull().sum(axis=1)
    
    # rellenar nulos con la media para mantener la consistencia estadística
    for col in ['PRECIP', 'EVAP', 'TMAX', 'TMIN']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(df[col].mean())
        
    return df

def ejecutar_analisis():
    """función principal"""
    archivo = '25001.txt'
    
    #Carga
    raw_data = cargar_datos(archivo)
    
    #Limpieza y Procesamiento
    df_limpio = limpiar_clima(raw_data)
    
    #mostrar resultados
    print("muestra de datos procesados (Primeras 5 filas):")
    print(df_limpio.head())
    
    #Exportación
    df_limpio.to_csv('datos_procesados_acatitan.csv', index=False)
    print("\nexito: Se ha generado el archivo 'datos_procesados_acatitan.csv'")

if __name__ == "__main__":
    ejecutar_analisis()