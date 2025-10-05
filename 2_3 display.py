import os,time,sys
import urandom

from media.display import *
from media.media import *

try:

    img=image.Image(1920,1080,image.ARGB8888)
    # 使用IDE的帧缓冲区作为显示输出
    Display.init(Display.VIRT, width=1920, height=1080, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    while True:
        img.clear()  # 清除图像内容
        for i in range(10):  # 循环绘制10个字符串
            # 随机生成字符串位置、颜色和大小
            x = (urandom.getrandbits(11) % img.width())  # 生成8位随机数（0~255）随机X坐标
            y = (urandom.getrandbits(11) % img.height())  # 随机Y坐标
            r = urandom.getrandbits(8)  # 红色分量
            g = urandom.getrandbits(8)  # 绿色分量
            b = urandom.getrandbits(8)  # 蓝色分量
            size = (urandom.getrandbits(30) % 64) + 32  # 字体大小（32到96之间）

            # 绘制字符串，支持中文字符
            img.draw_string_advanced(
                x, y, size, "Hello World!", color=(r, g, b),
            )

        Display.show_image(img)
        time.sleep(1)
        os.exitpoint()

except KeyboardInterrupt as e:
    print("用户停止: ", e)
except BaseException as e:
    print(f"异常: {e}")
finally:
    # 反初始化显示模块
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    # 释放媒体缓冲区
    MediaManager.deinit()
