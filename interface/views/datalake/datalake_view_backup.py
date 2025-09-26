from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTable        # Botones ultra-compactos con íconos solamente
        self.btn_subir = QPushButton("📤")
        self.btn_subir.setToolTip("Subir archivo")
        self.btn_subir.setFixedSize(20, 20)
        self.btn_subir.setStyleSheet("QPushButton { background: #3b82f6; color: white; border-radius: 2px; font-size: 9px; border: none; } QPushButton:hover { background: #2563eb; }")
        self.btn_subir.setCursor(Qt.PointingHandCursor)
        self.btn_subir.clicked.connect(self.subir_archivo)
        btns_layout.addWidget(self.btn_subir)tItem, QHBoxLayout, QFileDialog, QMessageBox, QFrame, QSplitter
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
        main_layout.setContentsMargins(8, 1, 8, 1)  # Márgenes mínimos
        main_layout.setSpacing(1)                    # Espacio mínimo entre elementos
        
        # Header en UNA línea ultra compacto
        header_layout = QHBoxLayout()
        header_layout.setSpacing(6)
        header_layout.setContentsMargins(0, 0, 0, 0)
        title = QLabel("📊 Datalake")
        title.setStyleSheet("font-size: 13px; font-weight: bold; color: #1e3c78; margin: 0px; padding: 1px;")
        header_layout.addWidget(title)
        desc = QLabel("• Gestiona archivos")
        desc.setStyleSheet("font-size: 9px; color: #777; margin: 0px; padding: 1px;")
        header_layout.addWidget(desc)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Splitter principal maximizado
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Tabla de archivos maximizada
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Archivo", "Tamaño", "Fecha", "Tipo"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setStyleSheet(
            "QTableWidget { background: #f8fafc; border: 1px solid #d0d7e5; font-size: 12px; }"
            "QHeaderView::section { background: #e3eaf6; font-weight: bold; border: 1px solid #d0d7e5; min-height: 26px; padding: 4px; }"
            "QTableWidget::item:selected { background: #c7e0fa; }"
            "QTableWidget::item { padding: 6px; }"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(400)  # Más altura para la tabla
        # Configurar anchos de columnas optimizados
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 60)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setShowGrid(True)
        self.table.itemSelectionChanged.connect(self.mostrar_metadatos)
        splitter.addWidget(self.table)

        # Panel de metadatos optimizado
        self.metadatos_panel = QFrame()
        self.metadatos_panel.setMinimumWidth(180)
        self.metadatos_panel.setMaximumWidth(220)
        self.metadatos_panel.setStyleSheet("background: #f9fafb; border-left: 2px solid #e5e7eb; border-radius: 0px;")
        self.metadatos_layout = QVBoxLayout(self.metadatos_panel)
        self.metadatos_layout.setContentsMargins(6, 6, 6, 6)
        self.metadatos_layout.setSpacing(1)
        
        # Título del panel
        metadatos_title = QLabel("📋 Detalles del archivo")
        metadatos_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #374151; margin-bottom: 4px;")
        self.metadatos_layout.addWidget(metadatos_title)
        
        self.lbl_metadatos = QLabel("Selecciona un archivo para ver detalles.")
        self.lbl_metadatos.setStyleSheet("font-size: 10px; color: #6b7280; padding: 4px; background: #f3f4f6; border-radius: 3px;")
        self.lbl_metadatos.setWordWrap(True)
        self.metadatos_layout.addWidget(self.lbl_metadatos)
        self.metadatos_layout.addStretch()
        splitter.addWidget(self.metadatos_panel)
        
        # Configurar proporciones del splitter (70% tabla, 30% metadatos)
        splitter.setSizes([700, 300])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        
        main_layout.addWidget(splitter)

        # Botones en la parte inferior (más compactos)
        btns_frame = QFrame()
        btns_frame.setMaximumHeight(26)  # Altura máxima reducida
        btns_frame.setStyleSheet("background: #f8fafc; border-top: 1px solid #e5e7eb; margin: 0px;")
        btns_layout = QHBoxLayout(btns_frame)
        btns_layout.setContentsMargins(4, 1, 4, 1)  # Márgenes ultra mínimos
        btns_layout.setSpacing(3)                    # Espacio mínimo entre botones
        
        self.btn_subir = QPushButton("� Subir")
        self.btn_subir.setStyleSheet("background: #3b82f6; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold; border: none;")
        self.btn_subir.setCursor(Qt.PointingHandCursor)
        self.btn_subir.clicked.connect(self.subir_archivo)
        btns_layout.addWidget(self.btn_subir)
        
        self.btn_descargar = QPushButton("💾 Descargar")
        self.btn_descargar.setStyleSheet("background: #1f2937; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold; border: none;")
        self.btn_descargar.setCursor(Qt.PointingHandCursor)
        self.btn_descargar.clicked.connect(self.descargar_archivo)
        btns_layout.addWidget(self.btn_descargar)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("background: #dc2626; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold; border: none;")
        self.btn_eliminar.setCursor(Qt.PointingHandCursor)
        self.btn_eliminar.clicked.connect(self.eliminar_archivo)
        btns_layout.addWidget(self.btn_eliminar)
        
        btns_layout.addSpacing(10)
        
        # Información de ubicación compacta
        ubicacion_lbl = QLabel(f"📂 {os.path.abspath(self.datalake_path)}")
        ubicacion_lbl.setStyleSheet("font-size: 9px; color: #6b7280; font-family: monospace;")
        btns_layout.addWidget(ubicacion_lbl)
        btns_layout.addStretch()
        
        main_layout.addWidget(btns_frame)

        self.actualizar_lista_archivos()


    def subir_archivo(self):
        """Permite al usuario seleccionar y subir un archivo al Datalake."""
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo para subir")
        if not ruta_archivo:
            return
        nombre = os.path.basename(ruta_archivo)
        destino = os.path.join(self.datalake_path, nombre)
        if os.path.exists(destino):
            resp = QMessageBox.question(self, "Sobrescribir archivo", f"El archivo '{nombre}' ya existe en el Datalake. ¿Deseas sobrescribirlo?", QMessageBox.Yes | QMessageBox.No)
            if resp != QMessageBox.Yes:
                return
        try:
            with open(ruta_archivo, "rb") as fsrc, open(destino, "wb") as fdst:
                fdst.write(fsrc.read())
            self.actualizar_lista_archivos()
            QMessageBox.information(self, "Subida exitosa", f"Archivo '{nombre}' subido al Datalake.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo subir el archivo: {str(e)}")

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
            self.lbl_metadatos.setText("Selecciona un archivo para ver detalles.")
            return
        nombre = self.table.item(row, 0).text()
        ruta = os.path.join(self.datalake_path, nombre)
        if not os.path.isfile(ruta):
            self.lbl_metadatos.setText("❌ Archivo no encontrado.")
            return
        size = os.path.getsize(ruta)
        fecha = os.path.getctime(ruta)
        from datetime import datetime
        fecha_str = datetime.fromtimestamp(fecha).strftime("%d/%m/%Y %H:%M")
        tipo = os.path.splitext(nombre)[1][1:].upper() or "SIN EXTENSIÓN"
        
        # Formatear tamaño
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024*1024:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size/(1024*1024):.1f} MB"
            
        metadatos = (
            f"<div style='font-size: 10px; line-height: 14px;'>"
            f"<b>📄 {nombre}</b><br><br>"
            f"<b>📏 Tamaño:</b> {size_str}<br>"
            f"<b>📅 Creado:</b> {fecha_str}<br>"
            f"<b>🏷️ Tipo:</b> {tipo}<br>"
            f"</div>"
        )
        self.lbl_metadatos.setText(metadatos)
