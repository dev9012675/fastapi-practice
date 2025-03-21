from fastapi import  status , HTTPException , Depends , APIRouter , UploadFile
from .. import  utils , oauth2
import speech_recognition as sr
import shutil

router = APIRouter(prefix="/api/audio" ,
                   tags=["Audio"])

@router.post('/transcribe')
async def get_transcription(file:UploadFile , current_user = Depends(oauth2.get_current_user) ):
    r = sr.Recognizer()
    path = f'files/{current_user.id}'
    await utils.create_file(path , file)
    AudioFile = (f'{path}/{file.filename}')
    with sr.AudioFile(AudioFile) as source:
        audio = r.record(source)
        
    try:
        transcription = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + transcription)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Could not understand audio')
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Could not request results from service')
    else:
        shutil.rmtree(path)
        return {"transcription":transcription}
   

