import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt



class InterGrafo(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(InterGrafo, self).__init__(*args, **kwargs)
        self.setWindowTitle("Logistik Nexus")
        self.setGeometry(75, 40, 1210, 675)
        self.setWindowIcon(QIcon("Icono/icoPrincipal.png"))
        self.setStyleSheet("background-color: #F7F7F7;")
        self.init_ui()

    def init_ui(self):

        self.label_Valor1 = QLabel(self)
        self.label_Valor1.setGeometry(40, 27, 180, 15)
        self.label_Valor1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_Valor1.setText("Seleccionar región de interés")

        self.valor4Y_input = QLineEdit(self)
        self.valor4Y_input.setGeometry(290, 175, 40, 20)


        self.SalidaGrafica = QWidget(self)
        self.SalidaGrafica.setGeometry(415, 10, 380, 290)
        self.SalidaGrafica.setStyleSheet("border: 1px solid black; background-color: #7FFF00;")

        layout = QVBoxLayout(self.SalidaGrafica)
        self.SalidaGrafica.setLayout(layout)

        self.linea = QLabel(self)
        self.linea.setGeometry(20, 320, 1170, 1)
        self.linea.setStyleSheet("background-color: red;")

        self.SalidaMap = QWidget(self)
        self.SalidaMap.setGeometry(20, 370, 380, 290)
        self.SalidaMap.setStyleSheet("border: 1px solid black; background-color: #7FFF00;")

        layout1 = QVBoxLayout(self.SalidaMap)
        self.SalidaMap.setLayout(layout1)




def main():
    app = QApplication(sys.argv)
    player = InterGrafo()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
