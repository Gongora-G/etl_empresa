### 2025-09-03 - Avance en la interfaz de usuario (dashboard)

- Se corrigió la estructura de la clase principal de la interfaz para evitar errores de ejecución.
- Se agregó un panel de notificaciones/logs recientes en la parte inferior del dashboard, permitiendo visualizar mensajes de estado, advertencias y errores recientes de los procesos ETL.
- El panel de logs utiliza un `QListWidget` para mostrar mensajes simulados, que luego se conectarán a los logs reales del sistema.
- Se mantiene la documentación y registro de cada avance y decisión en el archivo `DOCUMENTACION_DESARROLLO.md`.
# Documentación del Proyecto ETL_EMPRESA

## 1. Descripción General

Este proyecto tiene como objetivo implementar un sistema ETL (Extract, Transform, Load) profesional y escalable para la empresa, permitiendo la integración de datos desde múltiples fuentes (APIs, bases de datos, archivos, etc.), su transformación según reglas de negocio y su carga en un Data Warehouse (SQL Server) y archivos Excel/CSV para análisis y reportes.

---

## 2. Arquitectura General

### Módulos Principales
- **Extracción:** Obtención de datos desde APIs (ej. Zoho Bigin), bases de datos, archivos Excel/CSV, etc.
- **Transformación:** Limpieza, normalización y aplicación de reglas de negocio sobre los datos extraídos.
- **Carga:** Inserción de datos procesados en SQL Server, archivos Excel/CSV y otros destinos.
- **Orquestación:** Programación y control de los flujos ETL, gestión de errores y notificaciones.
- **Interfaz de usuario:** Dashboard visual e intuitivo para monitoreo, configuración y reportes (Streamlit).

### Flujo Básico
1. Configuración de fuentes y destinos.
2. Ejecución de procesos ETL (manual o programada).
3. Registro de logs y manejo de errores.
4. Visualización de resultados y estado de los procesos.

---

## 3. Herramientas y Tecnologías

- **Lenguaje:** Python
- **Frameworks/Librerías:**
  - Extracción: `requests`, `pandas`, `pyodbc`, `openpyxl`
  - Transformación: `pandas`
  - Carga: `pyodbc`, `pandas.to_sql`, `openpyxl`
  - Orquestación: `Apache Airflow` (opcional), `Task Scheduler` (Windows)
  - Interfaz: `PyQt5` (aplicación de escritorio profesional)
- **Base de datos destino:** Microsoft SQL Server
- **Control de versiones:** GitHub
- **Documentación:** README, manual de usuario
- **Pruebas:** Unitarias con `pytest`
- **Logs:** Registro de ejecución y errores
- **Configuración:** Archivos `.env` o `config.py`

---

## 4. Estructura de Carpetas Sugerida

```plaintext
ETL_EMPRESA/
│
├── etl/
│   ├── sources/           # Módulos para cada fuente de datos
│   │   ├── zoho_bigin.py
│   │   ├── sql_server.py
│   │   ├── excel.py
│   │   └── ...            # Otros conectores
│   ├── transforms/        # Módulos de transformación
│   │   ├── normalize.py
│   │   ├── clean.py
│   │   └── ...
│   ├── destinations/      # Módulos para destinos
│   │   ├── sql_server.py
│   │   ├── excel.py
│   │   └── ...
│   ├── orchestrator.py    # Orquestación de procesos ETL
│   ├── config.py
│   └── utils.py
│
├── interface/
│   ├── main_window.py     # Ventana principal PyQt5
│   ├── views/             # Subvistas PyQt5
│   │   ├── source_view.py
│   │   ├── ocr_view.py    # Vista para extracción OCR
│   │   ├── transform_view.py
│   │   ├── destination_view.py
│   │   └── log_view.py
│   └── components/        # Componentes reutilizables PyQt5
│       ├── sidebar.py
│       ├── table.py
│       └── ...
│
├── data/
│   └── ...                # Archivos fuente y resultados
│
├── logs/
│   └── ...                # Logs de ejecución
│
├── tests/
│   └── ...                # Pruebas unitarias
│
├── requirements.txt       # Dependencias Python
│
└── README.md              # Documentación
```

---

## 5. Arquitectura ETL con Data Lake y Data Warehouse

### Data Lake (local)
- Carpeta local `data_lake/` para almacenar datos crudos de todas las fuentes (Zoho Bigin, OCR, SQL Server, Excel, etc.).
- Estructura recomendada:
  ```
  data_lake/
    zoho_bigin/
      contactos_YYYYMMDD.csv
      empresas_YYYYMMDD.csv
      tratos_YYYYMMDD.csv
    ocr/
      facturas_ocr_YYYYMMDD.csv
      contratos_ocr_YYYYMMDD.csv
    sql_server/
      clientes_YYYYMMDD.csv
    excel/
      ventas_YYYYMMDD.csv
    logs/
      extraccion_YYYYMMDD.log
  ```

### Data Warehouse (SQL Server)
- Base de datos local en SQL Server: `DW_Empresa`
- Tablas principales: `Contactos`, `Empresas`, `Tratos`, más tablas específicas según el negocio (ej. `Facturas_OCR`).
- Los datos transformados y limpios se cargan aquí para análisis y reportes.

### Flujo ETL profesional
1. Extracción: Cada fuente tiene su propio extractor y guarda datos crudos en el Data Lake.
2. Transformación: Módulo aparte que lee del Data Lake, procesa y limpia los datos.
3. Carga: Los datos transformados se insertan en el Data Warehouse (SQL Server).
4. Visualización: Dashboards y reportes conectados al Data Warehouse.

### Integración de OCR
- El módulo OCR procesa archivos PDF, imágenes, etc. y guarda los resultados estructurados en `data_lake/ocr/`.
- El proceso ETL puede transformar estos datos y cargarlos en tablas específicas del Data Warehouse.

### Adaptación a múltiples fuentes
- La arquitectura permite agregar nuevas fuentes fácilmente, cada una con su propio módulo de extracción y carpeta en el Data Lake.

---

## 6. Plan de mejoras para el módulo de extracción

1. Exportar datos a Excel/CSV
   - Botón para exportar los datos de la pestaña activa a un archivo Excel o CSV.
2. Filtros y búsqueda rápida en las tablas
   - Campo de búsqueda arriba de cada tabla para filtrar por texto (nombre, empresa, email, etc.).
3. Paginación o carga progresiva
   - Paginación si el número de registros supera cierto umbral (ej. 100).
4. Visualización de detalles al hacer clic
   - Panel lateral o modal con los detalles completos del registro seleccionado.
5. Validación visual de campos obligatorios
   - Resaltar en rojo los campos obligatorios faltantes y mostrar advertencias.
6. Botón para recargar/actualizar los datos
   - Refrescar los datos sin cerrar la ventana.
7. Indicador de progreso/loading
   - Spinner o barra de progreso mientras se realiza la extracción.
8. Logs de extracción y errores accesibles
   - Botón para ver el log de la última extracción y los errores.

---

## 7. Buenas prácticas y recomendaciones
- Mantener los datos crudos en el Data Lake para trazabilidad y auditoría.
- Realizar la transformación en un módulo aparte, nunca en el Data Lake.
- Cargar solo datos limpios y validados al Data Warehouse.
- Documentar cada fuente, transformación y destino en los archivos de documentación.

---

## 8. Recomendaciones

- Mantener documentación actualizada.
- Implementar pruebas unitarias y logs detallados.
- Usar GitHub para control de versiones y colaboración.
- Priorizar la facilidad de uso en la interfaz (Streamlit).
- Diseñar el sistema para que sea extensible y adaptable a nuevas necesidades.

---


## 9. Próximos Pasos
- Implementar lógica de extracción y carga para cada tipo de conexión.
- [10/09/2025] Se integró la extracción real de datos de Zoho Bigin en el módulo de extracción, mostrando los datos en la tabla de la interfaz.
- Mejorar la visualización de logs y errores en la interfaz.
- Agregar más validaciones y ayudas contextuales en el gestor de conexiones.

---

## 10. Guía Paso a Paso para el Desarrollo y Uso del Proyecto

### 1. Inicialización del Proyecto
1. Crea la estructura de carpetas y archivos según el esquema anterior.
2. Inicializa un repositorio Git en la carpeta raíz:
  ```powershell
  git init
  ```
3. Crea un archivo `.gitignore` para excluir archivos temporales y sensibles.

### 2. Configuración del Entorno Python
1. Crea y activa un entorno virtual:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
2. Crea el archivo `requirements.txt` con las dependencias principales:
  - pandas
  - streamlit
  - requests
  - pyodbc
  - openpyxl
  - pytest
  - python-dotenv
  - (agrega otras según necesidad)
3. Instala las dependencias:
  ```powershell
  pip install -r requirements.txt
  ```

### 3. Desarrollo Modular
1. Implementa los conectores en `etl/sources/` para cada fuente de datos (ejemplo: Zoho Bigin, SQL Server, Excel).
2. Implementa los módulos de transformación en `etl/transforms/` (limpieza, normalización, reglas de negocio).
3. Implementa los módulos de carga en `etl/destinations/` (SQL Server, Excel, CSV).
4. Desarrolla el orquestador en `etl/orchestrator.py` para coordinar los procesos ETL.
5. Centraliza la configuración en `etl/config.py` y utilidades en `etl/utils.py`.

### 4. Desarrollo de la Interfaz de Usuario
1. Crea la vista principal en `interface/dashboard.py` usando Streamlit.
2. Desarrolla subvistas en `interface/views/` para cada etapa del proceso (fuentes, transformación, destino, logs).
3. Implementa componentes reutilizables en `interface/components/` (sidebar, tablas, formularios).
4. Integra la interfaz con los módulos ETL para ejecutar procesos y mostrar resultados.

### 5. Pruebas y Calidad
1. Implementa pruebas unitarias en `tests/` usando `pytest`.
2. Verifica la funcionalidad de cada módulo y la integración completa.

### 6. Control de Versiones
1. Realiza commits frecuentes y descriptivos en Git.
2. Sube el repositorio a GitHub para respaldo y colaboración:
  ```powershell
  git remote add origin <URL_REPOSITORIO_GITHUB>
  git push -u origin master
  ```

### 7. Documentación y Manual de Usuario
1. Mantén actualizado el archivo `README.md` con instrucciones de instalación, uso y ejemplos.
2. Documenta cada módulo y función en el código.

### 8. Automatización y Monitoreo
1. Configura la ejecución automática de procesos ETL (puedes usar Task Scheduler de Windows o Airflow si lo requieres).
2. Implementa registro de logs y manejo de errores en los procesos.
3. Agrega visualización de logs y estado en la interfaz.

### 9. Escalabilidad y Mantenimiento
1. Diseña el sistema para agregar nuevas fuentes/destinos fácilmente (solo crear nuevos módulos en las carpetas correspondientes).
2. Mantén la modularidad y buenas prácticas de desarrollo.

---

## 9.1. Relación entre botones de acción rápida y menú lateral

- **Botones de acción rápida (dashboard):**
  - Ejecutar ETL: Lanza el proceso ETL completo usando la configuración actual. No cambia de vista, solo ejecuta y actualiza KPIs/logs.
  - Subir archivo para OCR: Abre un diálogo para seleccionar archivo, ejecuta OCR y muestra el resultado en el dashboard o popup.
  - Exportar resultados: Permite exportar los resultados del último ETL a Excel/CSV. Abre diálogo de guardado, no cambia de vista.

- **Menú lateral:**
  - Cada opción carga una vista diferente en el panel principal:
    - Dashboard: KPIs, botones rápidos y logs.
    - Extracción: Configuración y prueba de fuentes de datos.
    - Transformación: Reglas de limpieza y transformación.
    - Carga: Configuración de destinos y revisión de cargas.
    - OCR: Subida de archivos, resultados y logs OCR.
    - Logs: Exploración de logs históricos.
    - Configuración: Parámetros generales y credenciales.

- **Resumen:**
  - Los botones rápidos ejecutan acciones globales desde el dashboard.
  - El menú lateral permite navegar y gestionar cada etapa del proceso ETL en vistas dedicadas.

---

**Próximo paso:**
- Desarrollar primero los módulos y vistas del menú lateral izquierdo, comenzando por el módulo de Extracción.

---

**Este documento sirve como guía y referencia para el desarrollo completo y profesional del proyecto ETL_EMPRESA.**
