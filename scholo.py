from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

url = 'https://app.shkolo.bg/dashboard/'

# load cookies.txt as text file
# with open('cookies.txt', 'r') as file:


options = Options()
options.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

driver.get(url)

# load the cookie string from the file
with open('cookies.txt', 'r') as file:
    cookie_string = file.read()

individual_cookies = cookie_string.split(';')
cookies = []
for cookie in individual_cookies:
    trimmed_cookie = cookie.strip()
    name, value = trimmed_cookie.split('=', 1)
    cookies.append({'name': name, 'value': value})

"""
cookies = [
    {'name': '_ga_H7W8R44FGE', 'value': 'GS1.2.1708844649.1.0.1708844649.0.0.0'},
    {'name': 'cookieconsent_dismissed', 'value': 'yes'},
    {'name': 'browser_fingerprint_id', 'value': 'eyJpdiI6IlVEMWwrb1JtSTRYdXI2R3BwbDNianc9PSIsInZhbHVlIjoiREtoQ0xSSmRMNWxyMW1sS0pMN211R094WW1jZ3p1TmNhZXhzUlpSSHZqdWFRSldUSDhYdFo0bXJvaXAyTTNwb2xMVmtnUCtwL1JWdXVUelR2T0VvRlE9PSIsIm1hYyI6ImFkNDYyZjQyMTRiZjE5ZmRhZDc4ZGM5OWRlMjA2ZGYyY2YwYTg1Nzc0Yzg5N2ZkY2NhNmU2ZjYyOWMxMTcwYWYiLCJ0YWciOiIifQ%3D%3D'},
    {'name': 'remember_customSession_6600ed82abed68d40d649e9d57421fb7eea40782', 'value': 'eyJpdiI6IngzTnovbjhVUUNsc2VwQVdQeFV3RGc9PSIsInZhbHVlIjoieXZwUFJkRElCTjBBc1ZlLzhVRlpNa1l4S1lPUGx6MEdDNXM4eDVEWkZ2T21EamlWRmVMS1MvU3h0NkJzT1RZMXNkWksyV1hDcWVHalA4SWgxUVB6TG1LRFFxazljK1ZkQ0wyL3ltZU1jWjh1NElmaTFWbFVpeGY3ZHZlV1V2bXZwSmdkby9PWU9FWTlucyszU0x2TnhvNUR6bTlTelVMSStFRlBicFp2QXNvTGtKelhzcXBMZ0hyZUtwSHUwOWlzUURHWnl2OVlKTUJabmZXK2gvZm9RamZIREVmT0xmNVRYampwUFEyc2I3MD0iLCJtYWMiOiJlYTY5ZGVmNTVlYWYwNmRjMWNmYTdiY2Y0ZDE5MDIzZmQzZDkzZjZiOTFkMWQ0NzFjYzBmYzg5YWQzNWNlMDgxIiwidGFnIjoiIn0%3D'},
    {'name': 'cf_clearance', 'value': 'wRRPQmSBVZ4j5QH.sEbIfm5jfG8Ac02duPQSZ6nj91w-1709016911-1.0-Adv9mIpI7mwgYprYLNKFGvhr9jgSzCTjloPLNJe8WX26Zb4uyRfwHizgxUZ75YADaJAd5nXw2Zk6+A6x8b2KzmE='},
    {'name': '_gid', 'value': 'GA1.2.1847316888.1709016911'},
    {'name': '_ga', 'value': 'GA1.2.1036306178.1708844649'},
    {'name': 'XSRF-TOKEN', 'value': 'eyJpdiI6IjlKcGJ0RStSTkp0c045UFVZQUhVOWc9PSIsInZhbHVlIjoiZG5tSFRZRERiZ0N1bWRYeXByZ0FvcTZ2U05rYzN0Z2lBUHhRVlcweE5xM1VpVkRpL29yRDIva3k3VkRRQXBaYU12TCttcDlvSjhRYTNiRG9hNVVOMm1ramtPWnZjNGxrZjQ2aGJWSE9iUVVsTzNOckJITWZYa2lFZ1dGam8yenkiLCJtYWMiOiI2YTBhMjljMTA0MjUzNjFlZjBlODAxNmFhMjVkM2NjMTEwNDdhNmRkODBjYTRkNTE0MTViMjg0ZGUyOTY3NTJlIiwidGFnIjoiIn0%3D'},
    {'name': 'shkolo-cookie', 'value': 'eyJpdiI6Ind4RFpQNDh0SUR0RjFqK2E2UGhaWGc9PSIsInZhbHVlIjoiMVk4bVRlQ3BpNmFMU1dRVzE0eXk1c21iL1ovaUk4TE91RFNvVFgxWm5iNnhYQzVLWWxXSHU0S2owc2hQaTdjdkhzMEU3bi80YTBWMFhXeUxNZDEycXBBZU10NGFta0t0d2wzazAxSVRWK2tXa2hEY24vSFdPeGg0NTl0TUFjMXciLCJtYWMiOiIzNDBlYjZjYjM5NjY0NzY0N2E3Yzc3OTVmMmNhNzBiYmJlODE4YmU0MGIyN2FiY2M2YzczYWIyOWU0N2E1YzdkIiwidGFnIjoiIn0%3D'},
    {'name': '_ga_58ZMLS9Y6K', 'value': 'GS1.1.1709021571.6.1.1709021739.60.0.0'}
]
"""
for cookie in cookies:
    driver.add_cookie(cookie)

time.sleep(20)

"""
<div class="col-md-2 col-sm-4 col-xs-6">
        <a class="dashboard-stat dashboard-stat-v2 blue margin-bottom-10" href="/diary/pupil/2300566279#tab_grades">
            <div class="visual"><i class="far fa-chart-line"></i></div>
            <div class="details">
                <div class="number">
                                    <span data-counter="counterup" data-value="5.65">5.65</span>
                                </div>
                <div class="desc">Успех</div>
            </div>
        </a>
    </div>
"""

statistics = []
dashboards = driver.find_elements(By.XPATH, '//div[@class="col-md-2 col-sm-4 col-xs-6"]')   
for dashboard in dashboards:
    desc = dashboard.find_element(By.XPATH, './/div[@class="desc"]').text
    number = dashboard.find_element(By.XPATH, './/div[@class="number"]').text
    link = dashboard.find_element(By.XPATH, './/a').get_attribute('href')
    statistics.append({'desc': desc, 'number': number, 'link': link})

print(statistics)

"""
<div class="portlet-body stats-rank-portlet-body clearfix">
            <div class="col-sm-4 col-xs-6 stats-rank-box cursor-pointer centered-text">
                <div class="rank-value">
        <div class="stats-rank"> 15
            <div class="rank-arrow font-blue-dark"><i class="fas fa-minus"></i></div>
        </div>
        <div class="stats-label"> място в паралелката </div>
    </div>
    <div class="popupText statsRankPopup"><p><strong>Без промяна спрямо предната седмица.</strong><br> От общо 26 ученици.</p> </div>
            </div>
            <div class="col-sm-4 col-xs-6 stats-rank-box cursor-pointer centered-text">
                <div class="rank-value">
        <div class="stats-rank"> 102
            <div class="rank-arrow font-blue-dark"><i class="fas fa-minus"></i></div>
        </div>
        <div class="stats-label"> място във випуска </div>
    </div>
    <div class="popupText statsRankPopup"><p><strong>Без промяна спрямо предната седмица.</strong><br> От общо 192 ученици.</p> </div>
            </div>
            <div class="col-sm-4 col-xs-12 stats-rank-box cursor-pointer centered-text">
                <div class="rank-value">
        <div class="stats-rank"> 380
            <div class="rank-arrow font-blue-dark"><i class="fas fa-minus"></i></div>
        </div>
        <div class="stats-label"> място в училище </div>
    </div>
    <div class="popupText statsRankPopup"><p><strong>Без промяна спрямо предната седмица.</strong><br> От общо 1054 ученици.</p> </div>
            </div>
        </div>
"""
ranks=[]
rank_boxes = driver.find_elements(By.XPATH, '//div[@class="col-sm-4 col-xs-6 stats-rank-box cursor-pointer centered-text"]')
for rank_box in rank_boxes:
    stats_rank = rank_box.find_element(By.XPATH, './/div[@class="stats-rank"]')
    stats_label = rank_box.find_element(By.XPATH, './/div[@class="stats-label"]')
    ranks.append({'stats_rank': stats_rank.text.strip(), 'stats_label': stats_label.text.strip()})

print(ranks)
time.sleep(5)

# Find the element with the text 'Успех'
success_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Успех')]")
success_element.click()
# print("Clicked on 'Успех'")

time.sleep(5)

driver.get("https://app.shkolo.bg/ajax/diary/getGradesForPupil?fromDate=&toDate=&type=0&previousMonth=0&currentMonth=0&currentWeek=0&currentDay=0&includeDeleted=0&pupil_id=2300566279&_=1709021739855")
time.sleep(5)

"""
<tr class="compactTableRow " data-course-id="2300409674">
                        <td class="numVal">
                1
            </td>
            <td>
                                                    <i class="icon-book-open"></i> Български език и литература
                                        </td>
                            <td class="emptyForTerm1 solid-left-border numVal  hide " data-mix_id="" data-target_id="1_20" data-term_id="1">
                    <button class="btn small blue width-100 grade gradeTermFinal grade-button" id="grade_2300000000027263143" data-uid="t1_r1" data-grade-system-id="5">5 </button>                 </td>
                
                <td class="term1 solid-left-border " data-term_id="1">
                    <button class="btn small yellow-lemon grade " id="grade_2300000000007542230">4</button>
                        <button class="btn small green-jungle grade " id="grade_2300000000007542336">6</button>
                        <button class="btn small blue grade  classWorkGrade" id="grade_2300000000021870438">5</button>
                        <button class="btn small blue grade " id="grade_2300000000021871123">5</button>
                    </td>
                
                <td class="numVal term1 " data-mix_id="" data-target_id="1_20" data-term_id="1">
                    <button class="btn small blue width-100 grade gradeTermFinal grade-button" id="grade_2300000000027263143" data-uid="t1_r1" data-grade-system-id="5">5 </button>                 </td>
                            <td class="emptyForTerm2 solid-left-border numVal  hide " data-mix_id="" data-target_id="1_20" data-term_id="2">
                                    </td>
                
                <td class="term2 solid-left-border " data-term_id="2">
                                    </td>
                
                <td class="numVal term2 " data-mix_id="" data-target_id="1_20" data-term_id="2">
                                    </td>
                        
            <td class="emptyAnnual annualAssessment solid-left-border" data-annual_grades_for_all_modules="" data-mix_id="" data-target_id="1_20" data-is_main_course="" data-term_id="2">
                            </td>
        </tr>
"""
grades = []
grade_rows = driver.find_elements(By.XPATH, '//tr[@class="compactTableRow "]')
for grade_row in grade_rows:
    course = grade_row.find_element(By.XPATH, './/td[2]').text

    try:
        term1Final = grade_row.find_element(By.XPATH, './/td[3]/button').text
    except NoSuchElementException:
        term1Final = '' 
    term1Current = []
    for fgcurrent in grade_row.find_elements(By.XPATH, './/td[4]/button'):
        term1Current.append(fgcurrent.text)

    try:
        term2Final = grade_row.find_element(By.XPATH, './/td[6]/button').text
    except NoSuchElementException:
        term2Final = ''
    term2Current = []
    for sgcurrent in grade_row.find_elements(By.XPATH, './/td[7]/button'):
        term2Current.append(sgcurrent.text)

    try:
        final = grade_row.find_element(By.XPATH, './/td[8]/button').text
    except NoSuchElementException:
        final = ''

    grades.append({'course': course, 'term1Final': term1Final, 'term1Current': term1Current, 'term2Final': term2Final, 'term2Current': term2Current, 'final': final})

# print(grades)

result = {
    'ranks': ranks,
    'statistics': statistics,
    'grades': grades
}

json_str = json.dumps(result, indent=4, ensure_ascii=False)
print(json_str)

driver.quit()

# Format the date as YYYY-MM-DD
current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")
filename = formatted_date + '.json'
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)

print(f"Data saved to {filename}")

