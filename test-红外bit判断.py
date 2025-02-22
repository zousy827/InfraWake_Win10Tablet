import ctypes
import os
import time
import logging

# 定义 POINT 结构体
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

# DLL 文件路径
dll_path = "C:\\test\\inpoutx64.dll"  # 修改为实际路径

# 日志文件路径
log_path = "C:\\test\\service.log"  # 日志文件路径

# 配置日志
logging.basicConfig(
    filename=log_path,  # 日志文件路径
    level=logging.INFO,  # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    datefmt='%Y-%m-%d %H:%M:%S'  # 时间格式
)

# 检查 DLL 文件是否存在
if not os.path.exists(dll_path):
    logging.error(f"DLL file not found at {dll_path}")
    exit(1)

# 加载 DLL
try:
    inpoutx64 = ctypes.windll.LoadLibrary(dll_path)
except Exception as e:
    logging.error(f"Failed to load DLL: {e}")
    exit(1)

# 定义函数的原型
inpoutx64.Inp32.restype = ctypes.c_short
inpoutx64.Inp32.argtypes = [ctypes.c_short]

# 读取 I/O 地址
def read_io_port(port_address):
    try:
        return inpoutx64.Inp32(port_address)
    except Exception as e:
        logging.error(f"Error reading I/O port: {e}")
        return 0  # 返回默认值，避免程序卡住

# 定义控制屏幕的函数
def turn_off_screen():
    # 使用 ctypes 调用 Windows API 关闭屏幕
    SendMessage = ctypes.windll.user32.SendMessageW
    HWND_BROADCAST = 0xFFFF
    WM_SYSCOMMAND = 0x0112
    SC_MONITORPOWER = 0xF170
    MONITOR_OFF = 2
    SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)
    logging.info("Screen turned off")

def turn_on_screen():
    # 模拟鼠标移动（亮屏）
    SetCursorPos = ctypes.windll.user32.SetCursorPos
    mouse_event = ctypes.windll.user32.mouse_event
    MOUSEEVENTF_MOVE = 0x0001

    # 获取当前鼠标位置
    original_pos = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(original_pos))

    # 移动鼠标 1 像素再移回
    SetCursorPos(original_pos.x + 1, original_pos.y)
    time.sleep(0.05)
    SetCursorPos(original_pos.x, original_pos.y)
    mouse_event(MOUSEEVENTF_MOVE, 0, 0, 0, 0)
    logging.info("Screen turned on")

# 主循环
def main():
    port_address = 0xA06  # I/O 端口地址
    last_detected = False  # 记录上一次是否检测到红外
    last_action_time = time.time()  # 记录最后一次亮屏时间
    check_interval = 0.1  # 检测间隔时间，单位秒
    screen_off_delay = 120  # 屏幕息屏延迟时间，单位秒（2分钟）

    logging.info("Service started")

    while True:
        # 读取 I/O 端口的值
        value = read_io_port(port_address)
        detected = (value & 0x80) != 0  # 检查最高位是否为1

        # 打印调试信息
        logging.debug(f"Value at port 0x{port_address:04X}: 0x{value:04X} - Detected: {detected}")

        # 处理亮屏逻辑
        if detected:
            if not last_detected:
                logging.info("Infrared detected, turning screen on")
                turn_on_screen()
                last_action_time = time.time()  # 更新最后一次亮屏时间
            last_detected = True
        else:
            if last_detected:
                logging.info("No infrared detected")
            last_detected = False

        # 处理息屏逻辑
        if time.time() - last_action_time >= screen_off_delay:
            logging.info("No action detected for 2 minutes, turning screen off")
            turn_off_screen()
            last_action_time = time.time()  # 重置最后一次亮屏时间

        # 等待指定的间隔时间再进行下一次检测
        time.sleep(check_interval)

if __name__ == "__main__":
    main()
