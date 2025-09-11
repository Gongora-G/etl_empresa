### Visualización profesional de parámetros de conexión

Por motivos de seguridad y profesionalismo, los valores completos de parámetros sensibles (token, client_secret, refresh_token) se ocultan en la interfaz. Solo se muestran los primeros y últimos caracteres, con asteriscos en el medio. El usuario puede revelar el valor completo bajo demanda si es necesario.

Esta práctica protege la información confidencial y mejora la experiencia del usuario, evitando exposiciones accidentales de credenciales.

Ejemplo visual:
- Token: 1000.c689...f0c499   (oculto)
- Client Secret: 1ec66...9887e5b   (oculto)

Los parámetros no sensibles se muestran parcialmente si son largos, para mantener la interfaz limpia y profesional.
# Documentación de integración Zoho Bigin

## Proceso para obtener credenciales válidas

1. **Registro de aplicación en Zoho API Console**
	- Tipo: Aplicaciones basadas en servidor
	- Nombre: ETL Empresa
	- URL de inicio/redirección: https://localhost
	- Resultado: Se obtiene `client_id` y `client_secret`.

2. **Generación del código de autorización**
	- URL construida:
	  `https://accounts.zoho.com/oauth/v2/auth?scope=ZohoBigin.modules.ALL&client_id=CLIENT_ID&response_type=code&access_type=offline&redirect_uri=https://localhost`
	- Se autoriza la app y se copia el parámetro `code` de la URL de redirección.

3. **Intercambio del código por tokens en Postman**
	- POST a `https://accounts.zoho.com/oauth/v2/token` con body x-www-form-urlencoded:
	  - grant_type: authorization_code
	  - client_id: (el real)
	  - client_secret: (el real)
	  - redirect_uri: https://localhost
	  - code: (el obtenido)
	- Resultado: Se obtiene `access_token` y `refresh_token`.

## Errores y soluciones
- **invalid_code**: El código expiró o ya fue usado. Solución: generar uno nuevo y usarlo de inmediato.
- **invalid_client**: El client_id o client_secret no son válidos. Solución: revisar credenciales en Zoho API Console.
- **invalid_url_pattern (404)**: El endpoint usado no existe. Solución: usar `/bigin/v1/users` para probar autenticación.

## Guardado y refresco automático de token
- Los valores se guardan en `config.ini`.
- El sistema refresca el token automáticamente si expira, usando el `refresh_token`, `client_id` y `client_secret`.
- Si el refresco falla, se muestra el error detallado en la interfaz.

## Ejemplo de sección válida en config.ini
```ini
[zoho_bigin]
type = zoho_bigin
token = 1000.d880f1f153cf3fb742e83fdd62c4988e.976a626a595ec268ad5b47a6e5a03a0f
client_id = 1000.HK0XC64VRVBC5F98TUIQ0H53YSBIUD
client_secret = 1ec66e92e44790a324a1d5121c43ce7903e9887e5b
refresh_token = 1000.f3700dd8f6391d3095f45685c1bc6433.3e4988b4cdc8d984659f4c3b377fe447
```

---

**Todo el proceso y los errores fueron documentados para futuras referencias y soporte.**
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


# Registro de rediseño profesional de la vista de extracción y seguridad de parámetros

## Fecha: 04/09/2025

# Registro de integración de extracción real de Zoho Bigin

## Fecha: 10/09/2025

### Cambios realizados:
- Se integró la función `obtener_datos_zoho_bigin` en la vista de extracción para mostrar los datos reales de Zoho Bigin en la tabla.
- Ahora, al pulsar el botón "Extraer datos" con la conexión Zoho Bigin seleccionada, se consulta la API y se muestran los registros reales en la interfaz.
- Se documentó el proceso y se mantiene la simulación para otros tipos de conexión.

### Estado actual:
- El módulo de extracción permite visualizar datos reales de Zoho Bigin directamente en la interfaz.

### Cambios y decisiones:
- El combo de la vista de extracción ahora muestra las conexiones guardadas, no los tipos de fuente.
- Al seleccionar una conexión, se muestra un resumen visual de todos los campos y valores definidos, incluyendo los sensibles.
- Los campos sensibles (token, client_secret, refresh_token, password) se ocultan por defecto y pueden mostrarse/ocultarse todos con un solo botón para mayor seguridad y comodidad.
- Se eliminó el campo de parámetro/conexión, ya que toda la información se gestiona en el gestor de conexiones.
- Se agregó un botón "Probar conexión" que valida la conexión real para SQL Server y Zoho Bigin. En Zoho, si el token expira, se refresca automáticamente y se actualiza el config.ini.
- Se agregó un botón "Extraer datos" para ejecutar la lógica de extracción usando los parámetros definidos.
- El gestor de conexiones es completamente flexible: permite agregar, editar y eliminar cualquier campo, con tipo informativo.
- Al crear, editar o eliminar conexiones, la interfaz se actualiza automáticamente sin reiniciar la app.
- Se documentó el flujo recomendado: siempre guardar los cambios y probar la conexión antes de extraer datos.
- Se recomienda nunca compartir el archivo config.ini sin anonimizar los valores sensibles.

### Estado actual:
- La experiencia es interactiva, profesional y segura.
- El backend está listo para implementar la lógica real de extracción y carga para cada tipo de fuente/API.

---

**Próximo paso:**
- Implementar la lógica real de extracción y carga para cada tipo de fuente/API.
- Mejorar la visualización de logs y errores en la interfaz.
- Agregar más validaciones y ayudas contextuales en el gestor de conexiones.
- Documentar ejemplos y recomendaciones para cada tipo de conexión.
