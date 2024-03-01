import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

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


local_file = '2024-02-28.json'
bucket = 'shkolo-api'
s3_file = '2024-02-28.json'

# uploaded = upload_to_s3(local_file, bucket, s3_file)
# print(uploaded)

# result = read_from_s3(bucket, s3_file)
# print(result)

'''
current_date = datetime.now()
formatted_date = current_date.strftime("%Y-%m-%d")

prev_date = read_from_s3(bucket, 'prev')
print(f'Previous date: {prev_date}')

last_date = read_from_s3(bucket, 'last')
print(f'Last date: {last_date}')

if last_date != formatted_date:
    print("Different date")
    save_date_to_s3(bucket, 'prev', last_date)
    save_date_to_s3(bucket, 'last', formatted_date)
'''

# save_date_to_s3(bucket, 'last', '2024-02-28')
print('done')

