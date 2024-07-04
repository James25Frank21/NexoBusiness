import sys
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QWidget,
    QVBoxLayout, QListWidget, QDialog
)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx
from shapely.geometry import Polygon
import matplotlib

class CitySelectorDialog(QDialog):
    def __init__(self, parent=None):
        super(CitySelectorDialog, self).__init__(parent)
        self.setWindowTitle("Selecciona una Ciudad")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout(self)

        self.city_list_widget = QListWidget(self)
        self.city_list_widget.addItems([
            "TV17-Urb. Las Quintanas 4ta. Etapa - Miraflores - Los J",
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
        self.selected_city = None
        self.init_ui()

    def init_ui(self):

        self.image_label = QLabel(self)
        pixmap = QPixmap("imagenes/herramienta-de-seleccion.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(573, 350, 70, 70)
        self.image_label.setFixedSize(70, 70)

        self.image_label = QLabel(self)
        pixmap = QPixmap("imagenes/NN.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(567, 50, 90, 90)
        self.image_label.setFixedSize(90, 90)

        self.image_label = QLabel(self)
        pixmap = QPixmap("imagenes/pagina-web.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(210,80, 110, 110)
        self.image_label.setFixedSize(110, 110)

        self.image_label = QLabel(self)
        pixmap = QPixmap("imagenes/pastillas.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(860, 15, 180, 180)
        self.image_label.setFixedSize(180, 180)

        self.label_Valor1 = QLabel(self)
        self.label_Valor1.setGeometry(40, 27, 210, 15)
        self.label_Valor1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_Valor1.setStyleSheet("color:#343a40; font-size: 12px; font-weight: bold;")
        self.label_Valor1.setText("Selecciona tu región de interés")

        self.boton_Valor1 = QPushButton(self)
        self.boton_Valor1.setGeometry(80, 110, 80, 20)
        self.boton_Valor1.setText("SELECCIONAR")
        self.boton_Valor1.setStyleSheet("background-color: #0077B6 ; color: #FFFFFF;border-radius: 5px;")
        self.boton_Valor1.clicked.connect(self.open_city_selector)

        self.boton_RMapeo = QPushButton(self)
        self.boton_RMapeo.setGeometry(570, 180, 80, 20)
        self.boton_RMapeo.setText("Realizar mapeo")
        self.boton_RMapeo.setStyleSheet("background-color: #0077B6 ; color: #FFFFFF;border-radius: 5px;")
        self.boton_RMapeo.clicked.connect(self.generate_map)

        self.SalidaGrafica = QWidget(self)
        self.SalidaGrafica.setGeometry(40, 210, 500, 400)
        self.SalidaGrafica.setStyleSheet("border: 1px solid black; background-color: #87A1C3;border-radius: 10px;")

        self.SalidaMap = QWidget(self)
        self.SalidaMap.setGeometry(670, 210, 500, 400)
        self.SalidaMap.setStyleSheet("border: 1px solid black; background-color: #87A1C3;border-radius: 10px;")

        self.image_label = QLabel(self.SalidaGrafica)  # Label para mostrar la imagen
        self.image_label.setGeometry(10, 10, 480, 380)  # Ajustar según el tamaño del widget
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black; background-color: #406491;border-radius: 10px;")

        self.map_label = QLabel(self.SalidaMap)  # Label para mostrar la imagen del mapa
        self.map_label.setGeometry(10, 10, 480, 380)  # Ajustar según el tamaño del widget
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.map_label.setStyleSheet("border: 1px solid black; background-color: #406491;border-radius: 10px;")

    def open_city_selector(self):
        dialog = CitySelectorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_city = dialog.city_list_widget.currentItem().text()
            self.display_city(selected_city)

    def display_city(self, city):
        self.selected_city = city  # Guardar la ciudad seleccionada
        # Construir la ruta de la imagen
        image_path = f"imagenes/{city}.png"  # Ajustar el formato según el nombre y la extensión de las imágenes
        # Cargar y mostrar la imagen
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(470, 370, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.image_label.setText("Imagen no disponible")  # Mensaje en caso de error

    def generate_map(self):
        if self.selected_city:
            # Seleccionar la función de mapeo basada en la ciudad seleccionada
            if "TV41" in self.selected_city:
                self.generate_map41()
            elif "TV17" in self.selected_city:
                self.generate_map17()
            elif "TV18" in self.selected_city:
                self.generate_map18()
            elif "TV19" in self.selected_city:
                self.generate_map19()
            elif "TV28" in self.selected_city:
                self.generate_map28()
            elif "TV45" in self.selected_city:
                self.generate_map45()
            elif "TV46" in self.selected_city:
                self.generate_map46()
            elif "TV47" in self.selected_city:
                self.generate_map47()
            elif "TV48" in self.selected_city:
                self.generate_map48()

            else:
                self.map_label.setText("No se ha implementado el mapeo para esta ciudad.")
        else:
            self.map_label.setText("Por favor, selecciona una ciudad primero.")

    def generate_map17(self):
        # Implementar la lógica de mapeo específica para TV17
        coords = [(-79.01912100665638,-8.095066311845741),
                    (-79.01987850906093,-8.09476531391747),
                    (-79.02067324396154,-8.094478713635453),
                    (-79.0205819062326,-8.09423585092365),
                    (-79.02053369130088,-8.094113915430542),
                    (-79.02047580131392,-8.093953161095818),
                    (-79.02072083641471,-8.093924513832036),
                    (-79.02091600519384,-8.093899945178656),
                    (-79.02111117397297,-8.093875376525276),
                    (-79.02123173385777,-8.093839660666625),
                    (-79.02127183802291,-8.093824110450328),
                    (-79.02134947546827,-8.093790249323305),
                    (-79.0214210300243,-8.093764575450773),
                    (-79.0214293291575,-8.093756011833468),
                    (-79.02145219136307,-8.093746052924729),
                    (-79.02148288292521,-8.093741018216084),
                    (-79.02152171677605,-8.093723507245642),
                    (-79.02154489040068,-8.09371267035384),
                    (-79.02155538005914,-8.093713460890672),
                    (-79.02161190781777,-8.093695647542539),
                    (-79.02169441575737,-8.0936633687691),
                    (-79.02184917938423,-8.093606110101263),
                    (-79.02191923455588,-8.093580043634063),
                    (-79.02202907343514,-8.093545645789582),
                    (-79.0220794632344,-8.093611094533316),
                    (-79.0221203728451,-8.093728076103929),
                    (-79.02221954779651,-8.093990399131357),
                    (-79.02234682887317,-8.094329697037622),
                    (-79.02242846154887,-8.094568097559431),
                    (-79.02215112837486,-8.09466957207664),
                    (-79.02198347406753,-8.094734450951862),
                    (-79.02200268416871,-8.094794968872066),
                    (-79.02206314996711,-8.094958127775726),
                    (-79.02218194767555,-8.095283612946474),
                    (-79.02242269616784,-8.095915853243525),
                    (-79.02258108621179,-8.09633105253478),
                    (-79.02274789101317,-8.096768142370173),
                    (-79.02289392297511,-8.096977169908726),
                    (-79.02266614643214,-8.097095655169419),
                    (-79.02247696521283,-8.097186183672273),
                    (-79.02237495336846,-8.097243332961995),
                    (-79.02257957575178,-8.097473954927981),
                    (-79.02262969279884,-8.097515849771096),
                    (-79.02301907975283,-8.097203773257391),
                    (-79.02378286817614,-8.097976175501927),
                    (-79.0263904778917,-8.10068195538328),
                    (-79.02632535037996,-8.100744646563054),
                    (-79.0262540664271,-8.100812822411463),
                    (-79.02609443894843,-8.100969236941964),
                    (-79.02596095580455,-8.101101770515037),
                    (-79.02581329476779,-8.10123559335976),
                    (-79.02575803010015,-8.101164320949863),
                    (-79.02571561578712,-8.101109678876568),
                    (-79.02554104256089,-8.100890881983444),
                    (-79.02540559840595,-8.100733043649807),
                    (-79.02533814799554,-8.10064788809078),
                    (-79.02527793654147,-8.100545821114505),
                    (-79.02501876513979,-8.100238344161326),
                    (-79.02477182253524,-8.099948708871013),
                    (-79.02459172406284,-8.09973554585919),
                    (-79.02442385438819,-8.099536401286553),
                    (-79.02425961160115,-8.099333419657038),
                    (-79.02373225075453,-8.0997567178831),
                    (-79.02347500654001,-8.099964543786664),
                    (-79.02324286354091,-8.100147518892129),
                    (-79.02361663315239,-8.100579203367905),
                    (-79.02380351795816,-8.100792969042615),
                    (-79.02390010660777,-8.100904005018547),
                    (-79.02403235272408,-8.101054495775156),
                    (-79.02383252990344,-8.101178101275567),
                    (-79.02333445503653,-8.101470858669519),
                    (-79.02308751510111,-8.101617237362019),
                    (-79.02285211140519,-8.101758424636678),
                    (-79.02275492712172,-8.10181046936006),
                    (-79.02273338322932,-8.101827908338691),
                    (-79.02270449809353,-8.101793433236224),
                    (-79.02232528923133,-8.101321916163315),
                    (-79.02195227917838,-8.10084579638007),
                    (-79.02180102987933,-8.10064455823914),
                    (-79.02170316659063,-8.100483975218012),
                    (-79.02164946981745,-8.100398569936672),
                    (-79.02160080957607,-8.100318150928551),
                    (-79.02150643311805,-8.100166389689406),
                    (-79.02138888984375,-8.099977041930671),
                    (-79.02123083353545,-8.099723477506757),
                    (-79.02177399362986,-8.099455315851195),
                    (-79.02215279645469,-8.100062422775498),
                    (-79.02260973382245,-8.099764546554022),
                    (-79.02257532456613,-8.099711703576162),
                    (-79.02227520374664,-8.099212289813707),
                    (-79.0229192957752,-8.098897005408745),
                    (-79.02295174244843,-8.098884493493841),
                    (-79.02294423421006,-8.098868767894176),
                    (-79.02121481699021,-8.099701012684296),
                    (-79.02098662386729,-8.099305249269115),
                    (-79.02084658706946,-8.099059424112244),
                    (-79.02072195004851,-8.098792275406662),
                    (-79.02071142107675,-8.098766109405013),
                    (-79.02066798495581,-8.098667892814156),
                    (-79.02061241582982,-8.098544211238623),
                    (-79.02057194639636,-8.098447943857455),
                    (-79.02049868458224,-8.098288203414798),
                    (-79.02042905545319,-8.09812309149195),
                    (-79.02032589534682,-8.097893185321812),
                    (-79.02023627832963,-8.097698018848888),
                    (-79.01968352796763,-8.096447185685193),
                    (-79.01953892802067,-8.096114684505714),
                    (-79.01939805132241,-8.095776654118183),
                    (-79.01926920404424,-8.095448706507476),
                    (-79.01919478783917,-8.095273712073624),
                    (-79.01915095996209,-8.095174793132758),
                    (-79.01912100665638,-8.095066311845741)
            # Coordenadas para TV17
        ]
        self.create_map(coords)

    def generate_map18(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [(-79.01411185542368,-8.09946438011707),
                    (-79.01440410473651,-8.099195353202633),
                    (-79.01465027516097,-8.098983983253962),
                    (-79.01503382153479,-8.098646991665223),
                    (-79.01601956990474,-8.097810404402956),
                    (-79.01696355399052,-8.097026925402854),
                    (-79.0178819638481,-8.096239807002092),
                    (-79.01801276207394,-8.096153258301005),
                    (-79.01814837169745,-8.096283954894567),
                    (-79.01819872294838,-8.096369040292098),
                    (-79.01820396976062,-8.096482437596773),
                    (-79.01819625869518,-8.096711453830139),
                    (-79.01885805487078,-8.096540120191477),
                    (-79.01963655067327,-8.096348202106682),
                    (-79.01988744799006,-8.096909168834884),
                    (-79.02002671648461,-8.09724152422342),
                    (-79.0201918708702,-8.097607935990037),
                    (-79.02026982588853,-8.097797457592224),
                    (-79.02037557094468,-8.098042005043759),
                    (-79.02052684799953,-8.09838482404422),
                    (-79.02067812505484,-8.09873550381991),
                    (-79.02075677793515,-8.098928545964203),
                    (-79.02083476095852,-8.099111074618868),
                    (-79.02104037664,-8.099471732864686),
                    (-79.02123106795031,-8.099805775766775),
                    (-79.0214475397274,-8.100160465413353),
                    (-79.02172453717297,-8.10058350975379),
                    (-79.02187798483662,-8.10078658090869),
                    (-79.02200426318277,-8.100945140026937),
                    (-79.02230866660251,-8.101333805523112),
                    (-79.0224549378713,-8.101516371455986),
                    (-79.0226448300651,-8.101747379689371),
                    (-79.02292085031708,-8.102092843212553),
                    (-79.02253011010612,-8.102405650835845),
                    (-79.02219097996567,-8.102690945818281),
                    (-79.0224259900947,-8.102960475537934),
                    (-79.02326462354104,-8.102480469866943),
                    (-79.0236124442217,-8.102894701914506),
                    (-79.02383399462653,-8.10316470383679),
                    (-79.0238931597589,-8.103228958160482),
                    (-79.02394041487518,-8.103289282118965),
                    (-79.02463818181513,-8.10415619212538),
                    (-79.02356607529882,-8.104847782845466),
                    (-79.02362265813666,-8.104916192971455),
                    (-79.02365412668485,-8.10495295116096),
                    (-79.02366642025977,-8.104991898539852),
                    (-79.02366346532537,-8.105020948425388),
                    (-79.0236619158812,-8.105037957925592),
                    (-79.02365847483229,-8.105064854673593),
                    (-79.0236403861149,-8.105106281477447),
                    (-79.02362790084288,-8.105161847474443),
                    (-79.02362457719103,-8.105179314406751),
                    (-79.0236241704251,-8.105209635747254),
                    (-79.02362088603304,-8.105282652292985),
                    (-79.02369284875832,-8.105376249465856),
                    (-79.02376072777686,-8.105440051165377),
                    (-79.02378674801608,-8.105463994958145),
                    (-79.0238133423041,-8.105484338649404),
                    (-79.02386019453546,-8.105490518622222),
                    (-79.02387972076023,-8.105491160111098),
                    (-79.02390248068541,-8.105493014534737),
                    (-79.023916845114,-8.105493770484314),
                    (-79.02395729060805,-8.105494613441582),
                    (-79.02399495495516,-8.105491096529487),
                    (-79.02402573874352,-8.105483806688229),
                    (-79.02410046205429,-8.105563816460137),
                    (-79.02416223000662,-8.105636241137962),
                    (-79.02413532768247,-8.105655305879939),
                    (-79.02404189239155,-8.105712874350877),
                    (-79.02391281253495,-8.105793911957285),
                    (-79.02382239454933,-8.105848862556826),
                    (-79.0238060710859,-8.105860198479576),
                    (-79.0236440672697,-8.106003949358751),
                    (-79.02346171382267,-8.10616204516458),
                    (-79.02332946357977,-8.106276951346906),
                    (-79.02318734624536,-8.106401969504972),
                    (-79.02311378007548,-8.106466797083474),
                    (-79.02303715229752,-8.106535125483283),
                    (-79.02288007698961,-8.10667007406586),
                    (-79.02281284224809,-8.106727198624101),
                    (-79.02272638051524,-8.106803355635979),
                    (-79.02256428348466,-8.106941986068911),
                    (-79.02249446772106,-8.10700262760489),
                    (-79.02242465195748,-8.10706326914087),
                    (-79.02226404358619,-8.107202522642183),
                    (-79.02196983650873,-8.106948206949692),
                    (-79.02169298189939,-8.106698096626866),
                    (-79.02145986588215,-8.106483564601938),
                    (-79.0212011113591,-8.106244999611935),
                    (-79.02068884687455,-8.105763336045994),
                    (-79.02019861033565,-8.105290533233777),
                    (-79.01920642715217,-8.104340927742019),
                    (-79.01827332649853,-8.103454448277105),
                    (-79.01806758978651,-8.103253834708884),
                    (-79.0179199766466,-8.103111583274673),
                    (-79.01775822903832,-8.10296117726245),
                    (-79.01746334947171,-8.102678697181968),
                    (-79.01721128302304,-8.10243611113276),
                    (-79.01695783339918,-8.102194389152963),
                    (-79.01682561662624,-8.102062937032077),
                    (-79.01670448948153,-8.101949586056435),
                    (-79.01643682955336,-8.101690760426955),
                    (-79.01630032742767,-8.101561626972522),
                    (-79.01616587652839,-8.101429709844922),
                    (-79.01513605441887,-8.100446556561991),
                    (-79.01411185542368,-8.09946438011707)
            # Coordenadas para TV18
        ]
        self.create_map(coords)
    def generate_map19(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [  (-79.01511223257472, -8.09414657649485),
                    (-79.0163078080012, -8.097563651672104),
                    (-79.0131314311732, -8.100242089290077),
                    (-79.01089617196367, -8.096820054710562),
                    (-79.01511223257472, -8.09414657649485)
            # Coordenadas para TV18
        ]
        self.create_map(coords)
    def generate_map28(self):

        coords = [(-79.01838345276639, -8.093289700112905),
                  (-79.01809740887687, -8.092625445237218),
                  (-79.01675176942162, -8.093116570365973),
                  (-79.01510804557242, -8.094127971536853),
                  (-79.01458987008267, -8.093046757296118),
                  (-79.01401546606445, -8.091985786118533),
                  (-79.01301949976538, -8.090124638103102),
                  (-79.01218319252673, -8.088571076271162),
                  (-79.01147135861918, -8.087270324188257),
                  (-79.01097487344553, -8.086512942137201),
                  (-79.0115350788748, -8.086168054232242),
                  (-79.01354094443488, -8.085874767778808),
                  (-79.0145008606852, -8.085687237238325),
                  (-79.01516766775404, -8.085684735397319),
                  (-79.01568082595959, -8.085727321287484),
                  (-79.01623586969757, -8.085943391719994),
                  (-79.01649344542737, -8.086086008618938),
                  (-79.0168053993752, -8.086387727013694),
                  (-79.0171363335315, -8.0866612113662),
                  (-79.01751542642103, -8.086955267199652),
                  (-79.01768788396043, -8.087176906888088),
                  (-79.01823505279674, -8.08747611579659),
                  (-79.01871075019693, -8.08768419634113),
                  (-79.01909011846925, -8.087977217041512),
                  (-79.01970378506356, -8.088398933103976),
                  (-79.01985777600429, -8.088433886525483),
                  (-79.02002555405883, -8.088421695840328),
                  (-79.02027596105077, -8.088393586601786),
                  (-79.02074552811938, -8.088450394034137),
                  (-79.02123002708036, -8.08842496661615),
                  (-79.02164123098227, -8.088347116812479),
                  (-79.02188824840275, -8.08833166417481),
                  (-79.022055026813, -8.088389757487441),
                  (-79.02225737384104, -8.08850009063545),
                  (-79.02240288759954, -8.088611222091282),
                  (-79.02253115129078, -8.088776689718134),
                  (-79.02266042288396, -8.088905733662411),
                  (-79.02287746785323, -8.0890390687005),
                  (-79.0232038740008, -8.08922554241883),
                  (-79.02332226877354, -8.089240701310146),
                  (-79.02343380234215, -8.089226229492851),
                  (-79.02367274456988, -8.089121908167158),
                  (-79.02380601510959, -8.089252008183577),
                  (-79.02387909021434, -8.089372984409874),
                  (-79.02394517934874, -8.08955037564997),
                  (-79.02406546560336, -8.089939705534618),
                  (-79.02429292791695, -8.090696797673898),
                  (-79.02470121567737, -8.092221994873757),
                  (-79.02489207604206, -8.093096380222569),
                  (-79.02483939705722, -8.093269372532534),
                  (-79.02482808671533, -8.093753307129813),
                  (-79.02448647407095, -8.093766523589466),
                  (-79.02415322937162, -8.093824339877175),
                  (-79.02372891904936, -8.093955714185352),
                  (-79.02323560098672, -8.094150348039001),
                  (-79.02280583419112, -8.094319445612895),
                  (-79.02272953845745, -8.094162399050695),
                  (-79.02264856034053, -8.094019274735578),
                  (-79.02259044749543, -8.093916092748717),
                  (-79.02251760247063, -8.093796093789159),
                  (-79.02242051909602, -8.093704608749059),
                  (-79.02226382750423, -8.093636780770975),
                  (-79.02203917363023, -8.093595344152789),
                  (-79.02165826669383, -8.093729143142639),
                  (-79.02150804666422, -8.093787050351487),
                  (-79.02123626031955, -8.093898911232571),
                  (-79.0209870509375, -8.093943958401447),
                  (-79.0205087132268, -8.09400358034478),
                  (-79.02000291939027, -8.094089156850757),
                  (-79.01958798725589, -8.094132833941394),
                  (-79.0188356839464, -8.094421957946636),
                  (-79.01861949008943, -8.093872938843916),
                  (-79.01838345276639, -8.093289700112905)
            # Coordenadas para TV18
        ]
        self.create_map(coords)

    def generate_map41(self):
        coords = [
            (-79.0151259444519, -8.094155038637439),
            (-79.01633631662568, -8.09340538193321),
            (-79.01678234963278, -8.093136955114545),
            (-79.01788547066866, -8.096006984784871),
            (-79.0179714885527, -8.096133895127238),
            (-79.01785769437251, -8.096253254275524),
            (-79.01769553788094, -8.09638558542018),
            (-79.01754634118511, -8.0964925755464),
            (-79.01741477204845, -8.096626427675755),
            (-79.01719907450445, -8.09683041144221),
            (-79.01694462975787, -8.097037344235794),
            (-79.01629999216684, -8.097610828641692),
            (-79.0151259444519, -8.094155038637439)
        ]
        self.create_map(coords)
    def generate_map45(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [(-79.02812634447947,-8.102700486407741),
                    (-79.03018222939745,-8.10508956738758),
                    (-79.02894966887872,-8.10628425824892),
                    (-79.02634436222745,-8.10516820827857),
                    (-79.02558948835615,-8.10525662391018),
                    (-79.02385293112332,-8.103142056666826),
                    (-79.02638273315013,-8.100675110422785),
                    (-79.02812634447947,-8.102700486407741)
            # Coordenadas para TV18
        ]
        self.create_map(coords)

    def generate_map46(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [(-79.02967907601375,-8.097575432787522),
                    (-79.03023489829373,-8.098132066295676),
                    (-79.03056415862594,-8.098503765994039),
                    (-79.03070131987103,-8.098694235540677),
                    (-79.0315002773592,-8.100208464537687),
                    (-79.03081411212209,-8.100555130267011),
                    (-79.03058355674416,-8.100716394033228),
                    (-79.03007678084344,-8.101100617481094),
                    (-79.02873183939023,-8.102230682366894),
                    (-79.02813528824417,-8.102716643033261),
                    (-79.02717406897355,-8.101559576726018),
                    (-79.02645470856541,-8.100698751583835),
                    (-79.02734284384393,-8.099852529383526),
                    (-79.02842974591267,-8.098808300268274),
                    (-79.02911238644089,-8.09814091243544),
                    (-79.02967907601375,-8.097575432787522)
            # Coordenadas para TV18
        ]
        self.create_map(coords)
    def generate_map47(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [(-79.02725085012166,-8.095083054998042),
                    (-79.02964003616653,-8.09754911854958),
                    (-79.02890440243083,-8.098273947449744),
                    (-79.02808564036778,-8.099064848290304),
                    (-79.0264198785494,-8.10066328473576),
                    (-79.0251804551497,-8.09939659870303),
                    (-79.02399264893613,-8.098180150566293),
                    (-79.025574687058,-8.096681538333428),
                    (-79.02725085012166,-8.095083054998042)
            # Coordenadas para TV18
        ]
        self.create_map(coords)
    def generate_map48(self):
        # Implementar la lógica de mapeo específica para TV18
        coords = [(-79.02723940212891,-8.095099526591639),
                    (-79.02559190965756,-8.0966459529295),
                    (-79.02399696075506,-8.098170615281632),
                    (-79.02363407716834,-8.097812758921457),
                    (-79.02328667159557,-8.09746767229943),
                    (-79.02308743106367,-8.097278331608987),
                    (-79.02289270495315,-8.097080690574082),
                    (-79.02280928806478,-8.097004187286283),
                    (-79.02274779836273,-8.096913637257824),
                    (-79.02267956509442,-8.096812803373963),
                    (-79.02263067934402,-8.096711969490698),
                    (-79.02186384729194,-8.094676906144315),
                    (-79.02212945013643,-8.094586553051421),
                    (-79.02241138455602,-8.094469251854449),
                    (-79.02295892182009,-8.094261597564582),
                    (-79.02356471145414,-8.094020721942897),
                    (-79.0238758194817,-8.093910750006437),
                    (-79.02418324342034,-8.093833604583438),
                    (-79.02434974743609,-8.093803887731442),
                    (-79.02451714584545,-8.093775941847614),
                    (-79.02482332208781,-8.093762553305517),
                    (-79.02498936441764,-8.093768709794135),
                    (-79.02524931801074,-8.093797888863445),
                    (-79.02549375215833,-8.093856247000986),
                    (-79.02570640949821,-8.0939204555393),
                    (-79.02596915284532,-8.094034251156689),
                    (-79.02627035509057,-8.094190549958823),
                    (-79.02644097596036,-8.094314971371837),
                    (-79.02660884495407,-8.094455829676876),
                    (-79.02677939712653,-8.094625023443069),
                    (-79.02723940212891,-8.095099526591639)
            # Coordenadas para TV18
        ]
        self.create_map(coords)


    def create_map(self, coords):
        polygon = Polygon(coords)
        centroid = polygon.centroid
        centroid_coords = (centroid.x, centroid.y)

        graph = ox.graph_from_polygon(
            polygon,
            network_type='drive',
            simplify=True,
            retain_all=False,
            truncate_by_edge=False,
            clean_periphery=None,
            custom_filter=None
        )
        # Convertir el grafo a no dirigido si es dirigido
        if nx.is_directed(graph):
            graph = graph.to_undirected()

        # Encontrar las componentes conexas del grafo
        components = list(nx.connected_components(graph))

        # Elegir la componente conexa más grande
        largest_component = max(components, key=len)

        # Crear un nuevo grafo con la componente conexa más grande
        subgraph = graph.subgraph(largest_component).copy()

        # Asegurar que el grafo es conexo
        if not nx.is_connected(subgraph):
            raise ValueError("El grafo aún no es conexo.")

        # Cálculo del centro del grafo
        center_node = nx.center(subgraph)[0]
        center_coords = (subgraph.nodes[center_node]['x'], subgraph.nodes[center_node]['y'])

        # Cálculo del centro absoluto y la mediana absoluta del grafo
        def absolute_centre(graph):
            all_pairs_shortest_path_length = dict(nx.all_pairs_dijkstra_path_length(graph))
            abs_centre_node = min(all_pairs_shortest_path_length,
                                  key=lambda n: max(all_pairs_shortest_path_length[n].values()))
            return abs_centre_node

        def absolute_median(graph):
            all_pairs_shortest_path_length = dict(nx.all_pairs_dijkstra_path_length(graph))
            abs_median_node = min(all_pairs_shortest_path_length,
                                  key=lambda n: sum(all_pairs_shortest_path_length[n].values()))
            return abs_median_node

        abs_centre_node = absolute_centre(subgraph)
        abs_centre_coords = (subgraph.nodes[abs_centre_node]['x'], subgraph.nodes[abs_centre_node]['y'])

        abs_median_node = absolute_median(subgraph)
        abs_median_coords = (subgraph.nodes[abs_median_node]['x'], subgraph.nodes[abs_median_node]['y'])

        fig, ax = ox.plot_graph(subgraph, show=False, close=False)

        # Marcamos el centro del grafo
        ax.plot(center_coords[0], center_coords[1], marker='o', color='blue', markersize=10, label='Centro del Grafo')

        # Marcamos la mediana del grafo
        ax.plot(abs_median_coords[0], abs_median_coords[1], marker='x', color='green', markersize=10,
                label='Mediana del Grafo')

        # Marcamos el centro absoluto del grafo
        ax.plot(abs_centre_coords[0], abs_centre_coords[1], marker='o', color='purple', markersize=10,
                label='Centro Absoluto del Grafo')

        # Marcamos la mediana absoluta del grafo
        ax.plot(abs_median_coords[0], abs_median_coords[1], marker='x', color='orange', markersize=10,
                label='Mediana Absoluta del Grafo')

        # Marcamos el centroide del polígono
        ax.plot(centroid.x, centroid.y, marker='o', color='red', markersize=10, label='Centroide del Polígono')

        plt.legend()

        # Guardar el gráfico en un archivo temporal
        temp_image_path = "temp_map.png"
        fig.savefig(temp_image_path)
        plt.close(fig)

        # Cargar y mostrar la imagen en el widget
        pixmap = QPixmap(temp_image_path)
        if not pixmap.isNull():
            self.map_label.setPixmap(pixmap.scaled(580, 480, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.map_label.setText("Imagen no disponible")  # Mensaje en caso de error

def main():
    app = QApplication(sys.argv)
    player = InterGrafo()
    player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
