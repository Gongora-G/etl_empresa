from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import os

class DatalakeView(QWidget):
    def __init__(self, datalake_path="datalake", parent=None):
        super().__init__(parent)
        self.datalake_path = datalake_path
        self.setWindowTitle("Datalake - Archivos almacenados")
        layout = QVBoxLayout()

        title = QLabel("Datalake: Archivos almacenados")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #1e3c78;")
        layout.addWidget(title)

        desc = QLabel("Aquí puedes visualizar, descargar o eliminar los archivos almacenados en el Datalake local.")
        desc.setStyleSheet("font-size: 13px; color: #333;")
        layout.addWidget(desc)

        self.archivos_list = QListWidget()
        layout.addWidget(self.archivos_list)

        btns_layout = QHBoxLayout()
        self.btn_descargar = QPushButton("Descargar archivo")
        self.btn_descargar.clicked.connect(self.descargar_archivo)
        btns_layout.addWidget(self.btn_descargar)
        self.btn_eliminar = QPushButton("Eliminar archivo")
        self.btn_eliminar.clicked.connect(self.eliminar_archivo)
        btns_layout.addWidget(self.btn_eliminar)
        layout.addLayout(btns_layout)

        self.setLayout(layout)
        self.actualizar_lista_archivos()

    def actualizar_lista_archivos(self):
        self.archivos_list.clear()
        if not os.path.exists(self.datalake_path):
            os.makedirs(self.datalake_path)
        archivos = os.listdir(self.datalake_path)
        for archivo in archivos:
            self.archivos_list.addItem(archivo)

    def descargar_archivo(self):
        item = self.archivos_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Descargar", "Selecciona un archivo para descargar.")
            return
        nombre = item.text()
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
        item = self.archivos_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Eliminar", "Selecciona un archivo para eliminar.")
            return
        nombre = item.text()
        ruta = os.path.join(self.datalake_path, nombre)
        try:
            os.remove(ruta)
            self.actualizar_lista_archivos()
            QMessageBox.information(self, "Eliminar", f"Archivo '{nombre}' eliminado del Datalake.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo eliminar: {str(e)}")
