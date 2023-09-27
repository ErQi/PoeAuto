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

    def onClikcAlteration(self):
        # 点改造
        x, y = self.apply_offsets(132, 290)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作

    def onClikcAugmentation(self):
        # 点增幅
        x, y = self.apply_offsets(234, 360)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作

    def onClickRegal(self):
        # 点富豪
        x, y = self.apply_offsets(467, 290)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作

    def onClikcScouring(self):
        # 点重铸
        x, y = self.apply_offsets(463, 540)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作

    def onClickTransmutation(self):
        # 点蜕变
        x, y = self.apply_offsets(70, 290)
        pyautogui.moveTo(x, y, duration=self.sleep)
        pyautogui.rightClick()  # 执行点击操作


global should_continue
should_continue = True


def onAutoAlteration():
    # 使用窗口点击工具对象来执行点击操作
    poe.onClikcAlteration()
    # 操作待修改的物品
    poe.onClickToItem()
    # 模拟执行复制操作（Ctrl+C）
    pyautogui.hotkey('ctrl', 'c')


def onAutoRegal():
    # 先用增幅
    poe.onClikcAugmentation()
    poe.onClickToItem()
    # 再用富豪
    poe.onClickRegal()
    poe.onClickToItem()
    pyautogui.hotkey('ctrl', 'c')


def onAutoAgain():
    # 先用重铸
    poe.onClikcScouring()
    poe.onClickToItem()
    # 再用锐变
    poe.onClickTransmutation()
    poe.onClickToItem()
    # 接着用增幅
    poe.onClikcAugmentation()
    poe.onClickToItem()
    # 复制装备信息
    pyautogui.hotkey('ctrl', 'c')


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

        # 定义字段与对应条件和操作的字典
        field_conditions = {
            "药剂充能使用降低": {"pattern": r"药剂充能使用降低 (\d+)%", "threshold": 10},
            "冷却回复速度加快": {"pattern": r"冷却回复速度加快 (\d+)%", "threshold": 16},
            # 添加其他字段的条件和操作
        }

        isRarer = False

        while should_continue:
            # 获取剪贴板中的文本信息
            item_description = pyperclip.paste()

            # 判断稀有度,根据稀有度后面决定是重铸还是改造
            if "稀 有 度: 稀有" in item_description:
                count += 1
                isRarer = True
                pattern = r"--------\r\n(.*?)\r\n--------"
                matches = re.findall(pattern, item_description, re.DOTALL)

                print(f"------- \t第{count}次富豪 \t ------- ")
                print(matches[2])
                print()
                if "冷却回复" in item_description:
                    should_continue = False
                    break  # 退出循环
            else:
                isRarer = False

            matchCount = 0

            # 使用字典来处理字段
            for field, conditions in field_conditions.items():
                pattern = conditions["pattern"]
                match = re.search(pattern, item_description)

                if match:
                    # 如果匹配成功，获取匹配的数值
                    value = int(match.group(1))

                    # 在这里可以添加条件判断，检查是否满足阈值条件
                    if value >= conditions["threshold"]:
                        if isRarer:
                            # 如果是稀有判断符合次数
                            matchCount += 1
                            continue  # 开始下一次循环
                        else:
                            # 魔法装备直接去富豪
                            onAutoRegal()
                            isRarer = True
                            break  # 退出循环

            # 执行改造
            if isRarer:
                # 判断是刚符合进行了富豪的还是已经进行了富豪,但是富豪不符合的.
                if matchCount == 0:
                    continue  # 没有添加匹配就是刚富豪的,直接下次循环

                if matchCount == 2:
                    should_continue = False
                    print('改造成功,恭喜发财')
                    break
                # 执行重铸 锐变
                onAutoAgain()
            else:
                # 执行改造
                onAutoAlteration()

    else:
        print(f"未找到标题为 '{target_title}' 的窗口")
