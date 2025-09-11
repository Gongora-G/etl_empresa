from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from .connection_manager import ConnectionManager
import configparser

class ExtractionView(QWidget):
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
        layout.addLayout(botones_layout)

        # Tabla de resultados
        self.table = QTableWidget()
        self.table.setVisible(False)
        layout.addWidget(self.table)

        # Espaciador vertical para empujar todo hacia abajo
        layout.addStretch()

        # Layout horizontal para el botón en la esquina inferior derecha
        bottom_btn_layout = QHBoxLayout()
        bottom_btn_layout.addStretch()  # Empuja el botón a la derecha
        self.btn_gestionar_conexiones = QPushButton("Gestionar conexiones")
        self.btn_gestionar_conexiones.setStyleSheet("background-color: #1e3c78; color: white; font-size: 14px; padding: 6px 18px; border-radius: 8px;")
        self.btn_gestionar_conexiones.setFixedWidth(170)
        bottom_btn_layout.addWidget(self.btn_gestionar_conexiones)
        layout.addLayout(bottom_btn_layout)
        self.btn_gestionar_conexiones.clicked.connect(self.mostrar_gestor_conexiones)

        self.setLayout(layout)

        # Mostrar resumen inicial
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])
        else:
            self.resumen_label.setText("<i>No hay conexiones configuradas. Usa 'Gestionar conexiones' para crear una.</i>")

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
            datos = []
            for modulo, registros in resultados.items():
                for registro in registros:
                    fila = {"Módulo": modulo}
                    fila.update(registro)
                    datos.append(fila)
            if datos:
                self.mostrar_tabla(datos)
            else:
                QMessageBox.information(self, "Sin datos", "No se encontraron datos en Zoho Bigin.")
        else:
            # Si no es Zoho, mantener la simulación
            datos = [
                {"ID": 1, "Nombre": "Empresa A", "Valor": 1000},
                {"ID": 2, "Nombre": "Empresa B", "Valor": 2500},
                {"ID": 3, "Nombre": "Empresa C", "Valor": 1800},
            ]
            self.mostrar_tabla(datos)

    def mostrar_tabla(self, datos):
        if not datos:
            self.table.setVisible(False)
            return
        self.table.setVisible(True)
        self.table.setRowCount(len(datos))
        self.table.setColumnCount(len(datos[0]))
        self.table.setHorizontalHeaderLabels(list(datos[0].keys()))
        for i, fila in enumerate(datos):
            for j, clave in enumerate(fila):
                self.table.setItem(i, j, QTableWidgetItem(str(fila[clave])))

    def actualizar_conexiones(self):
        self.config.read("config.ini")
        self.conexion_combo.clear()
        self.conexion_combo.addItems(self.config.sections())
        # Actualizar resumen si hay conexiones
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])
        else:
            self.resumen_label.setText("<i>No hay conexiones configuradas. Usa 'Gestionar conexiones' para crear una.</i>")
