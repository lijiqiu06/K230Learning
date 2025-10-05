import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

sensor_id = 2
sensor = None

picture_width = int(1920/2)
picture_height = int(1080/2)

# 虚拟显示器模式
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080

try:
    # 构造一个具有默认配置的摄像头对象
    sensor = Sensor(id=sensor_id,width=1920, height=1080)
    # 重置摄像头sensor
    sensor.reset()

    # 无需进行镜像和翻转
    # 设置不要水平镜像
    sensor.set_hmirror(False)
    # 设置不要垂直翻转
    sensor.set_vflip(False)

    sensor.set_framesize(width=picture_width, height=picture_height, chn=CAM_CHN_ID_0)
    # 设置通道0的输出像素格式为RGB565，要注意有些案例只支持GRAYSCALE格式
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    # 根据模式初始化显示器
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)

    # 初始化媒体管理器
    MediaManager.init()
    # 启动传感器
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()
        os.exitpoint()

        # 捕获通道0的图像
        src_img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # 在屏幕左上角显示原始图像
        Display.show_image(src_img,x=0,y=0,layer = Display.LAYER_OSD0)

        # 图像处理放到这里
        #--------开始--------

        # 这里可以插入各种图像处理逻辑，例如二值化、直方图均衡化、滤波等

        # #直方图均衡化
        # src_img.histeq()

        # # Gamma 校正
        # src_img.gamma_corr(1.05)

        # #旋转校正
        # src_img.rotation_corr(0,20)

        # #镜头畸变校正
        # src_img.lens_corr(3.0)

        # #二值化  需将Sensor.RGB565改为Sensor.GRAYSCALE
        # src_img.binary([(120, 255)],invert=False)  # 二值化，阈值范围为 (120, 255),不进行像素值反转

        # # Canny 边缘检测算法  需将Sensor.RGB565改为Sensor.GRAYSCALE
        # src_img.find_edges(image.EDGE_CANNY, threshold=(20, 80))

        # # 简单的阈值高通滤波算法
        # src_img.find_edges(image.EDGE_SIMPLE, threshold=(20, 80))

        # 拉普拉斯核 适用于Sensor.RGB565 和 Sensor.GRAYSCALE
        src_img.laplacian(2,mul=0.2)  # 拉普拉斯边缘检测
        #--------结束--------

        # 在屏幕右上角显示处理后的图像
        Display.show_image(src_img,x=DISPLAY_WIDTH-picture_width,y=0,layer = Display.LAYER_OSD1)

        # 打印帧率到控制台
        print(fps.fps())

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    # 停止传感器运行
    if isinstance(sensor, Sensor):
        sensor.stop()
    # 反初始化显示模块
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()
