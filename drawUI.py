from PyQt5 import QtCore, QtGui, QtWidgets

IMG_SIZE_X = 255
IMG_SIZE_Y = 189
H_TEXT_AREA = 30

class Ui_DrawArea(object):
    def setupUi(self, MainWindow, img_1, img_2):
        MainWindow.setObjectName("Draw Line")
        MainWindow.setFixedSize(IMG_SIZE_X * 2,  IMG_SIZE_Y + H_TEXT_AREA)
        MainWindow.setWindowTitle("Hw2")
        # 
        self.info_board = QtWidgets.QLabel(MainWindow)
        self.info_board.setGeometry(10, IMG_SIZE_Y, IMG_SIZE_X * 2, H_TEXT_AREA)
        self.info_board.setText("Draw a line on the left image")
        #
        self.img_1 = QtWidgets.QLabel(MainWindow)
        # self.img_1 = IMG(MainWindow)
        self.img_1.setPixmap(img_1)
        self.img_1.setGeometry(0, 0, IMG_SIZE_X, IMG_SIZE_Y)

        # self.img_2 = IMG(MainWindow)
        self.img_2 = QtWidgets.QLabel(MainWindow)
        self.img_2.setPixmap(img_2)
        self.img_2.setGeometry(IMG_SIZE_X, 0, IMG_SIZE_X, IMG_SIZE_Y)

class IMG(QtWidgets.QLabel, QtGui.QMouseEvent):
    def __init__(self, parent):
        super(IMG, self).__init__(parent)

    def paintEvent(self, ev: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter()
        painter.setPen(
            QtGui.QPen(QtCore.Qt.red, 3, QtCore.Qt.SolidLine)
        )

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        print("pressed")

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        print("released")

        