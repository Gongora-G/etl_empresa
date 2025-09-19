from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QFileDialog, QMessageBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt
import os


class DatalakeView(QWidget):
    """
    Vista profesional para gestión de archivos del Datalake.
    Permite visualizar, descargar y eliminar archivos crudos, mostrando metadatos y aplicando estilos consistentes.
    """
    def __init__(self, datalake_path="datalake", parent=None):
        super().__init__(parent)
        self.datalake_path = datalake_path
        self.setWindowTitle("Datalake - Archivos almacenados")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 10, 20, 10)
        main_layout.setSpacing(8)
        title = QLabel("Datalake: Archivos almacenados")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3c78; margin-bottom: 2px;")
        main_layout.addWidget(title)
        desc = QLabel("Aquí puedes visualizar, descargar o eliminar los archivos almacenados en el Datalake local.")
        desc.setStyleSheet("font-size: 12px; color: #333; margin-bottom: 0px;")
        main_layout.addWidget(desc)

        splitter = QSplitter(Qt.Horizontal)

        # Tabla de archivos
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Tamaño", "Fecha creación", "Tipo"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setStyleSheet(
            "QTableWidget { background: #f8fafc; border: 1px solid #d0d7e5; font-size: 13px; }"
            "QHeaderView::section { background: #e3eaf6; font-weight: bold; border: 1px solid #d0d7e5; min-height: 28px; }"
            "QTableWidget::item:selected { background: #c7e0fa; }"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumWidth(500)
        self.table.setColumnWidth(0, 220)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 140)
        self.table.setColumnWidth(3, 70)
        self.table.setContentsMargins(0, 0, 0, 0)
        self.table.setShowGrid(True)
        self.table.setStyleSheet(self.table.styleSheet() + "QTableWidget { margin-top: 0px; margin-bottom: 0px; }")
        self.table.itemSelectionChanged.connect(self.mostrar_metadatos)
        splitter.addWidget(self.table)

        # Panel lateral de metadatos
        self.metadatos_panel = QFrame()
        self.metadatos_panel.setMinimumWidth(220)
        self.metadatos_panel.setStyleSheet("background: #f4f7fb; border-left: 1px solid #d0d7e5; margin-top: 0px;")
        self.metadatos_layout = QVBoxLayout(self.metadatos_panel)
        self.metadatos_layout.setContentsMargins(10, 10, 10, 10)
        self.metadatos_layout.setSpacing(4)
        self.lbl_metadatos = QLabel("Selecciona un archivo para ver metadatos.")
        self.lbl_metadatos.setStyleSheet("font-size: 12px; color: #444;")
        self.metadatos_layout.addWidget(self.lbl_metadatos)
        self.metadatos_layout.addStretch()
        splitter.addWidget(self.metadatos_panel)

        main_layout.addWidget(splitter)

        # Botones de acción
        btns_layout = QHBoxLayout()
        btns_layout.setSpacing(12)
        self.btn_descargar = QPushButton("Descargar archivo")
        self.btn_descargar.setStyleSheet("background: #1e3c78; color: white; padding: 5px 16px; border-radius: 5px; font-size: 13px;")
        self.btn_descargar.setCursor(Qt.PointingHandCursor)
        self.btn_descargar.clicked.connect(self.descargar_archivo)
        btns_layout.addWidget(self.btn_descargar)
        self.btn_eliminar = QPushButton("Eliminar archivo")
        self.btn_eliminar.setStyleSheet("background: #e53e3e; color: white; padding: 5px 16px; border-radius: 5px; font-size: 13px;")
        self.btn_eliminar.setCursor(Qt.PointingHandCursor)
        self.btn_eliminar.clicked.connect(self.eliminar_archivo)
        btns_layout.addWidget(self.btn_eliminar)
        btns_layout.addStretch()
        main_layout.addLayout(btns_layout)

        self.actualizar_lista_archivos()

    def actualizar_lista_archivos(self):
        self.table.setRowCount(0)
        if not os.path.exists(self.datalake_path):
            os.makedirs(self.datalake_path)
        archivos = os.listdir(self.datalake_path)
        for archivo in archivos:
            ruta = os.path.join(self.datalake_path, archivo)
            if os.path.isfile(ruta):
                size = os.path.getsize(ruta)
                fecha = os.path.getctime(ruta)
                tipo = os.path.splitext(archivo)[1][1:].upper() or "-"
                from datetime import datetime
                fecha_str = datetime.fromtimestamp(fecha).strftime("%Y-%m-%d %H:%M")
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(archivo))
                self.table.setItem(row, 1, QTableWidgetItem(f"{size/1024:.1f} KB"))
                self.table.setItem(row, 2, QTableWidgetItem(fecha_str))
                self.table.setItem(row, 3, QTableWidgetItem(tipo))

    def descargar_archivo(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Descargar", "Selecciona un archivo para descargar.")
            return
        nombre = self.table.item(row, 0).text()
        ruta_origen = os.path.join(self.datalake_path, nombre)
        ruta_destino, _ = QFileDialog.getSaveFileName(self, "Guardar como", nombre)
        if ruta_destino:
            try:
                with open(ruta_origen, "rb") as fsrc, open(ruta_destino, "wb") as fdst:
                    fdst.write(fsrc.read())
                QMessageBox.information(self, "Descargar", f"Archivo guardado en {ruta_destino}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo descargar: {str(e)}")

    def eliminar_archivo(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Eliminar", "Selecciona un archivo para eliminar.")
            return
        nombre = self.table.item(row, 0).text()
        ruta = os.path.join(self.datalake_path, nombre)
        try:
            os.remove(ruta)
            self.actualizar_lista_archivos()
            QMessageBox.information(self, "Eliminar", f"Archivo '{nombre}' eliminado del Datalake.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar: {str(e)}")

    def mostrar_metadatos(self):
        row = self.table.currentRow()
        if row < 0:
            self.lbl_metadatos.setText("Selecciona un archivo para ver metadatos.")
            return
        nombre = self.table.item(row, 0).text()
        ruta = os.path.join(self.datalake_path, nombre)
        if not os.path.isfile(ruta):
            self.lbl_metadatos.setText("Archivo no encontrado.")
            return
        size = os.path.getsize(ruta)
        fecha = os.path.getctime(ruta)
        from datetime import datetime
        fecha_str = datetime.fromtimestamp(fecha).strftime("%Y-%m-%d %H:%M:%S")
        tipo = os.path.splitext(nombre)[1][1:].upper() or "-"
        metadatos = (
            f"<b>Nombre:</b> {nombre}<br>"
            f"<b>Tamaño:</b> {size/1024:.2f} KB<br>"
            f"<b>Fecha creación:</b> {fecha_str}<br>"
            f"<b>Tipo:</b> {tipo}"
        )
        self.lbl_metadatos.setText(metadatos)
