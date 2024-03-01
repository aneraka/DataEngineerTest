from fastapi import APIRouter
from app.apps.auth.core.authentication import JWTBearer
from fastapi import File, UploadFile, Depends
from ..core.handlers import upload_file
from .serializers import UploadSerializer


router = APIRouter()


@router.post('/file_upload', dependencies=[Depends(JWTBearer())])
def receive_post_data(serializer: UploadSerializer = Depends(), file: UploadFile = File(...)):
    serializer = serializer.dict()

    return {'status_code': 200,
            'msg':'Data upload',
            'files':file.filename}

    # return {
    #     "payload": serializer,
    #     "uploaded": upload_file(
    #         type_table=serializer['type_table'],
    #         file=file
    #     ),
    #     "files": file.filename,
    # }
