from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from mainUI import IMG_SIZE_X, IMG_SIZE_Y, Ui_MainWindow
from drawUI import H_TEXT_AREA, Ui_DrawArea
from WarpingAlgorithm import *
from utils import *
import cv2
import threading
import glob
import time



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btn_draw_line.clicked.connect(self.open_drawing_area)
        self.ui.btn_warping.clicked.connect(self.warping)
        # self.ui.btn_animation.clicked.connect(self.generate_animation)
        self.ui.slider_time.valueChanged.connect(self.slider_time_changed)
        self.ui.slider_p.valueChanged.connect(self.slider_p_changed)
        self.ui.slider_a.valueChanged.connect(self.slider_a_changed)
        self.ui.slider_b.valueChanged.connect(self.slider_b_changed)

        self.features_line_1 = []
        self.features_line_2 = []

        # git thread
        # self.thread_gif = threading.Thread(target=self.show_gif)
        # self.thread_gif.start()
        
        self.ui.btn_warping.setEnabled(False)
        self.exit_gui = False
        self.show_gif_status = True

    def open_drawing_area(self):
        self.show_gif_status = False
        print("open")
        drawArea = DrawArea(self)
        drawArea.exec_()
        self.show_gif_status = True

        if len(self.features_line_1) < 0 or (len(self.features_line_1) != len(self.features_line_2)):
            self.ui.btn_warping.setEnabled(False)
        else:
            self.ui.btn_warping.setEnabled(True)
        # print(self.features_line_1, self.features_line_2)

    def generate_animation(self):
        for tt in range(0, 100, 1):
            t = tt / 100
            dst_lines = [(l1*(1-t)+l2*t)  for l1, l2 in zip(self.features_line_1, self.features_line_2)]

            img_1_warped = warping(
                src_lines = self.features_line_1,
                dst_lines = dst_lines,
                src = self.ui.img_1.pixmap().toImage(),
                para = self.ui
            )
            img_2_warped = warping(
                src_lines = self.features_line_2,
                dst_lines = dst_lines,
                src = self.ui.img_2.pixmap().toImage(),
                para = self.ui
            )

            cv2.imwrite(f"animation/1/{tt}.jpeg", img_1_warped)
            cv2.imwrite(f"animation/2/{tt}.jpeg", img_2_warped)
             


    def warping(self):
        
        t = self.ui.slider_time.value() / 100
        dst_lines = [(l1*(1-t)+l2*t)  for l1, l2 in zip(self.features_line_1, self.features_line_2)]

        img_1_warped = warping(
            src_lines = self.features_line_1,
            dst_lines = dst_lines,
            src = self.ui.img_1.pixmap().toImage(),
            para = self.ui
        )
        qimage = QImage(img_1_warped, img_1_warped.shape[1], img_1_warped.shape[0], QImage.Format_RGB32)
        qpixel = QPixmap.fromImage(qimage)
        self.ui.img_1_warping.setPixmap(qpixel)

        img_2_warped = warping(
            src_lines = self.features_line_2,
            dst_lines = dst_lines,
            src = self.ui.img_2.pixmap().toImage(),
            para = self.ui
        )
        qimage = QImage(img_2_warped, img_2_warped.shape[1], img_2_warped.shape[0], QImage.Format_RGB32)
        qpixel = QPixmap.fromImage(qimage)
        self.ui.img_2_warping.setPixmap(qpixel)

        self.ui.img_morphing.setGeometry(255 + t * 255 * 2, 0, 255, 189)
        blending_img = img_1_warped * (1-t) + img_2_warped * t
        blending_img = blending_img.astype(np.uint8).copy()
        qimage = QImage(blending_img, blending_img.shape[1], blending_img.shape[0], QImage.Format_RGB32)
        self.ui.img_morphing.setPixmap(
            QPixmap.fromImage(qimage)
        )
        self.show_gif_status = True


    def slider_time_changed(self):
        self.ui.label_time.setText(f"t = {self.ui.slider_time.value()/100}")

    def slider_p_changed(self):
        self.ui.label_p.setText(f"p = {self.ui.slider_p.value()/100}")

    def slider_a_changed(self):
        self.ui.label_a.setText(f"a = {self.ui.slider_a.value()/100}")

    def slider_b_changed(self):
        self.ui.label_b.setText(f"b = {self.ui.slider_b.value()/100}")

    def show_gif_thread(self):
        import os
        right_path = sorted([n for n in glob.glob("animation/1/*.jpeg")], key=lambda x: int(os.path.basename(x)[0:-5]))
        left_path = sorted([n for n in glob.glob("animation/2/*.jpeg")], key=lambda x: int(os.path.basename(x)[0:-5]))
        right_img = [cv2.cvtColor(cv2.imread(n), cv2.COLOR_BGR2RGB) for n in right_path]
        left_img = [cv2.cvtColor(cv2.imread(n), cv2.COLOR_BGR2RGB) for n in left_path]
        blending = [cv2.addWeighted(img1, 1-t/100, img2, t/100, 0) for t, (img1, img2) in enumerate(zip(right_img, left_img))]
        blending_qimage = [QImage(n.data, n.shape[1], n.shape[0], n.shape[1]*3, QImage.Format_RGB888) for n in blending]
        bleding_qpixels = [QPixmap.fromImage(n) for n in blending_qimage]
        bleding_qpixels += list(reversed(bleding_qpixels))

        blending_left = [QPixmap.fromImage(
            QImage(n.data, n.shape[1], n.shape[0], n.shape[1]*3, QImage.Format_RGB888)
        ) for n in left_img]
        blending_right = [QPixmap.fromImage(
            QImage(n.data, n.shape[1], n.shape[0], n.shape[1]*3, QImage.Format_RGB888)
        ) for n in right_img]
        blending_left += list(reversed(blending_left))
        blending_right += list(reversed(blending_right))

        pos = [QRect(IMG_SIZE_X * 4 * (t/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y) for t in range(100)]
        pos += list(reversed(pos))
        self.ui.img_gif.setGeometry(IMG_SIZE_X*4*(50/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)
        self.ui.img_gif_left.setGeometry(IMG_SIZE_X*4*(0/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)
        self.ui.img_gif_right.setGeometry(IMG_SIZE_X*4*(100/100), 2*IMG_SIZE_Y, IMG_SIZE_X, IMG_SIZE_Y)

        turn = True
        idx = 0
        while not self.exit_gui:
            while self.show_gif_status:
                self.ui.img_gif.setPixmap(bleding_qpixels[idx])
                self.ui.img_gif_left.setPixmap(blending_right[idx])
                self.ui.img_gif_right.setPixmap(blending_left[idx])

                idx += 1
                idx %= 198
                time.sleep(0.05)
                # self.update()


    def closeEvent(self, evt):
        self.show_gif_status = False
        self.exit_gui = True
        # self.thread_gif.join()

# class DrawGIFThread(QThread):
#     def __init__(self):
#         super(DrawGIFThread, self).__init__()
#     def run(self):
 

class DrawArea(QDialog, QMouseEvent):
    def __init__(self, parent):
        super().__init__()

        self.left_turn = True
        self.startPoint = QPoint()
        self.endPoint = QPoint()

        self.parent = parent

        self.ui = Ui_DrawArea()
        self.ui.setupUi(self, self.parent.ui.img_1.pixmap(), self.parent.ui.img_2.pixmap())
        self.img_1 = self.ui.img_1
        self.img_2 = self.ui.img_2

        self.label_img = QLabel(self)
        self.label_img.setGeometry(0, 0, 255*2, 189)
        self.pix = QPixmap(255 * 2, 189)
        self.pix.fill(Qt.transparent)
                
    
class DrawArea(QDialog, QMouseEvent):
    def __init__(self, parent):
        super().__init__()

        self.left_turn = True
        self.startPoint = QPoint()
        self.endPoint = QPoint()

        self.parent = parent

        self.ui = Ui_DrawArea()
        self.ui.setupUi(self, self.parent.ui.img_1.pixmap(), self.parent.ui.img_2.pixmap())
        self.img_1 = self.ui.img_1
        self.img_2 = self.ui.img_2

        self.label_img = QLabel(self)
        self.label_img.setGeometry(0, 0, 255*2, 189)
        self.pix = QPixmap(255 * 2, 189)
        self.pix.fill(Qt.transparent)
        
class DrawArea(QDialog, QMouseEvent):
    def __init__(self, parent):
        super().__init__()

        self.left_turn = True
        self.is_drawing = True
        self.startPoint = QPoint()
        self.endPoint = QPoint()

        self.parent = parent

        self.ui = Ui_DrawArea()
        self.ui.setupUi(self, self.parent.ui.img_1.pixmap(), self.parent.ui.img_2.pixmap())
        self.img_1 = self.ui.img_1
        self.img_2 = self.ui.img_2

        self.label_img = QLabel(self)
        self.label_img.setGeometry(0, 0, 255*2, 189)
        self.pix = QPixmap(255 * 2, 189)
        self.pix.fill(Qt.transparent)
        self.pen = QPen(Qt.SolidLine)      
        self.pen.setWidth(3)
        self.pen.setColor(Qt.red)

        self.features_line_1 = []
        self.features_line_2 = []

        
    def mousePressEvent(self, a0: QMouseEvent):
        self.startPoint = a0.pos()
        self.endPoint = self.startPoint

        if self.left_turn and self.is_invalid_area(a0.pos(), self.left_turn):
            self.ui.info_board.setText("Exceed drawable area. (left turn)")
            self.is_drawing = False
            return None
        elif (not self.left_turn) and self.is_invalid_area(a0.pos(), self.left_turn):
            self.is_drawing = False
            self.ui.info_board.setText("Exceed drawable area. (right turn)") 
            return None

        if a0.button() == Qt.LeftButton:
            self.is_drawing = True
            print("start", self.startPoint)
    
    def mouseMoveEvent(self, a0: QMouseEvent):
        if self.is_drawing:
            if self.left_turn and self.is_invalid_area(a0.pos(), self.left_turn):
                self.ui.info_board.setText("Exceed drawable area. (left turn)")
            elif (not self.left_turn) and self.is_invalid_area(a0.pos(), self.left_turn):
                self.ui.info_board.setText("Exceed drawable area. (right turn)")

    def mouseReleaseEvent(self, a0: QMouseEvent):        
        self.ui.info_board.clear()

        if self.left_turn and self.is_invalid_area(a0.pos(), self.left_turn):
            self.ui.info_board.setText("Exceed drawable area. (left turn)")
            self.is_drawing = False
        elif (not self.left_turn) and self.is_invalid_area(a0.pos(), self.left_turn):
            self.is_drawing = False
            self.ui.info_board.setText("Exceed drawable area. (right turn)")  

        if a0.button() == Qt.LeftButton and self.is_drawing and self.startPoint != a0.pos():
            self.endPoint = a0.pos()
            print("end", self.endPoint)
            if self.left_turn:
                self.features_line_1.append(
                    Line(s = Point(self.startPoint.x(), self.startPoint.y()),
                         e = Point(self.endPoint.x(), self.endPoint.y())))
            else:
                self.features_line_2.append(
                    Line(s = Point(self.startPoint.x(), self.startPoint.y()).shift_x(-255),
                         e = Point(self.endPoint.x(), self.endPoint.y()).shift_x(-255)))
            self.left_turn = (not self.left_turn)
            self.ui.info_board.setText(f"It's {'left' if self.left_turn else 'right'} turn.")

    def paintEvent(self, ev):
        qp = QPainter(self.pix)
        qp.setPen(self.pen)
        if self.startPoint != self.endPoint:
            qp.setPen(QPen(Qt.red, 3))
            qp.drawLine(self.startPoint, self.endPoint)
            qp.setPen(QPen(Qt.green, 3))
            qp.drawEllipse(self.startPoint.x()-1, self.startPoint.y()-1, 2, 2)
            qp.setPen(QPen(Qt.blue, 3))
            qp.drawEllipse(self.endPoint.x()-1, self.endPoint.y()-1, 2, 2)
        self.label_img.setPixmap(self.pix)

    def is_invalid_area(self, point, left_turn):
        if left_turn and (point.x() < IMG_SIZE_X and point.x() >= 0) and (point.y() >= 0 and point.y() < IMG_SIZE_Y):
            return False
        if (not left_turn) and (point.x() < IMG_SIZE_X * 2 and point.x() >= IMG_SIZE_X) \
                            and (point.y() >= 0 and point.y() < IMG_SIZE_Y): 
            return False
        return True

    def closeEvent(self, ev):
        self.parent.features_line_1 = self.features_line_1
        self.parent.features_line_2 = self.features_line_2
        # self.parent.ui.img_1_draw.setPixmap(self.label_img.geometry(0, 0, 255, 189))
        # self.parent.ui.img_2_draw.setPixmap(self.label_img.geometry(255, 0, 255, 189))