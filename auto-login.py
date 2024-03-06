import pyautogui
import time
import json
import boto3
import os
from pyautogui import hotkey, click, typewrite, displayMousePosition
from botocore.exceptions import NoCredentialsError

def open_spotlight():
    time.sleep(1)
    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command') 
    time.sleep(3)

def open_app(app_name):
    open_spotlight()
    typewrite(app_name)
    time.sleep(1)
    pyautogui.press('enter')

def open_terminal():
    open_app('terminal')
                
def open_chrome():
    open_app('Google Chrome')
    time.sleep(5)
    
def open_chrome_page_from_terminal(site):
    open_terminal()
    time.sleep(1)
    pyautogui.write('open -a "Google Chrome" ' + site)
    hotkey('enter')
    time.sleep(10)
    chrome_full_screen()
    time.sleep(5)
    pyautogui.moveTo(863, 479, duration=1)       
    pyautogui.click()
    time.sleep(10)

def open_page_and_login(site):
    time.sleep(1)
    pyautogui.write(site)   
    hotkey('enter')
    time.sleep(10)
    pyautogui.moveTo(863, 479, duration=1)       
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
    pyautogui.write(':x')
    time.sleep(1)
    pyautogui.press('enter')

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
    pyautogui.write('mkdir -p ~/tmp')
    pyautogui.press('enter')
    time.sleep(2) 
    pyautogui.write('cd ~/tmp')
    pyautogui.press('enter')
    
    pyautogui.write('vi login.json')
    pyautogui.press('enter')    
    time.sleep(2)
    pyautogui.write('ggVG')
    time.sleep(2)
    pyautogui.press('delete')    
    paste()
    time.sleep(2)
    save_and_exit_vi()
    time.sleep(3)

def format_cookies_to_file(filename):
    home_dir = os.path.expanduser("~")
    print(home_dir)
    with open(home_dir + '/tmp/login.json', 'r') as file:
        s = file.read()

    s = s.replace("'", '"')
    cookies = json.loads(s)
    joined_cookies = '; '.join([f'{cookie["name"]}={cookie["value"]}' for cookie in cookies])   
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(joined_cookies)
    print(joined_cookies)

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful. File uploaded to https://{bucket}.s3.amazonaws.com/{s3_file}")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
time.sleep(1)

open_chrome()
chrome_full_screen()
open_new_screen()
open_page_and_login('https://app.shkolo.bg')
copy_cookies()
chrome_full_screen()
quit_app()

open_terminal()
open_new_screen()
save_cookies_to_file()

cookies_file = "cookies.txt"
format_cookies_to_file(cookies_file)
upload_to_s3(cookies_file, 'shkolo-api', cookies_file)

print('Login successful')
