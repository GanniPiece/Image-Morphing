from PyQt5 import QtCore, QtGui, QtWidgets

IMG_SIZE_X = 255
IMG_SIZE_Y = 189

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(IMG_SIZE_X * 5,  IMG_SIZE_Y * 3)
        MainWindow.setWindowTitle("Hw2 Image Morphing")
        # 
        self.img_1 = QtWidgets.QLabel(MainWindow)
        self.img_1.setGeometry(0, 0, IMG_SIZE_X, IMG_SIZE_Y)
        self.img_1.setPixmap(
            QtGui.QPixmap("images/cheetah.jpg")
        )
        self.img_1_warping = QtWidgets.QLabel(MainWindow)
        self.img_1_warping.setGeometry(0, IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)
        self.img_1_draw = QtWidgets.QLabel(MainWindow)
        self.img_1_draw.setGeometry(0, 0, IMG_SIZE_X, IMG_SIZE_Y)


        self.img_morphing = QtWidgets.QLabel(MainWindow)
        self.img_morphing.setGeometry(IMG_SIZE_X * 2, 0, IMG_SIZE_X, IMG_SIZE_Y)
        # 
        self.img_2 = QtWidgets.QLabel(MainWindow)
        self.img_2.setGeometry(IMG_SIZE_X * 4, 0, IMG_SIZE_X, IMG_SIZE_Y)
        self.img_2.setPixmap(
            QtGui.QPixmap("images/women.jpg")
        )
        self.img_2_warping = QtWidgets.QLabel(MainWindow)
        self.img_2_warping.setGeometry(IMG_SIZE_X * 4, IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)

        self.img_2_draw = QtWidgets.QLabel(MainWindow)
        self.img_2_draw.setGeometry(IMG_SIZE_X * 4, 0, IMG_SIZE_X, IMG_SIZE_Y)
        # Configuration
        # t slider
        self.slider_time = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider_time.setGeometry(3/2*IMG_SIZE_X, IMG_SIZE_Y + 10, IMG_SIZE_X * 2, 30)
        self.slider_time.setMinimum(0)
        self.slider_time.setMaximum(100)
        self.slider_time.setSingleStep(1)
        self.slider_time.setValue(50)
        
        self.label_time = QtWidgets.QLabel(MainWindow)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setGeometry(IMG_SIZE_X+10, IMG_SIZE_Y, IMG_SIZE_X / 2, 40)
        self.label_time.setText(f"t = 0.5")
        # Warping
        self.btn_warping = QtWidgets.QPushButton(MainWindow)
        self.btn_warping.setText("Warping")
        self.btn_warping.setGeometry(7/2*IMG_SIZE_X, 6/4*IMG_SIZE_Y, IMG_SIZE_X / 2, 40)


        # self.btn_animation = QtWidgets.QPushButton(MainWindow)
        # self.btn_animation.setText("Start")
        # self.btn_animation.setGeometry(7/2 * IMG_SIZE_X, 7/4 * IMG_SIZE_Y, IMG_SIZE_X / 2, 40)
        # parameter
        # p
        self.label_p = QtWidgets.QLabel(MainWindow)
        self.label_p.setAlignment(QtCore.Qt.AlignCenter)
        self.label_p.setGeometry(IMG_SIZE_X+10, 5/4*IMG_SIZE_Y, IMG_SIZE_X / 2, 1/4*IMG_SIZE_Y)
        self.label_p.setText(f"p = 0.5")
        
        self.slider_p = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider_p.setGeometry(3/2*IMG_SIZE_X, 5/4*IMG_SIZE_Y + 10, IMG_SIZE_X, 30)
        self.slider_p.setMinimum(0)
        self.slider_p.setMaximum(100)
        self.slider_p.setSingleStep(1)
        self.slider_p.setValue(50)
        # a
        self.label_a = QtWidgets.QLabel(MainWindow)
        self.label_a.setAlignment(QtCore.Qt.AlignCenter)
        self.label_a.setGeometry(IMG_SIZE_X+10, 6/4*IMG_SIZE_Y, IMG_SIZE_X / 2, 1/4*IMG_SIZE_Y)
        self.label_a.setText(f"a = 0.5")
        
        self.slider_a = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider_a.setGeometry(3/2*IMG_SIZE_X, 6/4*IMG_SIZE_Y + 10, IMG_SIZE_X, 30)
        self.slider_a.setMinimum(0)
        self.slider_a.setMaximum(100)
        self.slider_a.setSingleStep(1)
        self.slider_a.setValue(50)
        # b
        self.label_b = QtWidgets.QLabel(MainWindow)
        self.label_b.setAlignment(QtCore.Qt.AlignCenter)
        self.label_b.setGeometry(IMG_SIZE_X+10, 7/4*IMG_SIZE_Y, IMG_SIZE_X / 2, 1/4*IMG_SIZE_Y)
        self.label_b.setText(f"b = 0.5")
        
        self.slider_b = QtWidgets.QSlider(QtCore.Qt.Horizontal, MainWindow)
        self.slider_b.setGeometry(3/2*IMG_SIZE_X, 7/4*IMG_SIZE_Y + 10, IMG_SIZE_X, 30)
        self.slider_b.setMinimum(50)
        self.slider_b.setMaximum(200)
        self.slider_b.setSingleStep(1)
        self.slider_b.setValue(50)

        # configuration buttons
        self.btn_draw_line = QtWidgets.QPushButton("Draw", MainWindow)
        self.btn_draw_line.setGeometry(7/2*IMG_SIZE_X, 5/4*IMG_SIZE_Y, IMG_SIZE_X / 2, 40)

        self.img_gif = QtWidgets.QLabel(MainWindow)
        self.img_gif.setGeometry(0, IMG_SIZE_Y*2, IMG_SIZE_X, IMG_SIZE_Y)

        self.movie_center = QtGui.QMovie("animation/center.gif")
        self.img_gif.setMovie(
            self.movie_center
        )

        self.img_gif_left = QtWidgets.QLabel(MainWindow)
        self.img_gif_right = QtWidgets.QLabel(MainWindow)
        self.movie_right = QtGui.QMovie("animation/right.gif")
        self.img_gif_left.setMovie(
            self.movie_right
        )
        self.movie_left = QtGui.QMovie("animation/left.gif")
        self.img_gif_right.setMovie(
            self.movie_left
        )

        self.movie_left.start()
        self.movie_right.start()
        self.movie_center.start()

        self.img_gif.setGeometry(IMG_SIZE_X*4*(50/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)
        self.img_gif_left.setGeometry(IMG_SIZE_X*4*(0/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)
        self.img_gif_right.setGeometry(IMG_SIZE_X*4*(100/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)