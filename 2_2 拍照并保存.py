import time, os, sys

#使用默认摄像头，可选参数:0,1,2.
sensor_id = 2

# ========== 多媒体/图像相关模块 ==========
from media.sensor import Sensor, CAM_CHN_ID_0
from media.display import Display
from media.media import MediaManager
import image

# ========== GPIO/按键/LED相关模块 ==========
from machine import Pin
from machine import FPIOA

def Key_Init():
    fpioa=FPIOA()
    fpioa.set_function(53,FPIOA.GPIO53)
    UserKey=Pin(53,Pin.IN,pull=Pin.PULL_DOWN)
    return UserKey

def Key_Scan(UserKey):
    global prebuttontime, button_state
    debounce = 20  # 消抖时间20ms
    cur = UserKey.value()
    now = time.ticks_ms()

    # 情况1：第一次检测到按下 → 记录时间，进入“等待确认”状态
    if cur == 1 and button_state == 0:
        prebuttontime = now
        button_state = 1

    # 情况2：持续按住，并且超过消抖时间 → 确认按下，返回1
    elif cur == 1 and button_state == 1:
        if time.ticks_diff(now, prebuttontime) > debounce:
            button_state = 2
            return 1

    # 情况3：松开按键 → 状态归零
    elif cur == 0:
        button_state = 0

    return 0

def RGB_Init():
    RGB=[]
    fpioa=FPIOA()
    fpioa.set_function(20,FPIOA.GPIO20)
    fpioa.set_function(62,FPIOA.GPIO62)
    fpioa.set_function(63,FPIOA.GPIO63)

    RGB_G=Pin(20,Pin.OUT)
    RGB_R=Pin(62,Pin.OUT)
    RGB_B=Pin(63,Pin.OUT)

    RGB_R.high()
    RGB_G.high()
    RGB_B.high()
    RGB.append(RGB_R)
    RGB.append(RGB_G)
    RGB.append(RGB_B)
    return RGB

# 选一个LED用来拍照提示
rgb=RGB_Init()
PHOTO_LED = rgb[2]   # 蓝色LED

# ========== 初始化按键：按下时高电平 ==========
prebuttontime=0
button_state=0
button = Key_Init()

# ========== 显示配置 ==========
DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 1080
FPS = 30

def lckfb_save_jpg(img, filename, quality=95):
    """
    将图像压缩成JPEG后写入文件 (不依赖第一段 save_jpg/MediaManager.convert_to_jpeg 的写法)
    :param img:    传入的图像对象 (Sensor.snapshot() 得到)
    :param filename: 保存的目标文件名 (含路径)
    :param quality:  压缩质量 (1-100)
    """
    compressed_data = img.compress(quality=quality)

    with open(filename, "wb") as f:
        f.write(compressed_data)

    print(f"[INFO] 使用 lckfb_save_jpg() 保存完毕: {filename}")


# ========== 自动创建图片保存文件夹 & 计算已有图片数量 ==========
image_folder = "/data/images"

# 若不存在该目录则创建
try:
    os.stat(image_folder)  # 尝试获取目录信息
except OSError:
    os.mkdir(image_folder)  # 若失败则创建该目录

# 统计当前目录下以 “lckfb_XX.jpg” 命名的文件数量，自动从最大编号继续
image_count = 0
existing_images = [fname for fname in os.listdir(image_folder)
                   if fname.startswith("lckfb_") and fname.endswith(".jpg")]

if existing_images:
    # 提取编号并找出最大值
    numbers = []
    for fname in existing_images:
        # 假设文件名格式为 "lckfb_XX.jpg"
        # 取中间 XX 部分转为数字
        try:
            num_part = fname[6:11]  # "lckfb_" 长度为6，取到 ".jpg" 前还要注意下标
            numbers.append(int(num_part))
        except:
            pass
    if numbers:
        image_count = max(numbers)

try:
    print("[INFO] 初始化摄像头 ...")
    sensor = Sensor(id=sensor_id)
    sensor.reset()
    
    sensor.set_framesize(width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, chn=CAM_CHN_ID_0)
    sensor.set_pixformat(Sensor.RGB565, chn=CAM_CHN_ID_0)

    # ========== 初始化显示 ==========
    Display.init(Display.VIRT, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, fps=FPS)
    # ========== 初始化媒体管理器 ==========
    MediaManager.init()
    # ========== 启动摄像头 ==========
    sensor.run()
    print("[INFO] 摄像头已启动，进入主循环 ...")

    fps = time.clock()

    while True:
        fps.tick()
        os.exitpoint()

        #抓取通道0的图像
        img = sensor.snapshot(chn=CAM_CHN_ID_0)

        if Key_Scan(button):
            # LED闪烁提示
            PHOTO_LED.low()   # 点亮LED
            time.sleep_ms(20)
            PHOTO_LED.high()  # 熄灭LED

            # 拍照并保存
            image_count += 1
            filename = f"{image_folder}/lckfb_{image_count:05d}_{img.width()}x{img.height()}.jpg"
            print(f"[INFO] 拍照保存 -> {filename}")

            # 直接调用自定义的 lckfb_save_jpg() 函数
            lckfb_save_jpg(img, filename, quality=95)

        img.draw_string_advanced(0, 0, 32, str(image_count), color=(255, 0, 0))
        img.draw_string_advanced(0, DISPLAY_HEIGHT-32, 32, str(fps.fps()), color=(255, 0, 0))

        Display.show_image(img)

except KeyboardInterrupt:
    print("[INFO] 用户停止")
except BaseException as e:
    print(f"[ERROR] 出现异常: {e}")
finally:
    if 'sensor' in locals() and isinstance(sensor, Sensor):
        sensor.stop()
    Display.deinit()
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)
    MediaManager.deinit()
