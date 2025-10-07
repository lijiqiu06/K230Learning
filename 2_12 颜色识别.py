import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *

sensor_id = 2
sensor = None

picture_width = 400
picture_height = 240

# 虚拟显示器模式
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

try:
    # 构造一个具有默认配置的摄像头对象
    sensor = Sensor(id=sensor_id)
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
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)

    # 初始化媒体管理器
    MediaManager.init()
    # 启动传感器
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()
        os.exitpoint()

        # 捕获通道0的图像
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        # 图像处理放到这里
        #--------开始--------
        # 指定颜色阈值
        # 格式：[min_L, max_L, min_A, max_A, min_B, max_B]
        color_threshold = [(45, 68,32,61,2,31)]
        #color_threshold 是要寻找的颜色的阈值，area_threshold 表示过滤掉小于此面积的色块。
        blobs = img.find_blobs(color_threshold,area_threshold = 200,merge=True)

        # 如果检测到颜色块
        if blobs:
            # 遍历每个检测到的颜色块
            for blob in blobs:
                # 绘制颜色块的外接矩形
                # blob[0:4] 表示颜色块的矩形框 [x, y, w, h]，
                img.draw_rectangle(blob[0:4])

                # 在颜色块的中心绘制一个十字
                # blob[5] 和 blob[6] 分别是颜色块的中心坐标 (cx, cy)
                img.draw_cross(blob[5], blob[6])

                # 在控制台输出颜色块的中心坐标
                print("Blob Center: X={}, Y={}".format(blob[5], blob[6]))

        #--------结束--------

        # 显示捕获的图像，中心对齐，居中显示
        Display.show_image(img, x=int((DISPLAY_WIDTH - picture_width) / 2), y=int((DISPLAY_HEIGHT - picture_height) / 2))

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
