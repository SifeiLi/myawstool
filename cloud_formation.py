import cloud_formation_helper


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_SESSION_TOKEN = ''


# Test
cf_helper = cloud_formation_helper.CloudFormationHelper(region='us-east-2', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                                        aws_session_token=AWS_SESSION_TOKEN)
cf_helper.delete_specified_stacks("^EFS", 'CREATE_COMPLETE')
