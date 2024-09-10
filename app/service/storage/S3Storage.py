import boto3
from botocore.exceptions import NoCredentialsError
from app.service.storage.base import FileStorage
import os

class S3Storage(FileStorage):
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            endpoint_url=os.getenv("AWS_S3_URL"),
            region_name=os.getenv("AWS_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    
    async def upload_file(self, file_path: str, object_name: str):
        try:
            self.s3.upload_file(file_path, 'my-bucket', object_name)
            print(f"File '{file_path}' uploaded as '{object_name}'.")
        except NoCredentialsError:
            print("Credentials not available.")
            
    
    async def get_file(self, object_name: str, download_path: str):
        try:
            self.s3.download_file('my-bucket', object_name, download_path)
            print(f"File '{object_name}' downloaded to '{download_path}'.")
        except NoCredentialsError:
            print("Credentials not available.")
