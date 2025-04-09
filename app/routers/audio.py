from fastapi import  status , HTTPException , Depends , APIRouter , UploadFile , Body
from .. import  utils , oauth2 , schemas
import speech_recognition as sr
from os import listdir
from os.path import isfile, join
import pathlib
from fastapi.responses import FileResponse 
import soundfile
from io import BytesIO

router = APIRouter(prefix="/api/audio" ,
                   tags=["Audio"])

@router.post('/transcribe')
async def get_transcription(file:UploadFile , current_user = Depends(oauth2.get_current_user) ):
    r = sr.Recognizer()
    #path = f'files/{current_user.id}'
    #await utils.create_file(path , file)
    #AudioFile = (f'{path}/{file.filename}')
    AudioFile = BytesIO()
    data, samplerate = soundfile.read(BytesIO(await file.read()))
    soundfile.write(AudioFile, data, samplerate, subtype='PCM_16' , format='WAV')
    AudioFile.seek(0)
    with sr.AudioFile(AudioFile) as source:
        audio = r.record(source)
        
    try:
        transcription = r.recognize_google(audio)
    except sr.UnknownValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Could not understand audio')
    except sr.RequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Could not request results from service')
    else:
        return {"transcription":transcription}
    
@router.post('/retrieveFilenames')
async def get_files(audio:schemas.RetrieveFiles , current_user = Depends(oauth2.get_current_user)):
    onlyfiles = [f for f in listdir(audio.path) if isfile(join(audio.path, f))]
    print(f'Files in path are:{onlyfiles}')
    return {"files":onlyfiles}

@router.post('/retrieveFile')
async def get_file(fileToGet:schemas.RetrieveFiles , current_user = Depends(oauth2.get_current_user)):
    file = pathlib.Path(fileToGet.path)
    if file.is_file():
        return FileResponse(fileToGet.path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='File not found')

