import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
import json

def format_data(data, selected_term):
    term_subjects = {}
    for subject in data['subjects']:
        term_subjects[subject['subject']] = subject[selected_term]['current']
        
    result = {}
    result['Статистика'] = data['statistics']
    result['Оценки'] = term_subjects
    return result

def save_date_to_s3(bucket, key, date):
    with open(key, 'w', encoding='utf-8') as file:
        file.write(date)
    upload_to_s3(key, bucket, key)

def read_from_s3(bucket, key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read().decode('utf-8')

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

bucket = 'shkolo-api'
last_date = read_from_s3(bucket, 'last')
print(f'Last date: {last_date}')
last_content = read_from_s3(bucket, last_date + '.json')
last_content = json.loads(last_content)
# print(last_content)

formated_data = format_data(last_content, 'term2')
print(formated_data)