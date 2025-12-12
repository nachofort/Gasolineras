# ⛽ Visualizador de Precios de Gasolineras (WIP)

Este proyecto consulta datos abiertos del Ministerio para visualizar y comparar los precios de los carburantes en tiempo real. El repositorio contiene dos versiones de la aplicación: una versión desplegada en la nube y una versión local actualmente en desarrollo.

> ⚠️ **Estado del Proyecto:** En Desarrollo (Work In Progress)

## 📂 Estructura del Proyecto

### ☁️ 1. Versión Cloud (`app_cloud.py`)
Esta es la versión desplegada para acceso web público.
- **Enlace al sitio:** [PON_AQUI_TU_LINK_DE_STREAMLIT_O_RENDER]
- **Estado:** Funcional pero inestable.
- **🔴 Nota sobre la API:** Actualmente, la API del gobierno (`sedeaplicaciones.minetur.gob.es`) presenta intermitencias y problemas con el certificado SSL. Es posible que la versión web falle ocasionalmente al intentar obtener los datos en tiempo real debido a estas restricciones externas.

### 💻 2. Versión Local (`app_local.py`)
Esta es la versión de desarrollo donde se están implementando mejoras y soluciones a los problemas de conexión.
- **Estado:** 🚧 En construcción.
- **Objetivo:** Crear una versión más robusta que maneje mejor las excepciones, guarde históricos en local y permita un filtrado más avanzado sin depender tanto de la estabilidad inmediata de la API externa.

## 🛠️ Tecnologías

* **Lenguaje:** Python 3.14
* **Librerías clave:** `pandas`, `requests`, `urllib3`
* **Fuente de datos:** API Geoportal Gasolineras (Ministerio para la Transición Ecológica).

## 🚀 Cómo ejecutar la versión local (En construcción)

1. Clonar el repositorio.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt