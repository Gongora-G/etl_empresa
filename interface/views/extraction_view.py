from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QMessageBox, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt
from .connection_manager import ConnectionManager
import configparser

class ExtractionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        # Resumen visual de campos
        self.resumen_label = QLabel()
        self.resumen_label.setStyleSheet("font-size: 12px; color: #1e3c78; background: #f5f5f5; border-radius: 8px; padding: 8px;")
        layout.addWidget(self.resumen_label)

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

        # Mostrar resumen inicial
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])

    def mostrar_resumen_conexion(self, nombre):
        if nombre in self.config:
            params = self.config[nombre]
            resumen = "<b>Parámetros de conexión:</b><br>"
            for k in params:
                if not k.endswith('_type'):
                    tipo = params.get(f"{k}_type", "Texto")
                    resumen += f"<b>{k}</b> ({tipo}): {params[k]}<br>"
            self.resumen_label.setText(resumen)
        else:
            self.resumen_label.setText("")

    def probar_conexion(self):
        nombre = self.conexion_combo.currentText()
        params = self.config[nombre] if nombre in self.config else {}
        # Aquí va la lógica real de prueba de conexión
        # Por ahora, solo simula éxito
        QMessageBox.information(self, "Prueba de conexión", f"Conexión '{nombre}' probada exitosamente.")

    def extraer_datos(self):
        nombre = self.conexion_combo.currentText()
        params = self.config[nombre] if nombre in self.config else {}
        # Aquí va la lógica real de extracción
        # Simulación de datos
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
            self.resumen_label.setText("")

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
        gestor = ConnectionManager(self)
        dialog_layout.addWidget(gestor)
        dialog.setLayout(dialog_layout)
        dialog.exec_()
        # Refrescar lista de conexiones al cerrar gestor
        self.config.read("config.ini")
        self.conexion_combo.clear()
        self.conexion_combo.addItems(self.config.sections())
        # Actualizar resumen visual si hay conexiones
        if self.config.sections():
            self.mostrar_resumen_conexion(self.config.sections()[0])
