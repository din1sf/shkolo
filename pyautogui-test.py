import pyautogui
import time
from pyautogui import hotkey, click, typewrite, displayMousePosition


# open new terminal from spotlight search
time.sleep(1)
pyautogui.keyDown('command')
pyautogui.press('space')
pyautogui.keyUp('command') 
time.sleep(1)
typewrite('terminal')
time.sleep(1)
pyautogui.press('enter')
time.sleep(1)
pyautogui.keyDown('command')
pyautogui.press('n')
pyautogui.keyUp('command') 

# type in terminal
time.sleep(1)
typewrite('ls -l')
pyautogui.press('enter')
time.sleep(1) 
import pyautogui
import time
from pyautogui import hotkey, click, typewrite, displayMousePosition


def open_spotlight():
    time.sleep(1)
    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command') 
    time.sleep(1)

def open_app(app_name):
    open_spotlight()
    typewrite(app_name)
    time.sleep(1)
    pyautogui.press('enter')

def open_terminal():
    open_app('terminal')
                
def open_chrome():
    open_app('Google Chrome')
    
def open_page_and_login():
    time.sleep(1)
    pyautogui.write('ttps://app.shkolo.bg')
    hotkey('enter')
    time.sleep(10)
    pyautogui.moveTo(247, 483)       
    pyautogui.click()
    time.sleep(10)

def open_new_screen():
    pyautogui.keyDown('command')
    pyautogui.press('n')
    pyautogui.keyUp('command')
    time.sleep(1)

def chrome_full_screen():
    time.sleep(1)
    pyautogui.keyDown('fn')
    pyautogui.press('f')
    pyautogui.keyUp('fn')
    time.sleep(1)

def quit_app():
    time.sleep(1)
    pyautogui.keyDown('command')
    pyautogui.keyDown('q')
    time.sleep(2)
    pyautogui.keyUp('command')
    pyautogui.keyUp('q')
    
def copy_cookies():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('shift')
    pyautogui.press('k')
    time.sleep(1)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('shift')
    time.sleep(1)

def save_and_exit_vi():
    time.sleep(1)
    pyautogui.write(':wq')
    pyautogui.press('enter')
    time.sleep(1)

def selectAll():
    time.sleep(1)
    pyautogui.hotkey('command', 'a')
    time.sleep(1)

def copy():
    time.sleep(1)
    pyautogui.hotkey('command', 'c')
    time.sleep(1)

def paste():
    time.sleep(1)
    pyautogui.hotkey('command', 'v')
    time.sleep(1)

def save_cookies_to_file():
    time.sleep(2)
    pyautogui.write('vi login.txt')
    pyautogui.press('enter')    
    time.sleep(2)
    pyautogui.write('ggVG')
    time.sleep(2)
    pyautogui.press('delete')    
    paste()
    time.sleep(2)
    save_and_exit_vi()
    time.sleep(3)

time.sleep(1)

'''
open_chrome()
chrome_full_screen()
open_new_screen()
open_page_and_login()
copy_cookies()
chrome_full_screen()
quit_app()
'''

open_terminal()
open_new_screen()
save_cookies_to_file()

print('Login successful')
