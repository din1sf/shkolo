from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os

url = 'https://app.shkolo.bg/dashboard/'

options = Options()
options.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

# load the cookie string from the file
with open('cookies.txt', 'r') as file:
    cookie_string = file.read()
individual_cookies = cookie_string.split(';')
cookies = []
print('Cookies')
for cookie in individual_cookies:
    trimmed_cookie = cookie.strip()
    name, value = trimmed_cookie.split('=', 1)
    print(f'Name: {name}, Value: {value}')
    cookies.append({'name': name, 'value': value})

driver = webdriver.Chrome(options=options)
driver.get(url)
for cookie in cookies:
    driver.add_cookie(cookie)

'''
<form class="login-form" action="/auth/login" method="post" novalidate="novalidate">
                    <input type="hidden" name="_token" value="UcXGdokhMbTbMfIjDGbEhBSyoPPzoJ0ISzZhy27r">
                                        <div class="alert alert-danger  show-toastr" style="display: block;">
        Сесията Ви е изтекла. Въведете данните отново.
                    <button type="button" class="close" data-dismiss="alert" aria-hidden="true"></button>
            </div>
    
                        <div class="form-group">
                        <div class="input-icon">
                            <i class="fas fa-user"></i>
                            <input id="login-username" class="form-control placeholder" type="text" autocomplete="off" placeholder="Имейл или потребителско име" name="login" value="">
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="input-icon">
                            <i class="fas fa-lock"></i>
                            <i class="fas fa-eye showPass" data-for="passwordField"></i>
                            <input class="form-control placeholder" type="password" autocomplete="off" placeholder="Парола" name="password" id="passwordField">
                        </div>
                    </div>

                    <div class="form-actions" style="padding-bottom: 10px;">
                        <button type="submit" class="btn btn-lg btn-block uppercase btn-success">ВХОД</button>
                    </div>

                    
    
</div>
                </form>
'''
time.sleep(20)
newcookies = driver.get_cookies()
print('New cookies')
# iterate each cookie and print their name and value
for cookie in newcookies:
    print(f'Name: {cookie["name"]}, Value: {cookie["value"]}')

# try to find the login form
try:
    _username = os.environ.get("SHKOLO_USER")
    _password = os.environ.get("SHKOLO_PASSWORD")
    print(f'Username: {_username}')  

    login_form = driver.find_element(By.XPATH, '//form[@class="login-form"]')
    print('Login form found')
    username_element = driver.find_element(By.XPATH, '//input[@id="login-username"]')
    if username_element:
        username_element.send_keys(_username)
        password = driver.find_element(By.XPATH, '//input[@id="passwordField"]')
        password.send_keys(_password)
        login = driver.find_element(By.XPATH, '//button[@type="submit"]')
        time.sleep(10)
        login.click()
        print('Login button clicked')
        time.sleep(10)
    
        # get cookies value
        cookies = driver.get_cookies()
        cookies_string = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        print(cookies_string)
        #print(driver.page_source)
except NoSuchElementException:
    print('Login form not found')

time.sleep(20)
driver.quit()
print('Done')   

