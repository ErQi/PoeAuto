import re
import time
import pyautogui
import pygetwindow as gw
import win32gui
import pyperclip
import keyboard
import sys
import threading


class PathOfExile:
    def __init__(self, window):
        self.window = window
        self.window_x_offset = 0  # 初始偏差为0
        self.window_y_offset = 0  # 初始偏差为0
        self.sleep = 0.048

    def calculate_offsets(self):
        # 获取窗口左上角的坐标
        left, top, _, _ = win32gui.GetClientRect(self.window._hWnd)  # 使用窗口对象的 _hWnd 属性获取句柄
        self.window_x_offset, self.window_y_offset = win32gui.ClientToScreen(self.window._hWnd, (left, top))

    def apply_offsets(self, x, y):
        # 应用偏差值，将窗口内坐标转换为桌面坐标
        x += self.window_x_offset
        y += self.window_y_offset
        return x, y

    def onClickChisel(self):
        # 点击制图钉
        x, y = self.apply_offsets(640, 220)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onClickAlchemy(self):
        # 点击点金石
        x, y = self.apply_offsets(515, 290)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onClickScouring(self):
        # 点击重铸石
        x, y = self.apply_offsets(460, 550)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onClickWisdom(self):
        # 点击知识卷轴
        x, y = self.apply_offsets(125, 225)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onClickVaal(self):
        # 点击瓦尔宝石
        x, y = self.apply_offsets(640, 550)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onClickBackpack(self, x, y):
        # 左键点击背包
        x, y = self.apply_offsets(1625 + x, 650 + y)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.click()

    def onCopyBackpack(self, x, y):
        # 移动到背包指定位置复制
        x, y = self.apply_offsets(1625 + x, 650 + y)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.hotkey('ctrl', 'c')


global should_continue
should_continue = True


def on_key_event(event):
    global should_continue
    if event.name == 'f1':
        print("按下f1键，退出循环")
        keyboard.unhook_all()  # 停止监听所有按键事件
        should_continue = False


def listen_for_esc_key():
    keyboard.on_release(on_key_event)
    keyboard.wait()


def onUsageWisdom(z):
    global should_continue
    # 使用知识卷轴
    pyautogui.keyDown('shift')
    poe.onClickWisdom()
    for i in range(z):
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        if not should_continue:
            break
    pyautogui.keyUp('shift')


def onUsageScouring(z):
    global should_continue
    # 使用重铸石
    pyautogui.keyDown('shift')
    poe.onClickScouring()
    for i in range(z):
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        if not should_continue:
            break
    pyautogui.keyUp('shift')


def onUsageChisel(z):
    global should_continue
    # 使用制图钉
    pyautogui.keyDown('shift')
    poe.onClickChisel()
    for i in range(z):
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        if not should_continue:
            break
    pyautogui.keyUp('shift')


def onUsageAlchemy(z):
    global should_continue
    # 使用点金石
    pyautogui.keyDown('shift')
    poe.onClickAlchemy()
    for i in range(z):
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        if not should_continue:
            break
    pyautogui.keyUp('shift')


def onUsageVaal(z):
    global should_continue
    # 使用瓦尔宝珠
    pyautogui.keyDown('shift')
    poe.onClickVaal()
    for i in range(z):
        poe.onClickBackpack(int(i / 5) * 55, i % 5 * 55)
        if not should_continue:
            break
    pyautogui.keyUp('shift')


def onScouringAndAlchemy(x, y):
    global should_continue
    if not should_continue:
        sys.exit()
    # 先点击重铸
    poe.onClickScouring()
    poe.onClickBackpack(x, y)
    # 再点击点金
    poe.onClickAlchemy()
    poe.onClickBackpack(x, y)
    pyautogui.hotkey('ctrl', 'c')


if __name__ == '__main__':
    # 获取目标窗口
    target_title = "Path of Exile"  # 用你要操作的窗口标题替换
    target_window = gw.getWindowsWithTitle(target_title)

    # 子线程进行监听退出按键
    listener_thread = threading.Thread(target=listen_for_esc_key)
    listener_thread.start()

    if len(target_window) > 0:
        target_window = target_window[0]
        # 窗口最前方显示
        target_window.activate()
        time.sleep(1)

        count = 48
        # 创建一个窗口点击工具对象，将窗口作为参数传递
        poe = PathOfExile(target_window)

        # 计算偏差值
        poe.calculate_offsets()

        # 使用知识卷轴
        onUsageWisdom(count)
        if not should_continue:
            sys.exit()
        # 使用重铸石
        onUsageScouring(count)
        if not should_continue:
            sys.exit()
        # 使用制图钉
        onUsageChisel(count)
        if not should_continue:
            sys.exit()
        # 使用点金石
        onUsageAlchemy(count)
        if not should_continue:
            sys.exit()
        # 词缀判断
        for i in range(count):
            if not should_continue:
                sys.exit()
            x = int(i / 5) * 55
            y = i % 5 * 55
            # 移动到背包指定位置
            poe.onCopyBackpack(x, y)
            # 判断词缀
            item_description = pyperclip.paste()
            # 判断是否有不想要的词缀
            pattern = r"冷却回复率总降|药剂充能降低"
            while re.search(pattern, item_description):
                # 重铸点金
                onScouringAndAlchemy(x, y)
                # 重新获取词缀
                item_description = pyperclip.paste()

            # 判断稀有度
            match = re.search(r"\+(\d+)%", item_description)
            while match:
                number = int(match.group(1))
                if number > 70:
                    break
                else:
                    onScouringAndAlchemy(x, y)
                    # 重新获取词缀
                    item_description = pyperclip.paste()
                    match = re.search(r"\+(\d+)%", item_description)

        # 使用瓦尔宝石
        onUsageVaal(count)

    else:
        print(f"未找到标题为 '{target_title}' 的窗口")
