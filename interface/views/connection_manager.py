import configparser
import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QFormLayout, QHBoxLayout, QListWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config.ini')

class ConnectionManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestor de Conexiones de Datos")
        layout = QVBoxLayout()
        self.config = configparser.ConfigParser()
        self.load_config()
        title = QLabel("Gestor de Conexiones")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1e3c78;")
        layout.addWidget(title)
        self.connection_list = QListWidget()
        self.connection_list.addItems(self.config.sections())
        layout.addWidget(self.connection_list)
        # Widget de campos personalizados
        self.fields_layout = QVBoxLayout()
        layout.addLayout(self.fields_layout)
        self.btn_add_field = QPushButton("Agregar campo")
        layout.addWidget(self.btn_add_field)
        self.btn_new = QPushButton("Nueva conexión")
        self.btn_save = QPushButton("Guardar conexión")
        self.btn_delete = QPushButton("Eliminar conexión")
        btns = QHBoxLayout()
        btns.addWidget(self.btn_new)
        btns.addWidget(self.btn_save)
        btns.addWidget(self.btn_delete)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.connection_list.currentTextChanged.connect(self.load_connection)
        self.btn_new.clicked.connect(self.new_connection)
        self.btn_save.clicked.connect(self.save_connection)
        self.btn_delete.clicked.connect(self.delete_connection)
        self.btn_add_field.clicked.connect(self.add_field)
        if self.config.sections():
            self.load_connection(self.config.sections()[0])

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            self.config.read(CONFIG_PATH)

    def load_connection(self, section):
        if section not in self.config:
            return
        params = self.config[section]
        self.clear_fields()
        for key in params:
            if not key.endswith('_type'):  # Solo cargar campos, no tipos
                self.add_field(key, params[key])

    def new_connection(self):
        name, ok = QInputDialog.getText(self, "Nueva conexión", "Nombre de la conexión:")
        if ok and name:
            self.config.add_section(name)
            self.connection_list.addItem(name)
            items = self.connection_list.findItems(name, Qt.MatchExactly)
            if items:
                self.connection_list.setCurrentItem(items[0])
            self.clear_fields()

    def add_field(self, key=None, value=None, field_type=None):
        if key is None or isinstance(key, bool):
            key, ok = QInputDialog.getText(self, "Agregar campo", "Nombre del campo:")
            if not ok or not key or isinstance(key, bool):
                return
        if value is None:
            value = ''
        # Selección de tipo de campo
        type_combo = QComboBox()
        type_combo.addItems(["Texto", "Número", "Token/Clave", "URL", "Otro"])
        if field_type:
            idx = type_combo.findText(field_type)
            if idx >= 0:
                type_combo.setCurrentIndex(idx)
        field_layout = QHBoxLayout()
        key_input = QLineEdit(key)
        value_input = QLineEdit(value)
        btn_remove = QPushButton("X")
        btn_remove.setFixedWidth(28)
        btn_remove.setStyleSheet("color: red; font-weight: bold;")
        field_layout.addWidget(QLabel("Nombre:"))
        field_layout.addWidget(key_input)
        field_layout.addWidget(QLabel("Valor:"))
        field_layout.addWidget(value_input)
        field_layout.addWidget(QLabel("Tipo:"))
        field_layout.addWidget(type_combo)
        field_layout.addWidget(btn_remove)
        self.fields_layout.addLayout(field_layout)
        def remove():
            for i in reversed(range(field_layout.count())):
                widget = field_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.fields_layout.removeItem(field_layout)
        btn_remove.clicked.connect(remove)

    def clear_fields(self):
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.layout():
                layout = item.layout()
                while layout.count():
                    widget = layout.takeAt(0).widget()
                    if widget:
                        widget.setParent(None)

    def save_connection(self):
        section = self.connection_list.currentItem().text()
        self.config[section] = {}
        for i in range(self.fields_layout.count()):
            layout = self.fields_layout.itemAt(i).layout()
            if layout:
                key = layout.itemAt(1).widget().text()
                value = layout.itemAt(3).widget().text()
                field_type = layout.itemAt(5).widget().currentText()
                if key:
                    self.config[section][key] = value
                    self.config[section][f"{key}_type"] = field_type
        with open(CONFIG_PATH, 'w') as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Guardado", f"Conexión '{section}' guardada correctamente.")
        if self.parent() and hasattr(self.parent(), 'actualizar_conexiones'):
            self.parent().actualizar_conexiones()

    def delete_connection(self):
        section = self.connection_list.currentItem().text()
        self.config.remove_section(section)
        self.connection_list.takeItem(self.connection_list.currentRow())
        with open(CONFIG_PATH, 'w') as configfile:
            self.config.write(configfile)
        QMessageBox.information(self, "Eliminado", f"Conexión '{section}' eliminada.")
        if self.parent() and hasattr(self.parent(), 'actualizar_conexiones'):
            self.parent().actualizar_conexiones()
