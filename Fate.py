import time

import integer
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
        self.sleep = 0.068

    def calculate_offsets(self):
        # 获取窗口左上角的坐标
        left, top, _, _ = win32gui.GetClientRect(self.window._hWnd)  # 使用窗口对象的 _hWnd 属性获取句柄
        self.window_x_offset, self.window_y_offset = win32gui.ClientToScreen(self.window._hWnd, (left, top))

    def apply_offsets(self, x, y):
        # 应用偏差值，将窗口内坐标转换为桌面坐标
        x += self.window_x_offset
        y += self.window_y_offset
        return x, y

    def onClickFate(self):
        # 点击命运卡
        x, y = self.apply_offsets(290, 720)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()

    def onPlaceFate(self, x, y):
        # 点改造
        x, y = self.apply_offsets(1625 + x, 650 + y)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.keyDown('ctrl')
        pyautogui.click()
        pyautogui.keyUp('ctrl')

    def onConvertFate(self):
        x, y = self.apply_offsets(800, 500)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.keyDown('ctrl')
        pyautogui.click()
        pyautogui.keyUp('ctrl')

    def onClickTrading(self):
        x, y = self.apply_offsets(790, 780)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.click()

global should_continue
should_continue = True


def on_key_event(event):
    global should_continue
    if event.name == 'f1':
        print("按下f1键，退出循环")
        keyboard.unhook_all()  # 停止监听所有按键事件
        should_continue = False
        sys.exit()  # 退出程序


def listen_for_esc_key():
    keyboard.on_release(on_key_event)
    keyboard.wait()


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

        # 创建一个窗口点击工具对象，将窗口作为参数传递
        poe = PathOfExile(target_window)

        # 计算偏差值
        poe.calculate_offsets()

        # 点击次数
        integer
        click = 0;
        while should_continue:
            # # 点击命运卡
            # poe.onClickFate()
            #
            # # 放置命运卡
            # x, y = 0, 0
            # x = int(click / 5) * 55
            # y = click % 5 * 55
            # print(f'X的值是 {x}  Y的值是{y}')
            # poe.onPlaceFate(x, y)
            # pyautogui.hotkey('ctrl', 'c')
            #
            # # 增加点击计数
            # click += 1
            #
            # if click >= 60:
            #     should_continue = False
            #     break
            # # 获取剪贴板中的文本信息
            # fate_description = pyperclip.paste()
            # print(fate_description)


            # 点击背包命运卡
            x, y = 0, 0
            x = int(click / 5) * 55
            y = click % 5 * 55
            print(f'X的值是 {x}  Y的值是{y}')
            poe.onPlaceFate(x, y)

            # 增加点击计数
            click += 1

            # 点击交易
            poe.onClickTrading()

            # 拿取物品
            poe.onConvertFate()

            if click >= 60:
                should_continue = False
                break


    else:
        print(f"未找到标题为 '{target_title}' 的窗口")
