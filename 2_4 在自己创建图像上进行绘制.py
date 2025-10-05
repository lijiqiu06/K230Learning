import time, os, gc, sys, urandom

from media.display import *
from media.media import *

def CreateRandomColor():
    return (urandom.getrandbits(8), urandom.getrandbits(8), urandom.getrandbits(8))

try:

    img=image.Image(1920,1080,image.ARGB8888)
    # 使用IDE的帧缓冲区作为显示输出
    Display.init(Display.VIRT, width=1920, height=1080, to_ide=True)
    # 初始化媒体管理器
    MediaManager.init()

    while True:
        img.clear()  # 清除图像内容
        img.draw_line(200,200,900,900,color=CreateRandomColor())  # 绘制线段
        img.draw_rectangle(100,100,400,400,color=CreateRandomColor(),thickness=50)  # 绘制矩形
        img.draw_circle(800,800,200,color=CreateRandomColor(),thickness=20)  # 绘制圆
        img.draw_cross(1000,300,color=CreateRandomColor(),size=100,thickness=10)  # 绘制十字
        img.draw_arrow(1200,200,1500,500,color=CreateRandomColor(),thickness=15)  # 绘制箭头
        img.draw_ellipse(1500,800,200,100,0,color=CreateRandomColor(),thickness=20)  # 绘制椭圆 要有旋转角度
        keypoints = [(30, 30,0), (50, 50,0), (70, 70,0)] #要有旋转角度
        img.draw_keypoints(keypoints, size=10, color=(255, 255, 0), thickness=2)  # 绘制黄色关键点
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
