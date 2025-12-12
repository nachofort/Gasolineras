
import streamlit as st
import pandas as pd
import requests
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="Gasolineras",
    layout="wide",
    initial_sidebar_state="expanded",
)

#Función para obtener y limpiar datos (ETL)
@st.cache_data
def cargar_datos(id_ccaa):
    url = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/FiltroCCAA/{id_ccaa}"

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
    }


    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            data = response.json()
            lista_gasolineras = data['ListaEESSPrecio']

            df = pd.DataFrame(lista_gasolineras)

            #LIMPIEZA DE DATOS

            #Convertir Coordenadas
            df['lat'] = df['Latitud'].str.replace(',','.').astype(float)
            df['lon'] = df['Longitud (WGS84)'].str.replace(',','.').astype(float)

            #Convertir precios

            def limpiar_precio(valor):
                if not valor: return None
                return float (valor.replace(',', '.'))

            df['Precio_Gasolina_95'] = df['Precio Gasolina 95 E5'].apply(limpiar_precio)
            df['Precio_Diesel_A'] = df['Precio Gasóleo A'].apply(limpiar_precio)

            return df
        else:
            st.error(f"Error al conectar con la API: {response.status_code}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Excepción: {e}")
        return pd.DataFrame()

#Frontend
def main():
    st.title("Precios de Combustible")
    st.markdown("Datos a tiempo real del **Ministerio para la Transición Ecológica**.")

    #Cargar datos
    df = cargar_datos(13)

    if not df.empty:
        #FILTROS
        st.sidebar.header("Filtros")
        municipios = sorted(df['Municipio'].unique())
        municipio_sel = st.sidebar.multiselect("Filtrar por Municipio", municipios)
        tipo_combustible = st.sidebar.radio("⛽ Tipo de Combustible", ["Gasolina 95", "Diesel A"])
        columna_precio = 'Precio_Gasolina_95' if tipo_combustible == "Gasolina 95" else 'Precio_Diesel_A'

        if municipio_sel:
            df_filtrado = df[df['Municipio'].isin(municipio_sel)]
        else:
            df_filtrado = df

        #Limpiamos datos vacios
        df_filtrado = df_filtrado.dropna(subset=[columna_precio])

        #Metricas
        if not df_filtrado.empty:
            
            p33 = np.percentile(df_filtrado[columna_precio], 33)
            p66 = np.percentile(df_filtrado[columna_precio], 66)
            
            col1, col2, col3 = st.columns(3)
            media_gasolina = df_filtrado['Precio_Gasolina_95'].mean()
            media_diesel = df_filtrado['Precio_Diesel_A'].mean()

            col1.metric("Estaciones encontradas", len(df_filtrado))
            col2.metric("Precio Medio Gasolina 95", f"{media_gasolina:.3f} €")
            col3.metric("Precio Medio Diesel A", f"{media_diesel:.3f} €")

            #MAPA
            st.subheader(f"Mapa de Calor de {tipo_combustible}")

            # Centro del mapa basado en el promedio de coordenadas
            lat_centro = df_filtrado['lat'].mean()
            lon_centro = df_filtrado['lon'].mean()

            m = folium.Map(location=[lat_centro, lon_centro], zoom_start=11)

            marker_cluster = MarkerCluster().add_to(m)

            for _, fila in df_filtrado.iterrows():
                precio = fila[columna_precio]
                nombre = fila['Rótulo']
                direccion = fila['Dirección']

                # Lógica de colores semánticos
                if precio <= p33:
                    color = 'green'
                    icono = 'arrow-down'
                elif precio >= p66:
                    color = 'red'
                    icono = 'arrow-up'
                else:
                    color = 'orange'
                    icono = 'minus'

                # Crear el HTML del popup (lo que sale al pinchar)
                html_popup = f"""
                        <b>{nombre}</b><br>
                        Dirección: {direccion}<br>
                        Precio: <b>{precio} €/L</b>
                        """

                folium.Marker(
                    location=[fila['lat'], fila['lon']],
                    popup=html_popup,
                    icon=folium.Icon(color=color, icon=icono, prefix='fa')
                ).add_to(marker_cluster)

                # Renderizar mapa en Streamlit
                st_folium(m, width=1200, height=500)

        else:
            st.warning("No se han podido cargar los datos.")

    else:
        st.error("No se han podido cargar los datos de la API.")

if __name__ == "__main__":
    main()