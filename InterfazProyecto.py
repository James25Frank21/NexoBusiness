import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt



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
        #color del borde
        self.boton_Valor1.setStyleSheet("background-color: #0077B6 ; color: #FFFFFF;border-radius: 5px;")


        self.SalidaGrafica = QWidget(self)
        self.SalidaGrafica.setGeometry(40, 210, 500, 400)
        self.SalidaGrafica.setStyleSheet("border: 1px solid black; background-color: #FFFFFF;border-radius: 10px;")


        self.SalidaMap = QWidget(self)
        self.SalidaMap.setGeometry(670, 210, 500, 400)
        self.SalidaMap.setStyleSheet("border: 1px solid black; background-color: #FFFFFF;border-radius: 10px;")



def main():
    app = QApplication(sys.argv)
    player = InterGrafo()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
