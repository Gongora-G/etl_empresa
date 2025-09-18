"""
Interfaz principal del software ETL usando PyQt5
"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QPushButton, QListWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from interface.views import ExtractionView
from interface.views.connection_manager import ConnectionManager
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection_manager = ConnectionManager()
        self.setWindowTitle("ETL Empresa - Escritorio")
        self.setGeometry(100, 100, 1000, 700)

        azul = QColor(30, 60, 120)
        gris = QColor(240, 240, 240)

        # Layout principal horizontal
        main_layout = QHBoxLayout()

        # Menú lateral
        menu_frame = QFrame()
        menu_frame.setFixedWidth(220)
        menu_frame.setStyleSheet(f"background-color: rgb({azul.red()}, {azul.green()}, {azul.blue()});")
        menu_layout = QVBoxLayout()

        logo_label = QLabel()
        logo_label.setFixedHeight(100)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setText("[LOGO]")
        logo_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        menu_layout.addWidget(logo_label)

        nombre_empresa = QLabel("Nombre de la Empresa")
        nombre_empresa.setAlignment(Qt.AlignCenter)
        nombre_empresa.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        menu_layout.addWidget(nombre_empresa)

    opciones = ["Dashboard", "Extracción", "Transformación", "Carga", "Datalake", "OCR", "Logs", "Configuración"]
    self.menu_list = QListWidget()
    self.menu_list.addItems(opciones)
    def show_datalake(self):
        from interface.views.datalake.datalake_view import DatalakeView
        self.limpiar_content()
        datalake_view = DatalakeView()
        self.content_layout.addWidget(datalake_view)
        self.menu_list.setStyleSheet("color: white; font-size: 16px; background: transparent; border: none;")
        menu_layout.addWidget(self.menu_list)
        menu_layout.addStretch()
        menu_frame.setLayout(menu_layout)

        # Panel principal (contenido) - ahora intercambiable
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(f"background-color: rgb({gris.red()}, {gris.green()}, {gris.blue()});")
        self.content_layout = QVBoxLayout()
        self.content_frame.setLayout(self.content_layout)

        # Vista por defecto: dashboard
        self.show_dashboard()

        # Agregar menú y contenido al layout principal
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(self.content_frame)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Conectar selección de menú
        self.menu_list.currentRowChanged.connect(self.cambiar_vista)

    def limpiar_content(self):
        # Elimina widgets actuales del content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def show_dashboard(self):
        self.limpiar_content()
        # Panel de bienvenida y resumen
        bienvenida = QLabel("Bienvenido al sistema ETL de la empresa")
        bienvenida.setFont(QFont("Arial", 20))
        bienvenida.setStyleSheet("color: #1e3c78; margin-top: 30px;")
        self.content_layout.addWidget(bienvenida)

        resumen = QLabel("""
        Este dashboard te permite gestionar y monitorear los procesos ETL:
        - Extraer datos desde diferentes fuentes (APIs, SQL Server, OCR, etc.)
        - Transformar y limpiar la información
        - Cargar los datos en destinos como SQL Server, Excel, CSV
        - Visualizar logs y estado de los procesos
        """)
        resumen.setFont(QFont("Arial", 12))
        resumen.setStyleSheet("color: #333; margin-top: 10px;")
        self.content_layout.addWidget(resumen)

        # Indicadores y estadísticas (KPIs)
        kpi_frame = QFrame()
        kpi_layout = QHBoxLayout()

        kpi1 = QLabel("<b>Última ejecución:</b><br>01/09/2025 18:30")
        kpi1.setAlignment(Qt.AlignCenter)
        kpi1.setStyleSheet("background: #e3eafc; border-radius: 10px; padding: 15px; font-size: 14px;")
        kpi2 = QLabel("<b>Datos procesados:</b><br>12,500 registros")
        kpi2.setAlignment(Qt.AlignCenter)
        kpi2.setStyleSheet("background: #e3eafc; border-radius: 10px; padding: 15px; font-size: 14px;")
        kpi3 = QLabel("<b>Errores recientes:</b><br>0")
        kpi3.setAlignment(Qt.AlignCenter)
        kpi3.setStyleSheet("background: #e3eafc; border-radius: 10px; padding: 15px; font-size: 14px;")
        kpi4 = QLabel("<b>Próxima ejecución:</b><br>03/09/2025 08:00")
        kpi4.setAlignment(Qt.AlignCenter)
        kpi4.setStyleSheet("background: #e3eafc; border-radius: 10px; padding: 15px; font-size: 14px;")

        kpi_layout.addWidget(kpi1)
        kpi_layout.addWidget(kpi2)
        kpi_layout.addWidget(kpi3)
        kpi_layout.addWidget(kpi4)
        kpi_frame.setLayout(kpi_layout)
        self.content_layout.addWidget(kpi_frame)

        # Botones de acción rápida
        acciones_frame = QFrame()
        acciones_layout = QHBoxLayout()

        btn_ejecutar_etl = QPushButton("Ejecutar ETL")
        btn_ejecutar_etl.setStyleSheet("background-color: #1e3c78; color: white; font-size: 16px; padding: 10px 30px; border-radius: 8px;")
        acciones_layout.addWidget(btn_ejecutar_etl)

        btn_subir_ocr = QPushButton("Subir archivo para OCR")
        btn_subir_ocr.setStyleSheet("background-color: #1e3c78; color: white; font-size: 16px; padding: 10px 30px; border-radius: 8px;")
        acciones_layout.addWidget(btn_subir_ocr)

        btn_exportar = QPushButton("Exportar resultados")
        btn_exportar.setStyleSheet("background-color: #1e3c78; color: white; font-size: 16px; padding: 10px 30px; border-radius: 8px;")
        acciones_layout.addWidget(btn_exportar)

        acciones_frame.setLayout(acciones_layout)
        self.content_layout.addWidget(acciones_frame)

        # Panel de notificaciones/logs recientes
        logs_frame = QFrame()
        logs_frame.setStyleSheet("background: #f5f5f5; border: 1px solid #d1d1d1; border-radius: 8px;")
        logs_layout = QVBoxLayout()
        logs_title = QLabel("Notificaciones y logs recientes")
        logs_title.setFont(QFont("Arial", 13, QFont.Bold))
        logs_title.setStyleSheet("color: #1e3c78; margin-bottom: 4px;")
        logs_layout.addWidget(logs_title)

        # Simulación de logs (luego se conectará a logs reales)
        self.logs_list = QListWidget()
        self.logs_list.addItem("[INFO] Proceso ETL ejecutado correctamente - 01/09/2025 18:30")
        self.logs_list.addItem("[WARNING] Archivo de entrada con datos incompletos - 01/09/2025 18:00")
        self.logs_list.addItem("[ERROR] Fallo conexión SQL Server - 31/08/2025 22:10")
        self.logs_list.setStyleSheet("background: #fff; font-size: 13px; border: none;")
        logs_layout.addWidget(self.logs_list)
        logs_frame.setLayout(logs_layout)

        self.content_layout.addWidget(logs_frame)
        self.content_layout.addStretch()

    def show_extraction(self):
        self.limpiar_content()
        extraction_view = ExtractionView(self.connection_manager)
        self.content_layout.addWidget(extraction_view)

    def cambiar_vista(self, index):
        if index == 0:
            self.show_dashboard()
        elif index == 1:
            self.show_extraction()
        elif index == 4:
            self.show_datalake()
        # Aquí se pueden agregar más elif para otras vistas


# Bloque principal para ejecutar la ventana
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
