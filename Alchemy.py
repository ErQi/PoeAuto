import time
import pyautogui
import pygetwindow as gw
import win32gui
import pyperclip
import re
import keyboard
import threading
import sys


class PathOfExile:
    def __init__(self, window):
        self.window = window
        self.window_x_offset = 0  # 初始偏差为0
        self.window_y_offset = 0  # 初始偏差为0
        self.sleep = 0.098

    def calculate_offsets(self):
        # 获取窗口左上角的坐标
        left, top, _, _ = win32gui.GetClientRect(self.window._hWnd)  # 使用窗口对象的 _hWnd 属性获取句柄
        self.window_x_offset, self.window_y_offset = win32gui.ClientToScreen(self.window._hWnd, (left, top))

    def apply_offsets(self, x, y):
        # 应用偏差值，将窗口内坐标转换为桌面坐标
        x += self.window_x_offset
        y += self.window_y_offset
        return x, y

    def onClickToItem(self):
        # 点击中间的装备
        x, y = self.apply_offsets(365, 530)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.click()

    def onAlchemy(self):
        # 点点金
        x, y = self.apply_offsets(522, 296)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作

    def onClickScouring(self):
        # 点重铸
        x, y = self.apply_offsets(463, 540)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作


global should_continue
should_continue = True


def onAutoAlchemy():
    # 使用窗口点击工具对象来执行点击操作
    poe.onAlchemy()
    # 操作待修改的物品
    poe.onClickToItem()
    # 复制装备信息
    pyautogui.hotkey('ctrl', 'c')


def onAutoScouring():
    # 使用窗口点击工具对象来执行点击操作
    poe.onClickScouring()
    # 操作待修改的物品
    poe.onClickToItem()


def on_key_event(event):
    global should_continue
    if event.name == 'f1':
        print("按下f1键，退出循环")
        keyboard.unhook_all()  # 停止监听所有按键事件
        should_continue = False


def listen_for_esc_key():
    keyboard.on_release(on_key_event)
    keyboard.wait()


if __name__ == '__main__':
    # 获取目标窗口
    target_title = "Path of Exile"  # 用你要操作的窗口标题替换
    target_window = gw.getWindowsWithTitle(target_title)

    count = 0

    if len(target_window) > 0:
        target_window = target_window[0]
        # 窗口最前方显示
        target_window.activate()
        time.sleep(1)

        # 创建一个窗口点击工具对象，将窗口作为参数传递
        poe = PathOfExile(target_window)

        # 计算偏差值
        poe.calculate_offsets()

        # 子线程进行监听退出按键
        listener_thread = threading.Thread(target=listen_for_esc_key)
        listener_thread.start()

        while should_continue:
            # 先点击重铸
            onAutoScouring()
            # 再点击点金
            onAutoAlchemy()

            item_description = pyperclip.paste()

            # 判断稀有度,根据稀有度后面决定是重铸还是改造
            if "稀 有 度: 稀有" in item_description:
                count += 1
                isRarer = True
                pattern = r"需求:\r\n等级: \d+\r\n-{8}"
                change_item = re.sub(pattern, "", item_description, count=1)
                pattern = r"-+\r\n(.*?)\r\n-+"
                matches = re.findall(pattern, change_item, re.DOTALL)

                print(f"------- \t第{count}次点金 \t ------- ")
                print(matches[1])
                print()

                if not should_continue:
                    break

                # 定义字段与对应条件和操作的字典
                pattern = r"增加的天赋为"
                matches = re.findall(pattern, matches[1])
                should_continue = len(matches) < 3


    else:
        print(f"未找到标题为 '{target_title}' 的窗口")
