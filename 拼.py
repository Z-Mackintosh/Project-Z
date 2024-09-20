import pyperclip
import pyautogui
import time
import keyboard
import threading

def has_selection():
    # 保存原始剪贴板内容
    original_clipboard = pyperclip.paste()
    
    # 尝试复制选中的内容
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)  # 短暂等待以确保复制完成
    
    # 检查是否有新的选中内容
    new_clipboard = pyperclip.paste()
    
    # 恢复原始剪贴板内容
    pyperclip.copy(original_clipboard)
    
    return new_clipboard != original_clipboard

def convert_pinyin():
    # 保存原始剪贴板内容
    original_clipboard = pyperclip.paste()
    
    # 复制选中的拼音
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)  # 增加等待时间，确保复制完成
    
    pinyin = pyperclip.paste()
    
    # 检查是否成功复制了新内容
    if pinyin == original_clipboard:
        print("未检测到新的选中内容")
        return
    
    # 切换到中文输入模式
    pyautogui.press('shift')
    
    # 模拟键盘输入拼音
    pyautogui.write(pinyin)
    
    # 删除原来选中的拼音
    pyautogui.hotkey('ctrl', 'x')
    
    # 恢复原始剪贴板内容
    pyperclip.copy(original_clipboard)

is_converting = False
lock = threading.Lock()

def on_alt_press(event):
    global is_converting
    with lock:
        if has_selection() and not is_converting:
            is_converting = True
            threading.Thread(target=convert_pinyin).start()
            return False
    return True

def on_alt_release(event):
    global is_converting
    with lock:
        is_converting = False

# 监听 Alt 键
keyboard.on_press_key('alt', on_alt_press, suppress=True)
keyboard.on_release_key('alt', on_alt_release)

print("程序已启动，按 Ctrl+C 退出")
try:
    # 使用一个简单的循环来保持程序运行
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("程序已退出")