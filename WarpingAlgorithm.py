from multiprocessing import process
from PyQt5.QtCore import QLine, QPoint
from PyQt5.QtGui import QColor, QImage, qRgb
from utils import *
import numpy as np
import multiprocessing as mp
import threading


def warping(src_lines, dst_lines, src, para):
    src_img = qimage_to_numpy_img(src)
    dst_img = np.zeros(src_img.shape, dtype=np.uint8)
    p = para.slider_p.value() / 100
    a = para.slider_a.value() / 100
    b = para.slider_b.value() / 100
    
    thread_list = []
    for y_ptr in range(src_img.shape[1]):
        for x_ptr in range(src_img.shape[0]):
            pp = Point(x_ptr, y_ptr)
            single_point_calculation(dst_img, src_img, pp, src_lines, dst_lines, p, a, b)
            thread_list.append(
                threading.Thread(target = single_point_calculation, args=(dst_img, src_img, pp, src_lines, dst_lines, p, a, b))
            )
            thread_list[-1].start()
            # X = single_point_calculation(p, src_lines, dst_lines, para)
    for thread in thread_list:
        thread.join()

    return dst_img.transpose((1,0,2)).copy()

def single_point_calculation(dst_img, src_img, pp, src_lines, dst_lines, p, a, b):
    DSUM = Point(0, 0)
    weightsum = 0
    for src_line, dst_line in zip(src_lines, dst_lines):
        u, v = calculate_u_v(dst_line, pp)
        x = calculate_mapped_src_point(u, v, src_line)
        D = x - pp
        weight = calculate_weight(src_line, x, u, v, p, a, b)
        DSUM = DSUM + (D * weight)
        weightsum += weight
    X = pp + DSUM / weightsum

    if X.x < 0: X.x = 0
    elif X.x >= 253: X.x = 253 
    if X.y < 0: X.y = 0
    elif X.y >= 187: X.y = 187            

    dst_img[pp.x, pp.y] = bilinear_interpolation(X, src_img)

def bilinear_interpolation(X, src):
    x = X.x
    y = X.y
    a = x - int(x)
    b = y - int(y)

    color =  src[int(x), int(y)] * (1-a) * (1-b) + \
            src[int(x), int(y)+1] * (1-a) * b + \
            src[int(x)+1, int(y)] * a * (1-b) + \
            src[int(x)+1, int(y)+1] * a * b
    return color

def calculate_weight(line, x, u, v, p, a, b):
    dist = line.dist(x, u, v)

    return pow((pow(line.length(), p) / (a + dist)), b)

def calculate_u_v(line, X):
    vec = Vector(line)
    u = ((X - line.P) * (line.Q - line.P)) / pow(line.length(), 2)
    v = ((X - line.P) * vec.perpendicular()) / line.length()

    return u, v

def calculate_mapped_src_point(u, v, line):
    vec = Vector(line)
    x = line.P + ((line.Q - line.P) * u) + ((vec.perpendicular() * v) / line.length())
    return x

def qimage_to_numpy_img(img):
    size = img.size()
    s = img.bits().asstring(size.width() * size.height() * img.depth() // 8)
    ttimg = np.fromstring(s, dtype=np.uint8).reshape((size.height(), size.width(), img.depth() // 8))
    ttimg = np.swapaxes(ttimg, 0, 1)

    # print([QColor(img.pixel(QPoint(0, 1))).red(), QColor(img.pixel(QPoint(0, 1))).green(), QColor(img.pixel(QPoint(0, 1))).blue()], npimg[1, 0])
    # npimg = np.zeros((size.width(), size.height(), img.depth() // 8), dtype=np.uint8)
    # for y_ptr in range(size.height()):
    #     for x_ptr in range(size.width()):
    #         p = img.pixel(QPoint(x_ptr, y_ptr))
    #         c = QColor(p)
    #         npimg[x_ptr, y_ptr] = np.array([c.blue(), c.green(), c.red(), c.alpha()], dtype=np.uint8)
    
    # npimg = np.swapaxes(npimg, 0, 1)
    return ttimg