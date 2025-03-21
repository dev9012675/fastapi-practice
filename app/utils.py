from passlib.context import CryptContext
from fastapi import UploadFile
import soundfile
import os

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)

async def create_file(path:str , file:UploadFile):
     if not os.path.exists(path):
        os.makedirs(path)

     with open(f'{path}/{file.filename}' , 'wb') as disk_file:
        file_bytes = await file.read()
        disk_file.write(file_bytes)

     AudioFile = (f'{path}/{file.filename}')
     data, samplerate = soundfile.read(AudioFile)
     soundfile.write(AudioFile, data, samplerate, subtype='PCM_16')