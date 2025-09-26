from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, 
    QHBoxLayout, QFileDialog, QMessageBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt
import os
import shutil
from datetime import datetime


class DatalakeView(QWidget):
    def __init__(self):
        super().__init__()
        self.datalake_path = "data/datalake"
        self.init_ui()
        self.cargar_archivos()

    def init_ui(self):
        # Layout principal sin espacios desperdiciados
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        main_layout.setSpacing(0)                    # Sin espaciado

        # Título principal pegado arriba sin espacios
        title = QLabel("🗄️ Gestor de Archivos - Datalake")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #1e3c78; margin: 0px; padding: 12px 18px;")
        main_layout.addWidget(title)

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
            "QTableWidget { background: #f8fafc; border: 1px solid #d0d7e5; font-size: 15px; }"
            "QHeaderView::section { background: #e3eaf6; font-weight: bold; border: 1px solid #d0d7e5; min-height: 32px; padding: 8px; font-size: 15px; }"
            "QTableWidget::item:selected { background: #c7e0fa; }"
            "QTableWidget::item { padding: 10px; }"
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(500)  # Altura aumentada para mayor extensión hacia arriba
        # Configurar anchos de columnas optimizados para diferentes tamaños de ventana
        self.table.setColumnWidth(0, 350)  # Nombre de archivo más ancho
        self.table.setColumnWidth(1, 100)  # Tamaño
        self.table.setColumnWidth(2, 130)  # Fecha más ancha
        self.table.setColumnWidth(3, 80)   # Tipo
        self.table.horizontalHeader().setStretchLastSection(True)  # Última columna se expande
        self.table.setShowGrid(True)
        self.table.itemSelectionChanged.connect(self.mostrar_metadatos)
        splitter.addWidget(self.table)

        # Panel de metadatos sin espacios desperdiciados
        self.metadatos_panel = QFrame()
        self.metadatos_panel.setMinimumWidth(200)
        self.metadatos_panel.setMaximumWidth(250)
        self.metadatos_panel.setStyleSheet("background: #f9fafb; border-left: 2px solid #e5e7eb; border-radius: 0px;")
        self.metadatos_layout = QVBoxLayout(self.metadatos_panel)
        self.metadatos_layout.setContentsMargins(10, 10, 10, 10)
        self.metadatos_layout.setSpacing(5)
        
        # Título del panel
        metadatos_title = QLabel("📋 Detalles del archivo")
        metadatos_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151; margin-bottom: 8px;")
        self.metadatos_layout.addWidget(metadatos_title)
        
        self.lbl_metadatos = QLabel("Selecciona un archivo para ver detalles.")
        self.lbl_metadatos.setStyleSheet("font-size: 14px; color: #6b7280; padding: 8px; background: #f3f4f6; border-radius: 4px; line-height: 1.4;")
        self.lbl_metadatos.setWordWrap(True)
        self.metadatos_layout.addWidget(self.lbl_metadatos)
        self.metadatos_layout.addStretch()
        splitter.addWidget(self.metadatos_panel)
        
        # Configurar proporciones del splitter para máximo uso del espacio
        splitter.setSizes([750, 250])  # 75% tabla, 25% metadatos
        splitter.setStretchFactor(0, 1)  # La tabla se expande
        splitter.setStretchFactor(1, 0)  # Panel metadatos tamaño fijo
        
        main_layout.addWidget(splitter)

        # Botones en la parte inferior (grandes y visibles)
        btns_frame = QFrame()
        btns_frame.setMaximumHeight(60)  # Altura aumentada para botones más grandes
        btns_frame.setStyleSheet("background: #f8fafc; border-top: 1px solid #e5e7eb; margin: 0px;")
        btns_layout = QHBoxLayout(btns_frame)
        btns_layout.setContentsMargins(12, 10, 12, 10)  # Márgenes apropiados para botones grandes
        btns_layout.setSpacing(10)                       # Espacio entre botones grandes
        
        # Botones grandes con iconos y texto
        self.btn_subir = QPushButton("📤 Subir")
        self.btn_subir.setToolTip("Subir archivo al datalake")
        self.btn_subir.setFixedSize(95, 40)
        self.btn_subir.setStyleSheet("QPushButton { background: #1e3c78; color: white; border-radius: 6px; font-size: 15px; border: none; font-weight: bold; } QPushButton:hover { background: #2563eb; }")
        self.btn_subir.setCursor(Qt.PointingHandCursor)
        self.btn_subir.clicked.connect(self.subir_archivo)
        btns_layout.addWidget(self.btn_subir)
        
        self.btn_descargar = QPushButton("📥 Descargar")
        self.btn_descargar.setToolTip("Descargar archivo seleccionado")
        self.btn_descargar.setFixedSize(120, 40)
        self.btn_descargar.setStyleSheet("QPushButton { background: #1e3c78; color: white; border-radius: 6px; font-size: 15px; border: none; font-weight: bold; } QPushButton:hover { background: #374151; }")
        self.btn_descargar.setCursor(Qt.PointingHandCursor)
        self.btn_descargar.clicked.connect(self.descargar_archivo)
        btns_layout.addWidget(self.btn_descargar)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setToolTip("Eliminar archivo seleccionado")
        self.btn_eliminar.setFixedSize(110, 40)
        self.btn_eliminar.setStyleSheet("QPushButton { background: #dc2626; color: white; border-radius: 6px; font-size: 15px; border: none; font-weight: bold; } QPushButton:hover { background: #b91c1c; }")
        self.btn_eliminar.setCursor(Qt.PointingHandCursor)
        self.btn_eliminar.clicked.connect(self.eliminar_archivo)
        btns_layout.addWidget(self.btn_eliminar)
        
        # Espaciador para empujar la ubicación al final
        btns_layout.addStretch()
        
        # Información de ubicación al final de la línea
        ubicacion_lbl = QLabel(f"📂 {os.path.abspath(self.datalake_path)}")
        ubicacion_lbl.setStyleSheet("font-size: 12px; color: #6b7280; font-style: italic; margin-right: 8px;")
        btns_layout.addWidget(ubicacion_lbl)
        
        main_layout.addWidget(btns_frame)

    def cargar_archivos(self):
        """Cargar archivos del datalake en la tabla"""
        try:
            if not os.path.exists(self.datalake_path):
                os.makedirs(self.datalake_path)
            
            files = os.listdir(self.datalake_path)
            self.table.setRowCount(len(files))
            
            for i, filename in enumerate(files):
                filepath = os.path.join(self.datalake_path, filename)
                if os.path.isfile(filepath):
                    # Nombre del archivo
                    self.table.setItem(i, 0, QTableWidgetItem(filename))
                    
                    # Tamaño del archivo
                    size = os.path.getsize(filepath)
                    size_str = self.format_size(size)
                    self.table.setItem(i, 1, QTableWidgetItem(size_str))
                    
                    # Fecha de modificación
                    mtime = os.path.getmtime(filepath)
                    date_str = datetime.fromtimestamp(mtime).strftime("%d/%m/%Y %H:%M")
                    self.table.setItem(i, 2, QTableWidgetItem(date_str))
                    
                    # Tipo de archivo
                    ext = os.path.splitext(filename)[1].upper()
                    self.table.setItem(i, 3, QTableWidgetItem(ext))
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar archivos: {str(e)}")

    def format_size(self, size_bytes):
        """Formatear el tamaño del archivo"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s}{size_names[i]}"

    def mostrar_metadatos(self):
        """Mostrar metadatos del archivo seleccionado"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            filename = self.table.item(current_row, 0).text()
            filepath = os.path.join(self.datalake_path, filename)
            
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                
                metadatos = f"""
📄 <b>{filename}</b><br><br>
📊 <b>Tamaño:</b> {self.format_size(stat.st_size)}<br>
📅 <b>Creado:</b> {datetime.fromtimestamp(stat.st_ctime).strftime('%d/%m/%Y %H:%M')}<br>
🔄 <b>Modificado:</b> {datetime.fromtimestamp(stat.st_mtime).strftime('%d/%m/%Y %H:%M')}<br>
📍 <b>Ruta:</b> {filepath}
                """.strip()
                
                self.lbl_metadatos.setText(metadatos)
            else:
                self.lbl_metadatos.setText("Archivo no encontrado.")
        else:
            self.lbl_metadatos.setText("Selecciona un archivo para ver detalles.")

    def subir_archivo(self):
        """Subir archivo al datalake"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Seleccionar archivo", "", "Todos los archivos (*)"
            )
            
            if file_path:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(self.datalake_path, filename)
                
                if os.path.exists(dest_path):
                    reply = QMessageBox.question(
                        self, "Archivo existe", 
                        f"El archivo '{filename}' ya existe. ¿Desea reemplazarlo?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        return
                
                shutil.copy2(file_path, dest_path)
                QMessageBox.information(self, "Éxito", f"Archivo '{filename}' subido correctamente.")
                self.cargar_archivos()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al subir archivo: {str(e)}")

    def descargar_archivo(self):
        """Descargar archivo del datalake"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Advertencia", "Seleccione un archivo para descargar.")
                return
            
            filename = self.table.item(current_row, 0).text()
            source_path = os.path.join(self.datalake_path, filename)
            
            if not os.path.exists(source_path):
                QMessageBox.warning(self, "Error", "El archivo no existe.")
                return
            
            dest_path, _ = QFileDialog.getSaveFileName(
                self, "Guardar archivo", filename, "Todos los archivos (*)"
            )
            
            if dest_path:
                shutil.copy2(source_path, dest_path)
                QMessageBox.information(self, "Éxito", f"Archivo descargado como '{dest_path}'.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al descargar archivo: {str(e)}")

    def eliminar_archivo(self):
        """Eliminar archivo del datalake"""
        try:
            current_row = self.table.currentRow()
            if current_row < 0:
                QMessageBox.warning(self, "Advertencia", "Seleccione un archivo para eliminar.")
                return
            
            filename = self.table.item(current_row, 0).text()
            filepath = os.path.join(self.datalake_path, filename)
            
            if not os.path.exists(filepath):
                QMessageBox.warning(self, "Error", "El archivo no existe.")
                return
            
            reply = QMessageBox.question(
                self, "Confirmar eliminación", 
                f"¿Está seguro de que desea eliminar '{filename}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                os.remove(filepath)
                QMessageBox.information(self, "Éxito", f"Archivo '{filename}' eliminado correctamente.")
                self.cargar_archivos()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar archivo: {str(e)}")