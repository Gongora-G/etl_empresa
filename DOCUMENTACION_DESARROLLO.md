# Registro de desarrollo y decisiones

## 2025-09-03

- Se corrigió la estructura e indentación de la clase MainWindow para que todo el contenido esté dentro de un solo método `__init__` y el bloque principal fuera de la clase.
- Se agregó el bloque principal para ejecutar la ventana de la aplicación PyQt5 (`if __name__ == "__main__": ...`).
- Se validó visualmente el dashboard principal, cumpliendo con los estándares de software profesional.
- Se acordó avanzar primero con la vista y elementos visuales del dashboard antes de la funcionalidad.
- Se agregó un panel de notificaciones/logs recientes en la parte inferior del dashboard, con simulación de mensajes de log (INFO, WARNING, ERROR). Este panel se conectará a logs reales en futuras etapas.

# Documentación de Desarrollo ETL_EMPRESA

Este documento servirá para registrar cambios importantes, decisiones, errores encontrados y soluciones durante el desarrollo del proyecto.

## Registro de Cambios

- Fecha: 02/09/2025
- Descripción del cambio: Creación de la estructura base del proyecto ETL_EMPRESA, incluyendo carpetas principales, archivos iniciales y documentación.
- Archivos/módulos afectados: etl/, interface/, data/, logs/, tests/, requirements.txt, README.md, .gitignore, DOCUMENTACION_ETL_EMPRESA.md, DOCUMENTACION_DESARROLLO.md
- Motivo/solución: Establecer una base modular y profesional para el desarrollo del sistema ETL, facilitando la escalabilidad y el mantenimiento.

## Registro de Errores

(Sin registros por el momento)

## Notas y Mejoras

- Fecha: 02/09/2025
- Observaciones: Se recomienda mantener la documentación y los registros de cambios actualizados para facilitar el seguimiento y la colaboración.
- Propuestas de mejora: Agregar plantillas para nuevos módulos y scripts de automatización para facilitar la integración de nuevas fuentes/destinos.
- Fecha: 02/09/2025
- Descripción del cambio: Creación del repositorio remoto en GitHub con el nombre sugerido 'etl_empresa'.
- Archivos/módulos afectados: Repositorio GitHub
- Motivo/solución: Centralizar el control de versiones, facilitar la colaboración y respaldo del proyecto.
- Fecha: 02/09/2025
- Descripción del cambio: Vinculación del repositorio local con GitHub y primer push exitoso al repositorio remoto 'etl_empresa'.
- Archivos/módulos afectados: Repositorio GitHub
- Motivo/solución: Publicar la estructura base del proyecto y habilitar el control de versiones remoto.
- Fecha: 02/09/2025
- Descripción del cambio: Configuración del entorno virtual Python y la instalación de dependencias principales del proyecto.
- Archivos/módulos afectados: venv/, requirements.txt
- Motivo/solución: Preparar el entorno de desarrollo aislado y asegurar las librerías necesarias para el proyecto.

## Comandos ejecutados

1. Creación del entorno virtual:
	```powershell
	python -m venv venv
	```
2. Activación del entorno virtual:
	```powershell
	.\venv\Scripts\activate
	```
3. Instalación de dependencias:
	```powershell
	pip install -r requirements.txt
	```
- Fecha: 02/09/2025
- Descripción del cambio: Creación e integración del módulo OCR en la estructura del proyecto, con enfoque modular para distintos tipos de documentos (cédula, certificación bancaria, desprendible de pago, etc.). Instalación de librerías necesarias (pytesseract, pdfplumber, Pillow).
- Archivos/módulos afectados: etl/ocr/, etl/ocr/extract_ocr.py, requirements.txt
- Motivo/solución: Permitir la extracción profesional y escalable de texto desde imágenes y PDFs, facilitando la integración de nuevos tipos de documentos en el futuro.
- Fecha: 02/09/2025
- Descripción del cambio: Se implementa el menú lateral de navegación en la interfaz principal PyQt5, con espacio para logo, nombre de la empresa y colores corporativos (azul y gris). Se definen las opciones principales del sistema ETL y se deja la estructura lista para agregar los siguientes módulos.
- Archivos/módulos afectados: interface/main_window.py
- Motivo/solución: Mejorar la experiencia de usuario y profesionalismo del software, facilitando la navegación y personalización visual.
- Fecha: 02/09/2025
- Descripción del cambio: Se agrega el panel de indicadores y estadísticas (KPIs) al dashboard principal, mostrando estado de procesos ETL, datos procesados, errores y próximas ejecuciones. Se corrige la estructura y se mejora la presentación visual.
- Archivos/módulos afectados: interface/main_window.py
- Motivo/solución: Proveer información clave y profesional al usuario sobre el estado y desempeño del sistema ETL.
- Fecha: 02/09/2025
- Descripción del cambio: Se corrige la indentación y la estructura del archivo main_window.py, asegurando que todo el contenido esté dentro del método __init__ de la clase MainWindow. El dashboard principal ahora muestra menú lateral, espacio para logo y nombre, panel de bienvenida, resumen y KPIs, con estilo profesional y colores corporativos. Se verifica visualmente el resultado y se valida la experiencia de usuario.
- Archivos/módulos afectados: interface/main_window.py
- Motivo/solución: Evitar errores de indentación y asegurar buenas prácticas en la estructura de clases y layouts en PyQt5. Mejorar la presentación visual y la navegación del software ETL.

## Registro de Errores

- Fecha: 02/09/2025
- Error: IndentationError: unexpected indent en main_window.py. Causa: parte del código estaba fuera del método __init__ de la clase MainWindow. Solución: reubicar todo el contenido dentro del método __init__ y revisar la indentación.
- Fecha: 02/09/2025
- Descripción del cambio: Se realiza el push de los cambios locales al repositorio remoto en GitHub, asegurando que el estado actual del proyecto esté respaldado y disponible para colaboración.
- Comando ejecutado:
	```powershell
	git push
	```

# Registro de corrección de errores críticos en la interfaz PyQt5

## Fecha: 03/09/2025

### Problemas detectados:
- Error: "QWidget: Must construct a QApplication before a QWidget" al ejecutar `main_window.py`.
- Widgets y layouts creados fuera del método `__init__` de la clase `MainWindow`.
- Uso incorrecto de `self` fuera de la clase, generando conflictos de contexto.
- Indentación incorrecta y duplicación de imports dentro de métodos.
- El dashboard no abría la ventana principal por inicialización incorrecta.

### Acciones realizadas:
- Se revisó el archivo línea por línea para identificar widgets y layouts fuera de `__init__`.
- Se movió toda la lógica de creación de widgets y layouts dentro del método `__init__`.
- Se eliminaron líneas fuera de la clase y se aseguraron los imports en la parte superior.
- Se probó la ejecución tras cada corrección hasta que la ventana abrió correctamente.
- Se validó el diseño profesional y modular del dashboard.

### Resultado:
- El dashboard ETL abre correctamente y muestra todos los paneles y botones.
- El código está listo para expandirse con nuevas funcionalidades.

---

#### Comando utilizado para ejecutar:
`python interface/main_window.py`

#### Estado final:
- Exit Code: 0
- Ventana abierta correctamente (ver imagen adjunta en registro de desarrollo)

---

#### Siguiente paso:
Avanzar con integración de módulos y funcionalidades.

# Registro de rediseño profesional del gestor de conexiones y campos personalizados

## Fecha: 03/09/2025

### Cambios y decisiones:
- Se rediseñó el gestor de conexiones para permitir agregar, editar y eliminar campos personalizados visualmente.
- Cada campo ahora permite definir su tipo (Texto, Número, Token/Clave, URL, Otro) para mayor claridad y control.
- Se eliminó la restricción de tipos predefinidos de fuente, permitiendo máxima flexibilidad para cualquier API, base de datos o sistema.
- El usuario puede gestionar credenciales y parámetros desde la interfaz, y la lógica de conexión se implementa en el backend usando estos parámetros.
- Se documentó que los tipos de campo son solo informativos para el usuario y para futuras validaciones o ayudas contextuales.
- Se recomienda consultar la documentación oficial de cada plataforma/API para saber qué campos y tipos se requieren.

### Ventajas de este enfoque:
- Máxima flexibilidad y escalabilidad.
- Experiencia visual profesional y amigable.
- Permite conectar a cualquier fuente, incluso APIs nuevas o personalizadas.
- Facilita la gestión de credenciales y parámetros sin tocar el código.

---

# Registro de mejoras en la gestión y guardado de conexiones

## Fecha: 03/09/2025

### Cambios realizados:
- Se corrigió y validó que todos los cambios en campos y conexiones se guarden correctamente al pulsar 'Guardar conexión'.
- Ahora cualquier modificación en los campos personalizados de una conexión requiere pulsar 'Guardar conexión' para persistir los cambios en el archivo `config.ini`.
- Se documentó el flujo recomendado: crear/editar campos, luego guardar para que los cambios sean efectivos.
- Se recomienda al usuario siempre pulsar 'Guardar conexión' tras cualquier cambio en los campos o valores de una conexión.

### Estado actual:
- El gestor de conexiones es flexible, visual y profesional.
- Los cambios se guardan de forma segura y confiable.

---

**Próximo paso:**
- Integrar la lógica de extracción usando los parámetros definidos y guardados en cada conexión.
