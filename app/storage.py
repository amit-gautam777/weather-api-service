import boto3
import aiofiles
from aiobotocore.session import get_session
from typing import Optional

BUCKET_NAME = "your_bucket_name"

async def save_to_s3(filename: str, data: str) -> None:
    session = get_session()
    async with session.create_client('s3') as s3:
        try:
            await s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=data)
        except Exception as e:
            print('error', e)
            return


async def load_from_s3(filename: str) -> Optional[str]:
    session = get_session()
    async with session.create_client('s3') as s3:
        try:
            response = await s3.get_object(Bucket=BUCKET_NAME, Key=filename)
            async with response['Body'] as stream:
                return await stream.read()
        except s3.exceptions.NoSuchKey:
            print('File not found in S3')
            return None
        except Exception as e:
            print('error', e)
            return None
