import json
import requests
import pandas as pd

from datetime import datetime

def obtener_gasolineras(id_ccaa):

    url= f'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroCCAA/{id_ccaa}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response_dict = json.loads(response.text)

        if response.status_code != 200:
            print(f"Error al conectar: Código {response.status_code}")
            return pd.DataFrame()

        print(f'Respuesta obtenida en {response.elapsed.total_seconds()} segundos.')

        gasolineras = []

        for estacion in response_dict['ListaEESSPrecio']:
            gasolineras.append({
                # INFORMACIÓN BÁSICA
                'rotulo': estacion.get['Rótulo', 'Desconocido'],
                'direccion': estacion.get['Dirección', ''],
                'municipio': estacion.get['Municipio', ''],
                'horario': estacion.get['Horario',''],

                # COORDENADAS
                'latitud': estacion.get['Latitud', ''],
                'longitud': estacion.get['Longitud (WGS84)', ''],

                # PRECIOS
                'precio_95': estacion.get['Precio Gasolina 95 E5', None],
                'precio_diesel': estacion.get['Precio Gasóleo A', None],

                # OTROS DATOS ÚTILES
                'id_estacion': estacion.get['IDEESS', ''],

            })
        df = pd.DataFrame(gasolineras)

        df['latitud'] = df['latitud'].str.replace(',', '.').astype(float)
        df['longitud'] = df['longitud'].str.replace(',', '.').astype(float)

        # Función para limpiar precios (convertir "1,540" a 1.540)
        def limpiar_numero(x):
            if not x: return None
            return float(str(x).replace(',', '.'))

        df['precio_95'] = df['precio_95'].apply(limpiar_numero)
        df['precio_diesel'] = df['precio_diesel'].apply(limpiar_numero)

        return df

    except Exception as err:
        print(f'El problema ha ocurrido un error: {err}')

def main ():
    print('-' * 50)
    print('⛽ BUSCADOR DE GASOLINERAS LOCAL')
    print('-' * 50)
    print('IDs de Comunidades Autónomas:')
    print('01: Andalucía | 09: Cataluña | 10: Valencia | 13: Madrid')
    print('12: Galicia   | 07: Castilla y León | ...')
    print('-' * 50)

    user_input = input(' Introduce el ID de la Comunidad Autónoma')

    df_resultado = obtener_gasolineras(user_input)

    if not df_resultado.empty:

        print(df_resultado.head(5))

        df_resultado.to_csv(f'gasolineras_ccaa_{user_input}.csv', index=False)
        print(f'Archivo guardado como gasolineras_cccaa_{user_input}.csv')
    else:
        print('No se encontraron datos.')

if __name__ == '__main__':
    main()

