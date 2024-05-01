import boto3
import datetime
import json
import os
from botocore.exceptions import ClientError

RECIPIENTS = ['2023mt12076@wilp.bits-pilani.ac.in' , '2022mt13194@wilp.bits-pilani.ac.in' , '2023mt12043@wilp.bits-pilani.ac.in' , 
'2022mt13072@wilp.bits-pilani.ac.in' , '2023mt13062@wilp.bits-pilani.ac.in', 'shwetajalan@wilp.bits-pilani.ac.in']

AWS_SES_SENDER = '2023mt12076@wilp.bits-pilani.ac.in'
    
def lambda_handler(event, context):
    # Create an S3 client
    print("event", event)
    s3 = boto3.client('s3')
    ses = boto3.client('ses', region_name='ap-south-1')
    S3_BUCKET_NAME = 'group2-s3-bucket'

    try:
        utc_now = datetime.datetime.utcnow()
        ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
        today_date = ist_now.strftime('%Y-%m-%d')
        objects_uploaded = []

        response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME)
        for obj in response['Contents']:
            if obj['LastModified'].strftime('%Y-%m-%d') == today_date:
                # Extract object details
                object_name = obj['Key']
                object_size = str(round(obj['Size']/1024, 1)) + " KB"
                object_type = object_name.split('.')[-1] if '.' in object_name else 'Unknown'
                s3_uri = f's3://{S3_BUCKET_NAME}/{object_name}'

                # Append object details to the list
                objects_uploaded.append({
                    'S3 Uri': f's3://{S3_BUCKET_NAME}/{object_name}',
                    'Object Name': object_name,
                    'Object Size': object_size,
                    'Object Type': object_type
                })

    except ClientError as e:
        print(f"Error listing objects: {e.response['Error']['Message']}")

        # Read the contents of the object
        object_data = response['Body'].read().decode('utf-8')

        # Do something with the object data
        print("Object data:", object_data)

# Send email with object details
    if objects_uploaded:
        json_data = json.dumps(objects_uploaded, indent=4)
        subject = f"Notification for S3 Objects Upload | {S3_BUCKET_NAME} | {today_date}"
        send_email(ses, subject, json_data)
        
def send_email(ses_client, subject, body):
    try:
        response = ses_client.send_email(
            Source=AWS_SES_SENDER,
            Destination={'ToAddresses': RECIPIENTS},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"Email sent successfully: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")
    return {
        'statusCode': 200,
        'body': 'Object read successfully'
    }
