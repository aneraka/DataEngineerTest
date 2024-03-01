from fastapi import APIRouter
from app.apps.auth.core.authentication import JWTBearer
from fastapi import File, UploadFile, Depends
from ..core.handlers import upload_file
from .serializers import UploadSerializer,Backup
from ..core.backup import backup


router = APIRouter()


@router.post('/file_upload', dependencies=[Depends(JWTBearer())])
def receive_post_data(serializer: UploadSerializer = Depends(), file: UploadFile = File(...)):
    serializer = serializer.dict()
    upload_file(    
            type_table=serializer['type_table'],
            file=file
        )
    return {'status_code': 200,
            'msg':'Data upload',
            'files':file.filename}

@router.post('/backup', dependencies=[Depends(JWTBearer())])
def receive_post_data(serializer: Backup = Depends()):
    serializer = serializer.dict()
    x = backup( 
            type_action=serializer['type_action'],
            type_table=serializer['type_table'])
    

    
    return {'status_code': 200,
            'msg':x.result}
    
