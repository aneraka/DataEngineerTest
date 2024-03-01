import os
import traceback
from io import StringIO
from datetime import datetime
from fastapi import HTTPException
from .constants import S3_FOLDER
from .utils import get_df, transform
from app.config.connections import conn_bd
from app.common import constants, handlers

S3_FOLDER: str = S3_FOLDER

def write_transformed(
        utc_time: str,
        file: dict,
        source_route: str,
        type_table: str
):  

    output = get_df(
        data=file['contents']
    )
    
    output,output_bad = transform(
        data=output,
        type_table=type_table
    )
    
    if not output_bad.empty:

        string = StringIO()

        output_bad.to_csv(string, index=False)
        
        file['contents'] = string.getvalue()
        file['extension'] = '.csv'

        #insertar en bd
        print('asd')
        handlers.UploadHandler.write_to_s3(
            utc_time,
            file,
            type_table,
            'bad'
        )

    
    if not output.empty:

        string = StringIO()

        output.to_csv(string, index=False)
        
        file['contents'] = string.getvalue()
        file['extension'] = '.csv'

        #insertar en bd
        print('good file')
        handlers.UploadHandler.write_to_s3(
            utc_time,
            file,
            type_table,
            'good'
        )
        return output
    
    else:
        return None
    

def upload_file(type_table: str, file):
    now2 = datetime.utcnow()
    now = now2.strftime(constants.DATETIME_FORMAT)
    file_data = handlers.UploadHandler.file_contents(file)

    try:
        print('source')
        uploaded = handlers.UploadHandler.write_to_s3(
            now,
            file_data,
            type_table,
            'source'
        )

    except Exception as e:
        raise HTTPException(
            status_code=512,
            detail="Source error with: " + str(traceback.format_exc())
        )
    

    try:
        transformed = write_transformed(
            utc_time=now,
            file=file_data,
            source_route=uploaded['path'],
            type_table=type_table
        )

        if transformed is not None:
            
            print('conexion')
            conn = conn_bd().connect()
            trans = conn.begin()
            transformed['create_at'] = now2
            transformed.to_sql(type_table,schema='data',if_exists='append',con=conn,index=False,chunksize=1000)
            print('fin conexion')
            # try:
            #     handlers.clean_redshift(
            #         conn,
            #         staging_table=TABLES[platform]['staging_table'],
            #         source_route=uploaded['path']
            #     )
            #     handlers.clean_redshift(
            #         conn,
            #         staging_table=TABLES[platform]['enrich_table'],
            #         source_route=uploaded['path']
            #     )
            #     handlers.copy_to_redshift(
            #         conn,
            #         bucket=os.getenv('S3_BUCKET'),
            #         staging_table=TABLES[platform]['staging_table'],
            #         source_route=transformed['path']
            #     )
            #     handlers.execute_redshift(
            #         conn,
            #         query_type='enrich',
            #         query=TABLES[platform]['name'],
            #         staging_table=TABLES[platform]['staging_table'],
            #     enrich_table=TABLES[platform]['enrich_table'],
            #     source_route=uploaded['path']
            #     )
            #     handlers.execute_redshift(
            #         conn,
            #         query_type='update',
            #         query='update',
            #         final_table=TABLES[platform]['final_table'],
            #         enrich_table=TABLES[platform]['enrich_table'],
            #         source_route=uploaded['path']
            #     )
            #     handlers.execute_redshift(
            #         conn,
            #         query_type='insert',
            #         query='insert',
            #         final_table=TABLES[platform]['final_table'],
            #         enrich_table=TABLES[platform]['enrich_table'],
            #         source_route=uploaded['path']
            #     )
            #     handlers.clean_redshift(
            #         conn, 
            #         staging_table=TABLES[platform]['staging_table'], 
            #         source_route=uploaded['path']
            #     )
            #     handlers.clean_redshift(
            #         conn, 
            #         staging_table=TABLES[platform]['enrich_table'], 
            #         source_route=uploaded['path']
            #     )

            trans.commit()

            # except Exception as e:
            #     trans.rollback()
            #     raise e


    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=513,
            detail="Transform error with: " + str(traceback.format_exc())
        )
    print('return')
    return {
        'source': uploaded,
        'transformed': transformed
    }