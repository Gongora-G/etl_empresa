from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from .connection_manager import ConnectionManager
import configparser
from PyQt5.QtWidgets import QToolButton, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyle

class ExtractionView(QWidget):
    # Diccionario de mapeo para mostrar solo los campos relevantes de Tratos
    TRATOS_MAP = {
        "id": "ID Trato",
        "Deal_Name": "Nombre Trato",
        "Account_Name": "Empresa",
        "Contact_Name": "Contacto",
        "Pagaduria": "Pagaduría",
        "Compra_cartera": "Compra cartera",
        "Amount": "Valor",
        "Stage": "Estado",
        "Description": "Descripción",
        "Labels": "Etiquetas",
        "Created_Time": "Fecha de creación",
        "Last_Modified_Time": "Última modificación",
        "Plazo_solicitado": "Plazo solicitado",
        "Tipo": "Tipo"
    }
    def mostrar_gestor_conexiones(self):
        dlg = ConnectionManager(self)
        dlg.setWindowModality(Qt.ApplicationModal)
        dlg.setMinimumWidth(500)
        dlg.exec_()
    def __init__(self, connection_manager, parent=None):
        super().__init__(parent)
        self.connection_manager = connection_manager
        self.sensitive_states = {}  # Estado de mostrar/ocultar por parámetro
        layout = QVBoxLayout()

        title = QLabel("Extracción de Datos")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e3c78;")
        layout.addWidget(title)

        desc = QLabel("Selecciona una conexión guardada para extraer datos. Puedes probar la conexión antes de extraer.")
        desc.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(desc)

        # Combo de conexiones guardadas
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")  # Asegúrate de que la ruta del archivo de configuración sea correcta
        self.conexion_combo = QComboBox()
        self.conexion_combo.addItems(self.config.sections())
        layout.addWidget(QLabel("Conexión:"))
        layout.addWidget(self.conexion_combo)
        self.conexion_combo.currentTextChanged.connect(self.mostrar_resumen_conexion)

        # Resumen de parámetros de conexión (arriba, como antes)
        self.sensibles_mostrados = False
        self.resumen_label = QLabel()
        self.resumen_label.setStyleSheet("font-size: 12px; color: #1e3c78; background: #f5f5f5; border-radius: 8px; padding: 8px;")
        layout.addWidget(self.resumen_label)
        # Botón para mostrar/ocultar todos los sensibles
        self.btn_toggle_sensibles = QPushButton("Mostrar sensibles")
        self.btn_toggle_sensibles.setFixedWidth(150)
        self.btn_toggle_sensibles.setStyleSheet("background-color: #e3eafc; color: #1e3c78; font-size: 12px; border-radius: 8px;")
        self.btn_toggle_sensibles.clicked.connect(self.toggle_sensibles)
        layout.addWidget(self.btn_toggle_sensibles)

        # Botones en la misma línea
        botones_layout = QHBoxLayout()
        self.btn_probar = QPushButton("Probar conexión")
        self.btn_probar.setStyleSheet("background-color: #1e3c78; color: white; font-size: 15px; padding: 8px 20px; border-radius: 8px;")
        self.btn_probar.setFixedWidth(180)
        botones_layout.addWidget(self.btn_probar)
        self.btn_probar.clicked.connect(self.probar_conexion)

        self.btn_extraer = QPushButton("Extraer datos")
        self.btn_extraer.setStyleSheet("background-color: #1e3c78; color: white; font-size: 15px; padding: 8px 40px; border-radius: 8px;")
        self.btn_extraer.setMinimumWidth(320)
        botones_layout.addWidget(self.btn_extraer, 2)
        self.btn_extraer.clicked.connect(self.extraer_datos)

        # Botón para actualizar/recargar los datos
        self.btn_actualizar = QPushButton("Actualizar datos")
        self.btn_actualizar.setStyleSheet("""
            QPushButton {
                background-color: #1e3c78;
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #274b99;
            }
            QPushButton:pressed {
                background-color: #162447;
            }
        """)
        self.btn_actualizar.setFixedWidth(180)
        self.btn_actualizar.clicked.connect(self.actualizar_datos)
        botones_layout.addWidget(self.btn_actualizar)

        layout.addLayout(botones_layout)

        # Botón para exportar la pestaña activa
        self.btn_exportar = QPushButton("Exportar a Excel/CSV")
        self.btn_exportar.setStyleSheet("background-color: #e3eafc; color: #1e3c78; font-size: 13px; border-radius: 8px;")
        self.btn_exportar.setFixedWidth(180)
        self.btn_exportar.clicked.connect(self.exportar_tabla_actual)
        layout.addWidget(self.btn_exportar)

        # Barra de filtros y búsqueda (inicialmente oculta)
        self.filtros_widget = QWidget()
        self.filtros_layout = QHBoxLayout()
        self.filtros_widget.setLayout(self.filtros_layout)
        self.filtros_widget.hide()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar en la pestaña actual...")
        self.search_box.setStyleSheet("font-size: 13px; padding: 6px; border-radius: 8px; background: #f5f5f5; color: #1e3c78;")
        self.search_box.textChanged.connect(self.filtrar_tabla_general)
        self.filtros_layout.addWidget(self.search_box)
        self.combo_columnas = QComboBox()
        self.combo_columnas.setMinimumWidth(150)
        self.combo_columnas.setStyleSheet("font-size: 13px; padding: 6px; border-radius: 8px; background: #e3eafc; color: #1e3c78;")
        self.combo_columnas.currentIndexChanged.connect(self.limpiar_filtro_columna)
        self.filtros_layout.addWidget(self.combo_columnas)
        self.input_filtro_columna = QLineEdit()
        self.input_filtro_columna.setPlaceholderText("Valor a filtrar...")
        self.input_filtro_columna.setStyleSheet("font-size: 13px; padding: 6px; border-radius: 8px; background: #f5f5f5; color: #1e3c78;")
        self.filtros_layout.addWidget(self.input_filtro_columna)
        self.btn_filtrar_columna = QPushButton("Filtrar")
        self.btn_filtrar_columna.setStyleSheet("""
            QPushButton {
                background-color: #1e3c78;
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #274b99;
            }
            QPushButton:pressed {
                background-color: #162447;
            }
        """)
        self.btn_filtrar_columna.setFixedWidth(110)
        self.btn_filtrar_columna.clicked.connect(self.filtrar_tabla_columna)
        self.filtros_layout.addWidget(self.btn_filtrar_columna)
        layout.addWidget(self.filtros_widget)

        # Layout principal vertical
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)
        # Bloque superior fijo (información y botones)
        main_layout.addLayout(layout)
        # Bloque central: tabla con pestañas
        self.tabs = QTabWidget()
        self.tab_tables = {}
        for modulo in ["Tratos", "Contactos", "Empresas"]:
            table = QTableWidget()
            table.setVisible(False)
            self.tab_tables[modulo] = table
            self.tabs.addTab(table, modulo)
        self.tabs.setVisible(False)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.tabs, stretch=1)
        # Bloque inferior: botón alineado a la derecha
        bottom_btn_layout = QHBoxLayout()
        bottom_btn_layout.addStretch()
        self.btn_gestionar_conexiones = QPushButton("Gestionar conexiones")
        self.btn_gestionar_conexiones.setStyleSheet("background-color: #1e3c78; color: white; font-size: 14px; padding: 6px 18px; border-radius: 8px;")
        self.btn_gestionar_conexiones.setFixedWidth(170)
        self.btn_gestionar_conexiones.clicked.connect(self.mostrar_gestor_conexiones)
        bottom_btn_layout.addWidget(self.btn_gestionar_conexiones)
        main_layout.addLayout(bottom_btn_layout)
        self.setLayout(main_layout)


        # Eliminar barra de paginación y variables relacionadas

        # Mostrar resumen inicial
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])
        else:
            self.resumen_label.setText("<i>No hay conexiones configuradas. Usa 'Gestionar conexiones' para crear una.</i>")

        # Panel lateral para detalles del registro seleccionado
        self.panel_detalle = QWidget()
        self.panel_detalle.setFixedWidth(350)
        self.panel_detalle.setStyleSheet("background: #f5f5f5; border-left: 2px solid #e3eafc;")
        self.panel_detalle_layout = QVBoxLayout()
        self.panel_detalle.setLayout(self.panel_detalle_layout)
        self.panel_detalle.hide()
        main_layout.addWidget(self.panel_detalle)

        # Botón para exportar y actualizar (inicialmente ocultos)
        self.btn_exportar.hide()
        self.btn_actualizar.hide()

    def mostrar_resumen_conexion(self, nombre):
        # Muestra los parámetros de conexión en un solo label, con opción de mostrar/ocultar sensibles
        if nombre in self.config:
            params = self.config[nombre]
            resumen = "<b>Parámetros de conexión:</b><br>"
            for key, value in params.items():
                if key.lower() in ["token", "client_secret", "refresh_token", "password"]:
                    if self.sensibles_mostrados:
                        display_value = value
                    else:
                        display_value = value[:6] + "..." + value[-6:] if len(value) > 10 else "******"
                    resumen += f"<b>{key.replace('_', ' ').title()}</b>: {display_value} <br>"
                else:
                    display_value = value[:6] + "..." + value[-6:] if len(value) > 12 else value
                    resumen += f"<b>{key.replace('_', ' ').title()}</b>: {display_value}<br>"
            self.resumen_label.setText(resumen)
        else:
            self.resumen_label.setText("")

    def toggle_sensibles(self):
        self.sensibles_mostrados = not self.sensibles_mostrados
        nombre = self.conexion_combo.currentText()
        self.mostrar_resumen_conexion(nombre)
        if self.sensibles_mostrados:
            self.btn_toggle_sensibles.setText("Ocultar sensibles")
        else:
            self.btn_toggle_sensibles.setText("Mostrar sensibles")

    def probar_conexion(self):
        import pyodbc
        import requests
        nombre = self.conexion_combo.currentText()
        params = self.config[nombre] if nombre in self.config else {}
        tipo = nombre.lower()
        # SQL Server
        if tipo == "sql_server":
            server = params.get("server", "")
            database = params.get("database", "")
            user = params.get("user", "")
            password = params.get("password", "")
            if not server or not database or not user or not password:
                QMessageBox.warning(self, "Error", "Faltan parámetros para la conexión SQL Server.")
                return
            conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
            try:
                conn = pyodbc.connect(conn_str, timeout=3)
                conn.close()
                QMessageBox.information(self, "Prueba de conexión", f"Conexión a SQL Server '{nombre}' exitosa.")
            except Exception as e:
                QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar: {str(e)}")
        # Zoho Bigin
        elif tipo == "zoho_bigin":
            token = params.get("token", "")
            client_id = params.get("client_id", "")
            client_secret = params.get("client_secret", "")
            refresh_token = params.get("refresh_token", "")
            if not token:
                QMessageBox.warning(self, "Error", "Falta el token para la conexión Zoho Bigin.")
                return
            url = "https://www.zohoapis.com/bigin/v1/users"
            headers = {
                "Authorization": f"Zoho-oauthtoken {token}",
                "Content-Type": "application/json"
            }
            try:
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code == 200:
                    QMessageBox.information(self, "Prueba de conexión", f"Conexión a Zoho Bigin '{nombre}' exitosa.")
                elif response.status_code == 401:
                    # Intentar refrescar el token automáticamente
                    refresh_url = "https://accounts.zoho.com/oauth/v2/token"
                    data = {
                        "refresh_token": refresh_token,
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "grant_type": "refresh_token"
                    }
                    resp = requests.post(refresh_url, data=data)
                    if resp.status_code == 200:
                        new_token = resp.json().get("access_token")
                        if new_token:
                            # Actualizar config.ini
                            import configparser
                            config = configparser.ConfigParser()
                            config.read("config.ini")
                            config[nombre]["token"] = new_token
                            with open("config.ini", "w") as f:
                                config.write(f)
                            # Reintentar conexión con nuevo token
                            headers["Authorization"] = f"Zoho-oauthtoken {new_token}"
                            retry = requests.get(url, headers=headers, timeout=5)
                            if retry.status_code == 200:
                                QMessageBox.information(self, "Prueba de conexión", f"Conexión a Zoho Bigin '{nombre}' exitosa tras refrescar token.")
                            else:
                                QMessageBox.critical(self, "Error de conexión", f"Token renovado pero la conexión falló: {retry.status_code}\n{retry.text}")
                        else:
                            QMessageBox.critical(self, "Error de conexión", f"No se recibió access_token al renovar: {resp.text}")
                    else:
                        QMessageBox.critical(self, "Error de conexión", f"Error al renovar token: {resp.status_code}\n{resp.text}")
                else:
                    QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar: {response.status_code}\n{response.text}")
            except Exception as e:
                QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar: {str(e)}")
        else:
            QMessageBox.information(self, "Prueba de conexión", "Solo está implementada la prueba para SQL Server y Zoho Bigin.")

    def extraer_datos(self):
        nombre = self.conexion_combo.currentText()
        params = self.config[nombre] if nombre in self.config else {}
        tipo = nombre.lower()
        if tipo == "zoho_bigin":
            try:
                import sys, os, traceback
                proyecto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
                if proyecto_root not in sys.path:
                    sys.path.insert(0, proyecto_root)
                from etl.sources.zoho_bigin import obtener_datos_zoho_bigin
                token = params.get("token", "")
                if not token:
                    QMessageBox.warning(self, "Error", "No se encontró el token para Zoho Bigin.")
                    return
                resultados = obtener_datos_zoho_bigin(token)
            except Exception as e:
                error_trace = traceback.format_exc()
                QMessageBox.critical(self, "Error detallado de importación", f"Error al extraer datos de Zoho Bigin:\n{str(e)}\n\nTraceback:\n{error_trace}")
                return
            # Unir todos los módulos en una sola lista para mostrar en la tabla
            # Mostrar los datos en pestañas por módulo
            datos_encontrados = False
            for modulo, registros in resultados.items():
                table = self.tab_tables.get(modulo)
                if table is not None:
                    # print(f"[DEBUG] Registros recibidos para Contactos: {len(registros)}")
                    if registros:
                        self.mostrar_tabla_modulo(table, registros)
                        table.setVisible(True)
                        datos_encontrados = True
                    else:
                        table.setVisible(False)
            self.tabs.setVisible(datos_encontrados)
            if not datos_encontrados:
                QMessageBox.information(self, "Sin datos", "No se encontraron datos en Zoho Bigin.")
        else:
            # Si no es Zoho, mantener la simulación
            datos = [
                {"ID": 1, "Nombre": "Empresa A", "Valor": 1000},
                {"ID": 2, "Nombre": "Empresa B", "Valor": 2500},
                {"ID": 3, "Nombre": "Empresa C", "Valor": 1800},
            ]
            self.mostrar_tabla(datos)
        # Al extraer datos exitosamente, mostrar los botones de exportar y actualizar
        self.filtros_widget.show()
        self.btn_exportar.show()
        self.btn_actualizar.show()

    def actualizar_filtros_columnas(self):
        # Actualiza el combo de columnas según la tabla activa
        self.combo_columnas.clear()
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None:
            return
        for col in range(table.columnCount()):
            nombre_col = table.horizontalHeaderItem(col).text()
            self.combo_columnas.addItem(nombre_col)
        self.input_filtro_columna.clear()

    def limpiar_filtro_columna(self):
        self.input_filtro_columna.clear()
        # Opcional: podrías filtrar en tiempo real si lo deseas

    def filtrar_tabla_general(self):
        texto = self.search_box.text().lower()
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None:
            return
        for fila in range(table.rowCount()):
            visible = False
            for col in range(table.columnCount()):
                item = table.item(fila, col)
                if item and texto in item.text().lower():
                    visible = True
                    break
            table.setRowHidden(fila, not visible)

    def filtrar_tabla_columna(self):
        col_idx = self.combo_columnas.currentIndex()
        valor = self.input_filtro_columna.text().lower()
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None or valor == "":
            return
        for fila in range(table.rowCount()):
            item = table.item(fila, col_idx)
            visible = item and valor in item.text().lower()
            table.setRowHidden(fila, not visible)

    def mostrar_tabla_modulo(self, table, registros):
        # Limpieza de campos para visualización profesional
        def limpiar_valor(val):
            if isinstance(val, dict):
                # Mostrar solo el nombre si existe
                return val.get('name', '')
            if isinstance(val, list):
                # Concatenar nombres si es lista de dicts
                return ', '.join([v.get('name', '') if isinstance(v, dict) else str(v) for v in val])
            if val is None:
                return ''
            # Eliminar signos raros y saltos de línea
            return str(val).replace('{', '').replace('}', '').replace("'", '').replace('[', '').replace(']', '').replace('\n', ' ').replace(';', ' ').replace('"', '').strip()

        # Diccionario de mapeo con los nombres reales del JSON de Zoho
        TRATOS_MAP = {
            'id': 'ID Trato',
            'Deal_Name': 'Nombre Trato',
            'Account_Name': 'Empresa',
            'Contact_Name': 'Contacto',
            'Pagadur_a': 'Pagaduría',
            'Amount': 'Importe',
            'Monto_solicitado': 'Monto Aprobado',
            'Plazo_solicitado': 'Plazo solicitado',
            'Compra_cartera': 'Compra cartera',
            'Description': 'Descripción',
            'Type': 'Tipo',
            'Modified_Time': 'Última Modificación',
        }

        # Filtrar y limpiar registros
        if table in self.tab_tables.values() and self.tabs.tabText(self.tabs.indexOf(table)) == "Tratos":
            registros_limpios = []
            for reg in registros:
                reg_limpio = {}
                for k, v in TRATOS_MAP.items():
                    valor = reg.get(k, '')
                    reg_limpio[k] = limpiar_valor(valor)
                registros_limpios.append(reg_limpio)
            # Determinar columnas visibles (solo si hay datos)
            columnas = [k for k, v in TRATOS_MAP.items() if any(r[k] for r in registros_limpios)]
            nombres = [TRATOS_MAP[c] for c in columnas]
            # Mostrar tabla usando el método existente
            table.setRowCount(len(registros_limpios))
            table.setColumnCount(len(columnas))
            table.setHorizontalHeaderLabels(nombres)
            # Definir campos obligatorios
            obligatorios = {'ID Trato', 'Nombre Trato', 'Empresa', 'Contacto', 'Pagaduría', 'Importe'}
            for i, fila in enumerate(registros_limpios):
                for j, clave in enumerate(columnas):
                    valor = fila.get(clave, "")
                    item = QTableWidgetItem()
                    if not valor:
                        if TRATOS_MAP[clave] in obligatorios:
                            item.setText("Obligatorio")
                            item.setForeground(Qt.red)
                        else:
                            item.setText("Sin dato")
                            item.setForeground(Qt.gray)
                    else:
                        item.setText(str(valor))
                    table.setItem(i, j, item)
            table.resizeColumnsToContents()
            table.setVisible(True)
            return
        if not registros:
            table.setVisible(False)
            return
        # Visualización profesional para cada módulo
        modulo = self.tabs.tabText(self.tabs.indexOf(table))
        if modulo == "Tratos":
            campos = [
                ('id', 'ID Trato', True),
                ('Deal_Name', 'Nombre Trato', True),
                ('Account_Name', 'Empresa', True),
                ('Contact_Name', 'Contacto', True),
                ('Pagadur_a', 'Pagaduría', True),
                ('Amount', 'Importe', True),
                ('Monto_solicitado', 'Monto Aprobado', False),
                ('Plazo_solicitado', 'Plazo solicitado', False),
                ('Compra_cartera', 'Compra cartera', False),
                ('Description', 'Descripción', False),
                ('Type', 'Tipo', False),
                ('Modified_Time', 'Última Modificación', False),
            ]
        elif modulo == "Contactos":
            campos = [
                ('id', 'ID Contacto', True),
                ('NUIP1', 'NUIP', True),
                ('Last_Name', 'Apellidos', True),
                ('First_Name', 'Nombre', True),
                ('Account_Name', 'Nombre de Empresa', True),
                ('Email', 'Correo electrónico', False),
                ('Phone', 'Teléfono', False),
                ('Owner', 'Propietario de Contacto', True),
            ]
        elif modulo == "Empresas":
            campos = [
                ('id', 'ID Empresa', True),
                ('Account_Name', 'Nombre de Empresa', True),
                ('Phone', 'Teléfono', False),
                ('Website', 'Sitio web', False),
                ('Owner', 'Propietario de Empresa', True),
                ('Email_nomina', 'Email nomina', False),
                ('Description', 'Descripción', False),
            ]
        # Limpiar y mapear los registros
        registros_limpios = []
        for reg in registros:
            reg_limpio = {}
            for k, nombre, _ in campos:
                valor = reg.get(k, '')
                # Si es Owner, mostrar solo el nombre
                if k == 'Owner' and isinstance(valor, dict):
                    valor = valor.get('name', '')
                reg_limpio[k] = limpiar_valor(valor)
            registros_limpios.append(reg_limpio)
        # Limpiar y mapear los registros SOLO UNA VEZ
        registros_limpios = []
        for reg in registros:
            reg_limpio = {}
            for k, nombre, _ in campos:
                valor = reg.get(k, '')
                # Si es Owner, mostrar solo el nombre
                if k == 'Owner' and isinstance(valor, dict):
                    valor = valor.get('name', '')
                reg_limpio[k] = limpiar_valor(valor)
            registros_limpios.append(reg_limpio)
        # Determinar columnas visibles (solo si hay datos o son obligatorias)
        columnas = [k for k, nombre, req in campos if any(r[k] for r in registros_limpios) or req]
        nombres = [nombre for k, nombre, req in campos if k in columnas]
        # Mostrar tabla usando el método existente
        table.setRowCount(len(registros_limpios))
        table.setColumnCount(len(columnas))
        table.setHorizontalHeaderLabels(nombres)
        for i, fila in enumerate(registros_limpios):
            for j, clave in enumerate(columnas):
                valor = fila.get(clave, "")
                item = QTableWidgetItem()
                obligatorio = False
                for k, nombre, req in campos:
                    if k == clave:
                        obligatorio = req
                        break
                if not valor:
                    if obligatorio:
                        item.setText("Obligatorio")
                        item.setForeground(Qt.red)
                    else:
                        item.setText("Sin dato")
                        item.setForeground(Qt.gray)
                else:
                    item.setText(str(valor))
                table.setItem(i, j, item)
        table.resizeColumnsToContents()
        table.setVisible(True)
        # Al mostrar una nueva tabla, actualizar el combo de columnas
        self.actualizar_filtros_columnas()
        # Eliminar lógica de paginación

    def exportar_tabla_actual(self):
        import pandas as pd
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None or table.rowCount() == 0:
            QMessageBox.warning(self, "Exportar", "No hay datos para exportar en la pestaña actual.")
            return
        # Obtener los datos de la tabla
        columnas = [table.horizontalHeaderItem(i).text() for i in range(table.columnCount())]
        datos = []
        for fila in range(table.rowCount()):
            fila_datos = []
            for col in range(table.columnCount()):
                item = table.item(fila, col)
                fila_datos.append(item.text() if item else "")
            datos.append(fila_datos)
        df = pd.DataFrame(datos, columns=columnas)
        # Diálogo para elegir formato y ruta
        opciones = QFileDialog.Options()
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar como", f"{modulo}.xlsx", "Archivos Excel (*.xlsx);;Archivos CSV (*.csv)", options=opciones)
        if ruta:
            try:
                if ruta.endswith(".csv"):
                    df.to_csv(ruta, index=False, encoding="utf-8-sig")
                else:
                    df.to_excel(ruta, index=False)
                QMessageBox.information(self, "Exportar", f"Datos exportados correctamente a {ruta}")
            except Exception as e:
                QMessageBox.critical(self, "Error de exportación", f"No se pudo exportar: {str(e)}")

    def actualizar_conexiones(self):
        self.config.read("config.ini")
        self.conexion_combo.clear()
        self.conexion_combo.addItems(self.config.sections())
        # Actualizar resumen si hay conexiones
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])
        else:
            self.resumen_label.setText("<i>No hay conexiones configuradas. Usa 'Gestionar conexiones' para crear una.</i>")

    def filtrar_tabla_actual(self):
        texto = self.search_box.text().lower()
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None:
            return
        for fila in range(table.rowCount()):
            visible = False
            for col in range(table.columnCount()):
                item = table.item(fila, col)
                if item and texto in item.text().lower():
                    visible = True
                    break
            table.setRowHidden(fila, not visible)

    def mostrar_dialogo_filtros(self):
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None:
            return
        dialog = QDialog(self)
        dialog.setWindowTitle("Filtros avanzados")
        dialog.setMinimumWidth(400)
        vlayout = QVBoxLayout()
        self.combo_filtros = []
        for col in range(table.columnCount()):
            nombre_col = table.horizontalHeaderItem(col).text()
            hlayout = QHBoxLayout()
            label = QLabel(nombre_col)
            combo = QComboBox()
            combo.addItem("(Todos)")
            valores = set()
            for fila in range(table.rowCount()):
                item = table.item(fila, col)
                if item:
                    valores.add(item.text())
            for valor in sorted(valores):
                combo.addItem(valor)
            hlayout.addWidget(label)
            hlayout.addWidget(combo)
            vlayout.addLayout(hlayout)
            self.combo_filtros.append(combo)
        btn_aplicar = QPushButton("Aplicar filtros")
        btn_aplicar.setStyleSheet("background-color: #1e3c78; color: white; font-size: 13px; border-radius: 8px;")
        btn_aplicar.clicked.connect(lambda: self.aplicar_filtros_avanzados(dialog))
        vlayout.addWidget(btn_aplicar)
        dialog.setLayout(vlayout)
        dialog.exec_()

    def aplicar_filtros_avanzados(self, dialog):
        modulo = self.tabs.tabText(self.tabs.currentIndex())
        table = self.tab_tables.get(modulo)
        if table is None:
            return
        filtros = [combo.currentText() for combo in self.combo_filtros]
        for fila in range(table.rowCount()):
            visible = True
            for col, filtro in enumerate(filtros):
                if filtro != "(Todos)":
                    item = table.item(fila, col)
                    if not item or item.text() != filtro:
                        visible = False
                        break
            table.setRowHidden(fila, not visible)
        dialog.accept()

    def mostrar_detalle_registro(self, table, registros):
        selected = table.selectedItems()
        if not selected:
            self.panel_detalle.hide()
            return
        fila = selected[0].row()
        # Buscar el registro original (puede estar filtrado)
        if fila < len(registros):
            registro = registros[fila]
            # Limpiar panel
            for i in reversed(range(self.panel_detalle_layout.count())):
                widget = self.panel_detalle_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()
            # Mostrar detalles
            title = QLabel("Detalles del registro")
            title.setStyleSheet("font-size: 16px; font-weight: bold; color: #1e3c78; margin-bottom: 10px;")
            self.panel_detalle_layout.addWidget(title)
            for k, v in registro.items():
                label = QLabel(f"<b>{k}:</b> {v}")
                label.setStyleSheet("font-size: 13px; color: #333; margin-bottom: 4px;")
                self.panel_detalle_layout.addWidget(label)
            self.panel_detalle.show()

    def actualizar_datos(self):
        # Recarga los datos de la fuente seleccionada y actualiza la tabla activa
        self.extraer_datos()
