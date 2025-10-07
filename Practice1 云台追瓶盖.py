import time, os, sys
from media.sensor import *
from media.display import *
from media.media import *
from machine import Pin,FPIOA,PWM



# Initialize PWM for servo control
fpioa=FPIOA()
fpioa.set_function(47,FPIOA.PWM3)
fpioa.set_function(61,FPIOA.PWM1)
Yaw_pwm=PWM(3,50,0) #50Hz, 0% duty cycle
Pitch_pwm=PWM(1,50,0) #50Hz, 0% duty cycle
Yaw_pwm.enable(1)
Pitch_pwm.enable(1)
Yaw_pwm.duty(1.5/20*100) #90度
Pitch_pwm.duty(1.5/20*100) #90度
print("舵机初始化完成")
time.sleep(1)

sensor_id = 2
sensor = None

PICTURE_WIDTH = 400
PICTURE_HEIGHT = 240

# 虚拟显示器模式
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

#屏幕中心点
center_x=int(PICTURE_WIDTH/2)
center_y=int(PICTURE_HEIGHT/2)
Yaw_Angle=90
Pitch_Angle=90

def Update_Servo(x,y):
    global Yaw_Angle,Pitch_Angle
    if x>center_x+30:
        Yaw_Angle-=1
        if Yaw_Angle<0:
            Yaw_Angle=0
        Yaw_pwm.duty((0.5+Yaw_Angle/180*2)/20*100)
    elif x<center_x-30:
        Yaw_Angle+=1
        if Yaw_Angle>180:
            Yaw_Angle=180
        Yaw_pwm.duty((0.5+Yaw_Angle/180*2)/20*100)
    if y>center_y+30:
        Pitch_Angle+=1
        if Pitch_Angle>180:
            Pitch_Angle=180
        Pitch_pwm.duty((0.5+Pitch_Angle/180*2)/20*100)
    elif y<center_y-30:
        Pitch_Angle-=1
        if Pitch_Angle<0:
            Pitch_Angle=0
        Pitch_pwm.duty((0.5+Pitch_Angle/180*2)/20*100)

def find_best_red_blob(img):

    # 指定颜色阈值
    # 格式：[min_L, max_L, min_A, max_A, min_B, max_B]
    color_threshold = [(45, 68,32,61,2,31)]
#    color_threshold = [(40, 100, 65, 38, -21, 39)]

    # 查找色块，增加merge参数合并邻近色块
    blobs = img.find_blobs(
        color_threshold,
        area_threshold=300,  # 增大面积阈值，过滤小噪声
        merge=True
    )

    if not blobs:
        return None

    best_blob = None

    # 下方解除注释会卡顿
    # img_copy.binary(color_threshold,invert=False)
    for blob in blobs:

        # circles = img_copy.find_circles(threshold=6000,roi=(blob[0]-30,blob[1]-30,blob[2]+60,blob[3]+60))

        # if circles:
        #     circle = circles[0]  # 选择第一个圆
        #     img.draw_circle(circle.circle(), color=(1, 147, 230), thickness=3)  # 绘制圆
        if abs(blob[2]-blob[3])<10: #宽高比过滤
            best_blob = blob


    return best_blob

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

    sensor.set_framesize(width=PICTURE_WIDTH, height=PICTURE_HEIGHT, chn=CAM_CHN_ID_0)
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


        best_blob = find_best_red_blob(img)

        # 如果检测到颜色块
        if best_blob:
            # 绘制颜色块的外接圆
            # blob[0:4] 表示颜色块的矩形框 [x, y, w, h]，

            img.draw_circle(best_blob[5], best_blob[6], int(best_blob[2]/2), color=(0, 255, 0), thickness=3)
            # 在颜色块的中心绘制一个十字
            # blob[5] 和 blob[6] 分别是颜色块的中心坐标 (cx, cy)
            img.draw_cross(best_blob[5], best_blob[6])
            Update_Servo(best_blob[5],best_blob[6])

            # 在控制台输出颜色块的中心坐标
            print("Blob Center: X={}, Y={}".format(best_blob[5], best_blob[6]))

        #--------结束--------

        # 显示捕获的图像，中心对齐，居中显示
        Display.show_image(img, x=int((DISPLAY_WIDTH - PICTURE_WIDTH) / 2), y=int((DISPLAY_HEIGHT - PICTURE_HEIGHT) / 2))

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
