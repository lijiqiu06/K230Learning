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
    # 根据模式初始化显示器
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=60)


    # 初始化媒体管理器
    MediaManager.init()

    fps = time.clock()
    src_img = image.Image("/data/test.bmp")  # 预先加载一张图片用于显示测试
    # 在屏幕左上角显示原始图像
    Display.show_image(src_img,x=0,y=0,layer = Display.LAYER_OSD0)
    while True:
        fps.tick()
        os.exitpoint()

        # 图像处理放到这里
        #--------开始--------

        # 这里可以插入各种图像处理逻辑，例如二值化、直方图均衡化、滤波等

        #直方图均衡化
        src_img.histeq()
        
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
