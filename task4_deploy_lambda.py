import os
import pathlib
import tempfile
import shutil
import boto3

AWS_REGION = 'eu-central-1'
BASE = pathlib.Path().resolve()
SESSION = boto3.Session(profile_name='task4_deploy')
LAMBDA_SRC = os.path.join(BASE, 'src')
IAM_CLIENT = SESSION.client('iam')
LAMBDA_CLIENT = SESSION.client('lambda', region_name = AWS_REGION)
with tempfile.TemporaryDirectory() as td:
    lambda_archive_path = shutil.make_archive(td, 'zip', root_dir=LAMBDA_SRC)
    zipped_code = None
    with open(lambda_archive_path, 'rb') as f:
        zipped_code = f.read()
    role = IAM_CLIENT.get_role(RoleName='task3-role-zakaria-jokharidze')

    response = LAMBDA_CLIENT.create_function(
        FunctionName='task4_lambdazakaria_jokharidze',
        Runtime='python3.9',
        Role=role['Role']['Arn'],
        Handler='task4_function.lambda_handler',
        Code=dict(ZipFile=zipped_code),
        Timeout=300
    )

    print(response)