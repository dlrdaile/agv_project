import cv2
import numpy as np
def cv_show(name, image):      # 展示图像
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def picture_pretreatment(image):   # 图像预处理
    image = cv2.medianBlur(image, 5)     # 中值滤波     # 效果最好
    image = cv2.boxFilter(image, -1, (3, 3), normalize=True)   # 方框滤波

    image = cv2.GaussianBlur(image, (5, 5), 1)          # 高斯滤波
    # image = cv2.blur(image, (3, 3))                        # 均值滤波
    # cv_show("滤波效果", image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, gray_image = cv2.threshold(
        gray_image, 70, 255, cv2.THRESH_TOZERO)   # 低于 第一个数的灰度值 全都设为0 保留其他部分
    # cv_show("gray", gray_image)
    return gray_image


def histogram_equalization(image):
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(
        clipLimit=10.0, tileGridSize=(27, 27))  # 对图像进行分割，10*10
    img4 = clahe.apply(image)       # 进行直方图均衡化
    # cv_show("img4", img4)
    return img4


def mask_create(image):    # 筛选重要区域
    # image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((7, 7), np.uint8)
    # 通过腐蚀操作来获取边界 当然可以通过其他方式获取边界
    gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    # cv_show('gradient', gradient)
    ret, thresh = cv2.threshold(
        gradient, 80, 255, cv2.THRESH_BINARY)   # 二值化获取边缘
    _, mask = cv2.threshold(
        gradient, 0, 0, cv2.THRESH_BINARY)          # 获取mask黑底板
    # cv_show('thresh', thresh)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # 筛选最大边界
    area = []
    for i in range(len(contours)):
        area.append(cv2.contourArea(contours[i]))
    res_max = np.argmax(np.array(area))
    # 筛选出图像的边缘
    mask = cv2.drawContours(mask, contours, res_max, [
                            255, 255, 255], cv2.FILLED)
    # cv_show("mask", mask)
    image_vital = cv2.bitwise_and(image, image, mask=mask)
    # cv_show("image_vital", image_vital)
    return image_vital


def grad_treatment(image, original_picture=None):      # 梯度处理，目测不太好用
    if not original_picture:
        original_picture = image.copy()

    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian = cv2.convertScaleAbs(laplacian)
    gradX = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=3)
    gradY = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=3)
    gradX = cv2.convertScaleAbs(gradX)
    gradY = cv2.convertScaleAbs(gradY)
    gradDst = cv2.addWeighted(gradX, 0.5, gradY, 0.5, 2)
    res = np.hstack((gradX, gradY, gradDst))
    # cv_show('res', res)
    # cv_show('gradDst0', gradDst)
    # cv_show("laplacian", laplacian)
    return res, gradDst


def canny_treatment(image):  # 梯度检测
    v2 = cv2.Canny(image, 60, 100)    #
    # cv_show("canny_treatment", v2)
    return v2


def hist_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    # plt.plot(hist)          # 折线图统计
    # plt.show()
    # plt.hist(image.ravel(), 256, [0, 256])
    # plt.show()          # 原图像灰度展示
    equ = cv2.equalizeHist(image)

    # plt.hist(equ.ravel(), 256, [0, 256])
    # plt.show()
    # cv_show("equ", equ)
    return equ


def open_treatment(image):  # 开运算 先腐蚀再膨胀
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opening

def detect_surface(original_image):
    using_image = picture_pretreatment(original_image)   # 图像预处理
    # 创建mask滤波
    image = mask_create(using_image)
    # 直方图凸显 但是黑了点
    # image = hist_image(image)
    image = histogram_equalization(image)

    # 二值化
    ret, image = cv2.threshold(image, 95, 255, cv2.THRESH_BINARY)   # 查找边缘
    # 闭运算 操作填一下空隙
    # 给一个卷积核
    kernel = np.ones((5, 5), np.uint8)
    image = cv2. morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    # cv_show("top_hat", image)

    image = canny_treatment(image)    # 边缘检测

    return image