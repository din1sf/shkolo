from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import boto3
import time
import json
from botocore.exceptions import NoCredentialsError
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os


def read_last_data_as_json(bucket):
    return read_json_data(bucket, 'last.json')

def read_prev_data_as_json(bucket):
   return read_json_data(bucket, 'prev.json')

def read_json_data(bucket, key):
    data = read_from_s3(bucket, key)
    return json.loads(data)

def read_from_s3(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode('utf-8')

def save_date_to_s3(bucket, key, date):
    with open(key, 'w', encoding='utf-8') as file:
        file.write(date)
    upload_to_s3(key, bucket, key)

def upload_status_to_s3(bucket, status):
    key = 'status.txt'
    with open(key, 'w', encoding='utf-8') as file:
        file.write(status)
    upload_to_s3(key, bucket, key)

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
    
def download_cookies_from_s3(bucket, key):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, 'cookies.txt')
        print('Cookies downloaded from s3') 
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")


def load_cookies():
    download_cookies_from_s3('shkolo-api', 'cookies.txt')

    with open('cookies.txt', 'r') as file:
        cookie_string = file.read()
    individual_cookies = cookie_string.split(';')
    cookies = []
    for cookie in individual_cookies:
        trimmed_cookie = cookie.strip()
        name, value = trimmed_cookie.split('=', 1)
        cookies.append({'name': name, 'value': value})
    return cookies

def scrape_shkolo():
    url = 'https://app.shkolo.bg/dashboard/'

    options = Options()
    options.add_argument("Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
    options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # load the cookie string from the file
    cookies = load_cookies()

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(10)

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

    statistics = {}
    dashboards = driver.find_elements(By.XPATH, '//div[@class="col-md-2 col-sm-4 col-xs-6"]')   
    for dashboard in dashboards:
        desc = dashboard.find_element(By.XPATH, './/div[@class="desc"]').text
        number = dashboard.find_element(By.XPATH, './/div[@class="number"]').text
        statistics[desc] = number

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

    rank_boxes = driver.find_elements(By.XPATH, '//div[@class="col-sm-4 col-xs-6 stats-rank-box cursor-pointer centered-text"]')
    for rank_box in rank_boxes:
        stats_rank = rank_box.find_element(By.XPATH, './/div[@class="stats-rank"]').text.strip()
        stats_label = rank_box.find_element(By.XPATH, './/div[@class="stats-label"]').text.strip()
        statistics[stats_label] = stats_rank

    print(statistics)
    time.sleep(5)

    # Find the element with the text 'Успех'
    success_element = driver.find_element(By.XPATH, "//div[contains(text(), 'Успех')]")
    if success_element:
        success_element.click()

    time.sleep(10)

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

        grades.append({'subject': course, 'term1' : {'final': term1Final, 'current': term1Current}, 'term2' : {'final': term2Final, 'current': term2Current}, 'year': final})

    result = {
        'statistics': statistics,
        'subjects': grades
    }

    driver.quit()
    return result

# format the current term grades
def format_current_term_grades(data, selected_term):
    term_subjects = {}
    for subject in data['subjects']:
        term_subjects[subject['subject']] = subject[selected_term]['current']
        
    result = {}
    result['statistics'] = data['statistics']
    result['subjects'] = term_subjects
    
    return result

# use langchain to compare the grades and prepare human readable response
def compare_grades(prev, current):
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in the environment variable OPENAI_API_KEY")
    llm = ChatOpenAI(openai_api_key=openai_api_key)

    # You want to compare the success, the number of grades, the number of absences, the number of reviews, the number of tests, the number of parent meetings, the place in the parallel and the place in the class. You also want to compare the grades in the different subjects. You want to compare the grades in Bulgarian language and literature, English language, Spanish language, Mathematics, Civil education, Physical education and sports, English language (IUCH - PP), Module 1 - Oral communication (IUCH - PP (task module)) (English language), Module 2 - Written communication (IUCH - PP (task module)) (English language), Module 3 - Language through literature (IUCH - PP (task module)) (English language), Module 4 - Culture and intercultural communication (IUCH - PP (task module)) (English language), Business English (IUCH - PP (elective module)) (English language), Spanish language (IUCH - PP), Module 1 - Oral communication (IUCH - PP (task module)) (Spanish language), Module 2 - Written communication (IUCH - PP (task module)) (Spanish language), Spanish language and culture through literature and new technologies (IUCH - PP (elective module)) (Spanish language), Mathematics (IUCH - PP), Module 1 - Geometry (IUCH - PP (task module)) (Mathematics), Module 2 - Elements of mathematical analysis (IUCH - PP (task module)) (Mathematics), Research tasks with parameter (IUCH - PP (elective module)) (Mathematics), Information technology (IUCH - PP), Module 1 - Data processing and analysis (IUCH - PP (task module)) (Information technology), Module 2 - Multimedia (IUCH - PP (task module)) (Information technology), Automated customer contact systems (IUCH - PP (elective module)) (Information technology), Physics and astronomy (IUCH - PP), History of astronomy (IUCH - PP (elective module)) (Physics and astronomy), Football (FUCH - DP/DUP), Sports activities (football) (…), Traffic safety (…), Class hour (…). You want to compare the grades in the different subjects. You want to compare the grades in Bulgarian language and literature, English language, Spanish language,
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a parent who wants to compare the grades of your child. You have two sets of grades old and new, which are gathered from two days. You want to compare the statistics of the two sets of grades and the grades in the different subjects by give only the differences. Translate the statistics and subjects in English. Answers and should be in English in a good understandable language. If there is no changes in the statistics just answer 'No changes in statistics'. If there is no changes in the grades in the different subjects just answer 'No changes in subjects"),
        ("user", "Compare the old grades {old_grades} with the new grades {new_grades}")
    ])

    chain = prompt | llm 
    result = chain.invoke({"old_grades": prev, "new_grades": current})
    return result.content

# scrape shkolo web site
result = scrape_shkolo()
json_str = json.dumps(result, indent=4, ensure_ascii=False)
current_term_data = format_current_term_grades(result, 'term2')
print(current_term_data)

# Format the date as YYYY-MM-DD
current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

filename = formatted_date + '.json'
filepath = './history/' + filename
with open(filepath, 'w', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
print(f"Data saved to {filepath}")
with open('last.json', 'w', encoding='utf-8') as file:
    json.dump(current_term_data, file, indent=4, ensure_ascii=False)

# upload
bucket = 'shkolo-api'

uploaded = upload_to_s3(filepath, bucket, filename)

last_date = read_from_s3(bucket, 'last')
print(f'Last uploaded date: {last_date}')
prev_data = {}

if last_date != formatted_date:
    prev_date = last_date
    print("Different date. Move last to prev and save new date. Prev: " + prev_date + " Last: " + formatted_date)

    # read last data and save it to prev
    prev_data = read_last_data_as_json(bucket)
    with open('prev.json', 'w', encoding='utf-8') as file:
        json.dump(prev_data, file, indent=4, ensure_ascii=False)
    upload_to_s3('prev.json', bucket, 'prev.json')

    save_date_to_s3(bucket, 'prev', last_date)
    save_date_to_s3(bucket, 'last', formatted_date)
else:
    print("Same date. No need to move last to prev.")
    prev_data = read_prev_data_as_json(bucket)    
    prev_date = read_from_s3(bucket, 'prev')

uploaded = upload_to_s3('last.json', bucket, 'last.json')

# format date string in yyyy-mm-dd to human readable text contains the day, month and year
prev = datetime.strptime(prev_date, "%Y-%m-%d").strftime("%d %B %Y")
now = current_date.strftime("%d %B %Y")
status_header = "Status as of " + now + " comparing with " + prev + ".\n"

# compare with langchain
status = status_header + compare_grades(prev_data, current_term_data)
print(status)
upload_status_to_s3(bucket, status)

print('Done')
