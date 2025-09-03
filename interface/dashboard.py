
import streamlit as st

st.set_page_config(page_title="ETL Empresa", layout="wide")

st.title("ETL Empresa - Dashboard Principal")

st.sidebar.title("Menú de Navegación")
menu = st.sidebar.radio("Ir a:", ["Inicio", "Extracción OCR", "Fuentes de Datos", "Transformaciones", "Destinos", "Logs"])

if menu == "Inicio":
	st.header("Bienvenido al sistema ETL de la empresa")
	st.markdown("""
	Este dashboard te permite gestionar y monitorear los procesos ETL:
	- Extraer datos desde diferentes fuentes (APIs, SQL Server, OCR, etc.)
	- Transformar y limpiar la información
	- Cargar los datos en destinos como SQL Server, Excel, CSV
	- Visualizar logs y estado de los procesos
	""")
	st.info("Selecciona una opción en el menú lateral para comenzar.")

# Las demás vistas se irán integrando en los siguientes pasos
