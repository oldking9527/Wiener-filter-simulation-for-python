from scipy.signal import wiener#调用SciPy库中的wiener滤波函数
import cv2#建立opencv(cv2)-python库
import numpy as np#建立numpy函数包并简写np
import matplotlib.pyplot as plt#建立matplotlib绘图库简写plt
from skimage import filters#Scikit-Image，数字图片处理包
from skimage.morphology import disk

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
#对输出字体进行调整，使之输出中文

def gasuss_noise(image, mean=0, var=0.01):#定义高斯噪声  mean : 正态分布均值  var : 方差

    image = np.array(image / 255, dtype=float)#将输入数据转化为矩阵
    noise = np.random.normal(mean, var ** 0.5, image.shape)#将原图正态分布得出高斯噪声
    output = image + noise
    if output.min() < 0:
        low_clip = -1
    else:
        low_clip = 0
    output = np.clip(output, low_clip, 1.0)#数组output中的所有数限定到范围low_clip和1中
    output = np.uint8(output * 255)#存储的数据格式设为np.uint8
    return output

def oldking(image):
    path=image#提取图像路径
    lena = cv2.imread(image)#读取连接部分的图片并转换为灰度图像
    if lena.shape[-1] == 3:
        lenaGray = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
    else:
        lenaGray = lena.copy()

    plt.figure('滤波结果')
    plt.subplot(221)
    plt.title('原图')
    plt.imshow(lenaGray, cmap='gray')#展示图片，且为灰色

    # 添加高斯噪声
    lenaNoise = gasuss_noise(lenaGray)

    #plt.figure('添加高斯噪声后的图像')
    plt.subplot(222)
    plt.title('添加高斯噪声后的图像')
    plt.imshow(lenaNoise, cmap='gray')

    # 维纳滤波
    lenaNoise = lenaNoise.astype('float64')#转换数据类型
    lenaWiener = wiener(lenaNoise, [5,5])#调用维纳滤波函数
    lenaWiener = np.uint8(lenaWiener / lenaWiener.max() * 255)

    #plt.figure('经过维纳滤波后的图像')
    plt.subplot(224)
    plt.title('经过维纳滤波后的图像')
    plt.imshow(lenaWiener, cmap='gray')
    plt.show()

    #中值滤波
    edges1 = filters.median(lenaNoise, disk(5))

    #plt.figure('经过中值滤波后的图像')
    plt.subplot(223)
    plt.title('经过中值滤波后的图像')
    plt.imshow(edges1, cmap='gray')
    plt.show()

    #高斯滤波
    # edges2 = filters.gaussian_filter(lenaNoise, sigma=5)
    # plt.subplot(225)
    # plt.title('经过高斯滤波后的图像')
    # plt.imshow(edges2, cmap='gray')
    # plt.show()
