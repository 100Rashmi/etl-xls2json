import json

import boto3
import config

lambda_client = boto3.client('lambda')
iam_client = boto3.client('iam')

def get_role():
    #get role
    role = None
    try:
        role = iam_client.get_role(RoleName=config.IAM_ROLE_NAME)
    except Exception as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            try:
                # create basic iam role, if not exists
                role_policy_document = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "",
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "lambda.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                }
                role = iam_client.create_role(
                  RoleName=config.IAM_ROLE_NAME,
                  AssumeRolePolicyDocument=json.dumps(role_policy_document),
                )

                # attach policy
                policyArn = ["arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
                               'arn:aws:iam::aws:policy/AmazonS3FullAccess']
                for arn in policyArn:
                    response = iam_client.attach_role_policy(
                        RoleName=config.IAM_ROLE_NAME,
                        PolicyArn= arn
                    )
                    print(response)

            except Exception as ex:
                raise ex

        else:
            raise e
    return role


def delete_and_create_lambda_function():
    #delete lambda function already exist
    try:

        response = lambda_client. delete_function(
            FunctionName=config.LAMBDA_FUNC_NAME
        )
    except Exception as e:
        if e.response['Error']['Code'] == "ResourceNotFoundException":
            pass
        else:
            raise e

    with open('function.zip', 'rb') as f:
      zipped_code = f.read()

    # create lambda function
    role = get_role()
    response = lambda_client.create_function(
        FunctionName=config.LAMBDA_FUNC_NAME,
        Runtime='python3.6',
        Role=role['Role']['Arn'],
        Handler='handlers.mic_hanlder',
        Code={'ZipFile': zipped_code},
        Timeout=900
    )

    print(response)

def init_s3_bucket():
    #create bucket
    s3_client = boto3.client('s3')
    try:
        response = s3_client.create_bucket(
            ACL='private',
            Bucket=config.BUCKET_NAME,
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
    except Exception as e:
        if e.response['Error']['Code'] == "BucketAlreadyOwnedByYou" or e.response['Error']['Code'] == "BucketAlreadyExists":
            pass
        else:
            raise e

# ============ Initialsing AWS Lambda, the role and S3 bucket
init_s3_bucket()
delete_and_create_lambda_function()




