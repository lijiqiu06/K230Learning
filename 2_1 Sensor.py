import os,time,sys
import utime
from media.sensor import *
from media.display import *
from media.media import *

try:
    sensor=Sensor(id=2,fps=60)
    sensor.reset()

    sensor.set_framesize(Sensor.FHD, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB888, chn=CAM_CHN_ID_0)

    # 使用IDE的帧缓冲区作为显示输出
    Display.init(Display.VIRT, width=1920, height=1080, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    sensor.run()

    clock=utime.clock()
    while True:
        os.exitpoint()
        clock.tick()
        img=sensor.snapshot(chn=CAM_CHN_ID_0)
        Display.show_image(img)
        print("FPS:",clock.fps())
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
