from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt
from .connection_manager import ConnectionManager

class ExtractionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        title = QLabel("Extracción de Datos")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e3c78;")
        layout.addWidget(title)

        desc = QLabel("Configura y prueba la extracción de datos desde diferentes fuentes:")
        desc.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(desc)

        # Selección de fuente
        fuente_layout = QHBoxLayout()
        fuente_label = QLabel("Fuente de datos:")
        fuente_combo = QComboBox()
        fuente_combo.addItems(["Zoho Bigin", "SQL Server", "Excel/CSV", "Otro"])
        fuente_layout.addWidget(fuente_label)
        fuente_layout.addWidget(fuente_combo)
        layout.addLayout(fuente_layout)

        # Parámetro de conexión (ejemplo)
        param_layout = QHBoxLayout()
        param_label = QLabel("Parámetro/conexión:")
        param_input = QLineEdit()
        param_input.setPlaceholderText("Cadena de conexión, ruta o token...")
        param_layout.addWidget(param_label)
        param_layout.addWidget(param_input)
        layout.addLayout(param_layout)

        # Botón para cargar archivo si es Excel/CSV
        self.btn_archivo = QPushButton("Seleccionar archivo")
        self.btn_archivo.setVisible(False)
        layout.addWidget(self.btn_archivo)

        # Botón de prueba de extracción
        btn_test = QPushButton("Probar extracción")
        btn_test.setStyleSheet("background-color: #1e3c78; color: white; font-size: 15px; padding: 8px 20px; border-radius: 8px;")
        layout.addWidget(btn_test)

        # Resultado de prueba
        self.resultado = QLabel("")
        self.resultado.setStyleSheet("color: #1e3c78; margin-top: 10px;")
        layout.addWidget(self.resultado)

        # Tabla para mostrar datos extraídos
        self.table = QTableWidget()
        self.table.setVisible(False)
        layout.addWidget(self.table)

        # Gestor visual de conexiones (debe ir antes de actualizar_conexiones)
        self.connection_manager = ConnectionManager()

        # Botón para abrir gestor de conexiones (ubicado abajo a la derecha)
        bottom_btn_layout = QHBoxLayout()
        bottom_btn_layout.addStretch()
        self.btn_gestionar_conexiones = QPushButton("Gestionar conexiones")
        self.btn_gestionar_conexiones.setStyleSheet("background-color: #1e3c78; color: white; font-size: 13px; padding: 5px 16px; border-radius: 8px;")
        self.btn_gestionar_conexiones.setFixedWidth(170)
        bottom_btn_layout.addWidget(self.btn_gestionar_conexiones)
        layout.addStretch()
        layout.addLayout(bottom_btn_layout)
        self.btn_gestionar_conexiones.clicked.connect(self.mostrar_gestor_conexiones)

        self.setLayout(layout)

        # Lógica para mostrar botón de archivo solo si es Excel/CSV
        fuente_combo.currentTextChanged.connect(self.toggle_archivo)
        self.btn_archivo.clicked.connect(self.seleccionar_archivo)
        btn_test.clicked.connect(self.probar_extraccion)

    def toggle_archivo(self, text):
        self.btn_archivo.setVisible(text == "Excel/CSV")

    def seleccionar_archivo(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos Excel/CSV (*.xlsx *.csv)")
        if file:
            self.resultado.setText(f"Archivo seleccionado: {file}")

    def probar_extraccion(self):
        # Simulación de extracción de datos (ejemplo)
        # En la versión real, aquí se llamaría al módulo correspondiente
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
        self.conexion_combo.clear()
        self.conexion_combo.addItems(self.connection_manager.config.sections())

    def cargar_parametros_conexion(self, nombre):
        if nombre in self.connection_manager.config:
            params = self.connection_manager.config[nombre]
            # Aquí podrías poblar los campos de parámetros según la conexión seleccionada
            # Por simplicidad, solo mostramos los parámetros en consola
            print(f"Conexión seleccionada: {nombre}")
            for k, v in params.items():
                print(f"  {k}: {v}")

    def mostrar_gestor_conexiones(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Gestor de Conexiones")
        dialog.setMinimumWidth(500)
        dialog_layout = QVBoxLayout()
        gestor = ConnectionManager()
        dialog_layout.addWidget(gestor)
        dialog.setLayout(dialog_layout)
        dialog.exec_()
