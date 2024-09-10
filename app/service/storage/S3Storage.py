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
    

    async def upload_file_content(self, directory_path: str, file_name: str, content: dict, contentType: str):
        # Create the key (path to the file)
        key = f"{directory_path}/{file_name}"

        try:
            # Upload the file to S3 with the JSON content
            upload_file =  self.s3.put_object(
                Bucket=os.getenv('AWS_S3_BUCKET'),
                Key=key,
                Body=content,
                ContentType=contentType
            )
            return upload_file
        except Exception as e:
            print(f"Error uploading file to S3: {e}")
            return None
            
    
    async def get_file(self, directory_path: str, file_name: str):
        try:
            key = f"{directory_path}/{file_name}"
            response = self.s3.get_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=key)
            
            content = response['Body'].read().decode('utf-8')
            return content
        except Exception as e:
            print(f"Error fetching file content: {e}")
            return None
    

    async def delete_file(self, directory_path: str, file_name: str):
        try:
            key = f"{directory_path}/{file_name}"
            response = self.s3.delete_object(Bucket=os.getenv('AWS_S3_BUCKET'), Key=key)
            return response
        except Exception as e:
            print(f"Error deleting file '{key}': {e}")
            return None
