import os
import string
import sys
import 界面
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import 维纳滤波
import 音频滤波
import 添加噪声
import soundfile as sf

class mwindow(QWidget, 界面.Ui_Dialog):
    str=""

    def __init__(self):
        super(mwindow, self).__init__()
        self.setupUi(self)

    #选择图片
    def openimage(self):
        #选择图片
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "img", "*.jpg;*.tif;*.png;;All Files(*)")
        if imgName=="":
            return 0
        #qt5读取图片
        self.str=imgName
        jpg = QPixmap(imgName).scaled(self.label.width(), self.label.height())
        #显示原图
        self.label.setPixmap(jpg)

    def openwiener(self):
        print(self.str)#输出文件路径
        维纳滤波.oldking(self.str)

    def opensoundfile(self):
        sfName, sfType = QFileDialog.getOpenFileName(self, "打开音频", "sf", "*.wav;;All Files(*)")
        if sfName == "":
            return 0
        self.str=sfName
        添加噪声.main()
        音频滤波.main()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    #初始化窗口
    m=mwindow()
    #绑定按钮事件
    m.pushButton.clicked.connect(m.openimage)#选择图片
    m.pushButton_2.clicked.connect(m.openwiener)#开始维纳滤波
    m.pushButton_3.clicked.connect(m.opensoundfile)#打开音频
    m.show()
    sys.exit(app.exec_())

