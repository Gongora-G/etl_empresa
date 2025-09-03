# Interfaz principal del software ETL usando PyQt5

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFrame, QPushButton, QListWidget
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
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

        opciones = ["Dashboard", "Extracción", "Transformación", "Carga", "OCR", "Logs", "Configuración"]
        self.menu_list = QListWidget()
        self.menu_list.addItems(opciones)
        self.menu_list.setStyleSheet("color: white; font-size: 16px; background: transparent; border: none;")
        menu_layout.addWidget(self.menu_list)
        menu_layout.addStretch()
        menu_frame.setLayout(menu_layout)

        # Panel principal (contenido)
        content_frame = QFrame()
        content_frame.setStyleSheet(f"background-color: rgb({gris.red()}, {gris.green()}, {gris.blue()});")
        content_layout = QVBoxLayout()

        # Panel de bienvenida y resumen
        bienvenida = QLabel("Bienvenido al sistema ETL de la empresa")
        bienvenida.setFont(QFont("Arial", 20))
        bienvenida.setStyleSheet("color: #1e3c78; margin-top: 30px;")
        content_layout.addWidget(bienvenida)

        resumen = QLabel("""
        Este dashboard te permite gestionar y monitorear los procesos ETL:
        - Extraer datos desde diferentes fuentes (APIs, SQL Server, OCR, etc.)
        - Transformar y limpiar la información
        - Cargar los datos en destinos como SQL Server, Excel, CSV
        - Visualizar logs y estado de los procesos
        """)
        resumen.setFont(QFont("Arial", 12))
        resumen.setStyleSheet("color: #333; margin-top: 10px;")
        content_layout.addWidget(resumen)

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
        content_layout.addWidget(kpi_frame)

        content_layout.addStretch()
        content_frame.setLayout(content_layout)

        # Agregar menú y contenido al layout principal
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(content_frame)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
