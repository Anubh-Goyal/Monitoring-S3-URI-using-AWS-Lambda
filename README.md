# Monitoring-S3-URI-using-AWS-Lambda
Monitoring S3 URI using AWS Lambda

Using AWS lambda, write a program to monitor an S3 Uri. Whenever a user uploads data into the S3 storage, the program should capture the details. At the end of the day the program must send out an email to select users displaying the following information:
S3 Uri 
Object Name 
Object Size 
Object type 

1.  Create S3 Bucket with default settings.
    1. Update the bucket policy in json format which will allow the lambda to have getObject access.
2. Configure sender and recipient email ids to send notification to select users.
    1. Configure identities in SES for each email.
    2. Verify the sender and recipient email Id’s.
3. Create Execution Role for Lambda in IAM Console.
    1. Add below predefined policies to this role:
        1. AmazonS3FullAccess
        2. AmazonSESFullAccess
    2. Create new Inline Policy to invoke the lambda function, as it’s not predefined.
4. Configure a lambda function.
    1. Select Language as Python 3.9
    2. Set the Timeout to 1 min
    3. Add the execution role which we created in Step 3 to the above created lambda.
5.  Define Lambda function
    1. Create a S3 and SES Clients
    2. Get Today’s Date in IST
    3. Initiate objects_uploaded Array
    4. Call s3 list objects API for the bucket created
    5. Iterate through the S3 objects if object created on today’s date, then append  S3_uri, object name, size, type to objects_uploaded
        1. We have converted the object size in Kilobytes.
    6. If objects_uploaded are not null, we send this data using ses_client from sender email to recipient email id’s.
6. Configure a scheduled event in Amazon EventBridge to trigger this lambda at midnight everyday.
    1. Create schedule
        1. Give schedule name and description.
        2. Select ‘Recurring schedule’ as the schedule pattern
        3. Set cron pattern
        4. Set start date and end date under ‘Timeframe’
    2. Create Target
        1. Select target API as ‘All API’s’
        2. Configure AWS Lambda as AWS service and select Invoke as API.
        3. Select the Lambda function which we have created in Step 5.
    3. Create new role for this schedule since EventBridge Scheduler requires permission to send events to the target.
