import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QWidget,
    QVBoxLayout, QListWidget, QDialog, QFormLayout, QLineEdit
)
from PyQt5.QtCore import Qt


class CitySelectorDialog(QDialog):
    def __init__(self, parent=None):
        super(CitySelectorDialog, self).__init__(parent)
        self.setWindowTitle("Selecciona una Región")
        self.setGeometry(100, 100, 330, 200)

        self.layout = QVBoxLayout(self)

        self.city_list_widget = QListWidget(self)
        self.city_list_widget.addItems(["TV17-Urb. Las Quintanas 4ta. Etapa - Miraflores - Los J",
                                        "TV18-La Intendencia - El Molino",
                                        "TV19-Urb. Daniel Hoyle",
                                        "TV28-Urb. Santa Teresa del Avila",
                                        "TV41-Urb. Pay Pay - Leticia",
                                        "TV45-Urb. Huerta Grande - Barrio Ex Camal Municipal",
                                        "TV46-Urb. Las Quintanas 2da Etapa",
                                        "TV47-Urb. Las Quintanas 3ra. Etapa",
                                        "TV48-Urb. Las Quintanas 4ta Etapa - Parte Urb. Los Jard"
                                        ])  # Añadir ciudades aquí
        self.layout.addWidget(self.city_list_widget)

        self.city_list_widget.itemClicked.connect(self.select_city)

    def select_city(self, item):
        selected_city = item.text()
        self.accept()  # Cierra el diálogo
        self.parent().display_city(selected_city)


class InterGrafo(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(InterGrafo, self).__init__(*args, **kwargs)
        self.setWindowTitle("NexoBusiness")
        self.setGeometry(75, 40, 1210, 675)
        self.setWindowIcon(QIcon("Icono/icoPrincipal.png"))
        self.setStyleSheet("background-color: #f8f9fa;")
        self.init_ui()

    def init_ui(self):
        self.label_Valor1 = QLabel(self)
        self.label_Valor1.setGeometry(40, 27, 210, 15)
        self.label_Valor1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_Valor1.setStyleSheet("color:#343a40; font-size: 12px; font-weight: bold;")
        self.label_Valor1.setText("Selecciona tu región de interés")

        self.boton_Valor1 = QPushButton(self)
        self.boton_Valor1.setGeometry(80, 50, 80, 20)
        self.boton_Valor1.setText("SELECCIONAR")
        self.boton_Valor1.setStyleSheet("background-color: #0077B6 ; color: #FFFFFF;border-radius: 5px;")
        self.boton_Valor1.clicked.connect(self.open_city_selector)

        self.boton_RMapeo = QPushButton(self)
        self.boton_RMapeo.setGeometry(570, 180, 80, 20)
        self.boton_RMapeo.setText("Realizar mapeo")
        self.boton_RMapeo.setStyleSheet("background-color: #0077B6 ; color: #FFFFFF;border-radius: 5px;")

        self.SalidaGrafica = QWidget(self)
        self.SalidaGrafica.setGeometry(40, 210, 500, 400)
        self.SalidaGrafica.setStyleSheet("border: 1px solid black; background-color: #FFFFFF;border-radius: 10px;")

        self.SalidaMap = QWidget(self)
        self.SalidaMap.setGeometry(670, 210, 500, 400)
        self.SalidaMap.setStyleSheet("border: 1px solid black; background-color: #FFFFFF;border-radius: 10px;")

    def open_city_selector(self):
        dialog = CitySelectorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_city = dialog.city_list_widget.currentItem().text()
            self.display_city(selected_city)

    def display_city(self, city):
        # Aquí puedes actualizar la salida gráfica con la ciudad seleccionada.
        # Esto es solo un ejemplo de cómo podrías mostrar la ciudad seleccionada.
        label = QLabel(f"Ciudad Seleccionada: {city}", self.SalidaGrafica)
        label.setGeometry(10, 10, 480, 30)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold; color: #343a40;")
        label.show()


def main():
    app = QApplication(sys.argv)
    player = InterGrafo()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
