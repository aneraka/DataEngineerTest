from fastapi import APIRouter
from app.apps.auth.core.authentication import JWTBearer
from fastapi import File, UploadFile, Depends
from ..core.handlers import upload_file
from .serializers import UploadSerializer,Backup,Reporte
from ..core.backup import backup
from ..core.reporte import reporte


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

@router.post('/report', dependencies=[Depends(JWTBearer())])
def receive_post_data(data: Reporte = Depends()):
    
    result = reporte('general',data)
    
    return result.result

@router.post('/report/kpi1', dependencies=[Depends(JWTBearer())])
def receive_post_data():
    proceso = reporte()
    return     proceso.kpi1()

@router.post('/report/kpi2', dependencies=[Depends(JWTBearer())])
def receive_post_data():
    proceso = reporte()
    return     proceso.kpi2()
    
    
@router.get('/report/getDimensions', dependencies=[Depends(JWTBearer())])
def receive_post_data():
    
    return {'status_code': 200,
            'msg':{'department_id':'Department\'s id',
                   'department':'name of department',
                   'job_id':'Job\'s id',
                   'job':'name od job',
                   'year':'year of hired',
                   'month':'month of hired',
                   'quater':'quarter of hired'}}  

@router.get('/report/getMetrics', dependencies=[Depends(JWTBearer())])
def receive_post_data():
    
    return {'status_code': 200,
            'msg':{'employee_quantity'}}