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

def execute_db(
    cls,
    cursor,
    query_type: str,
    query: str,
    **kwargs
):
    query = cls.read_file(
        f'source/{query_type}/{query}.sql'
    ).format(
        **kwargs
    )

    cursor.execute(
        query
    )

def write_transformed(
        utc_time: str,
        file: dict,
        source_route: str,
        type_table: str
):  
    import pandas as pd
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
      
        return pd.DataFrame()
    

def upload_file(type_table: str, file):
    now2 = datetime.utcnow()
    now = now2.strftime(constants.DATETIME_FORMAT)
    file_data = handlers.UploadHandler.file_contents(file)
    print('upload')
    try:
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
        
        if not transformed.empty:
            if type_table in ['jobs','departments']:

                create_tmp(type_table=type_table,data=transformed)
                # update_db2(utc_time=now2,type_table=type_table,data=transformed)
                insert_db2(utc_time=now2,type_table=type_table,data=transformed)
                delete_tmp(type_table=type_table,data=transformed)
            elif type_table in 'hired_employees':
                conn = conn_bd().connect()
                trans = conn.begin()
                transformed['create_at'] = now2
                transformed.to_sql(type_table,schema='data',if_exists='append',con=conn,index=False)
                trans.commit()



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

def create_tmp(type_table,data):

    tmp_Table = f'{type_table}__tmp'
    conn = conn_bd().connect()
    trans = conn.begin()

    if type_table =='departments':
        conn.execute(f'''
                    CREATE TABLE "data".{tmp_Table} (
                        id int4 NOT NULL,
                        department varchar(50) NOT NULL
                    );
                    ''')
    elif type_table =='jobs':
        conn.execute(f'''
                    CREATE TABLE "data".{tmp_Table} (
                        id int4 NOT NULL,
                        job varchar(50) NOT NULL
                    );
                    ''')
    
    data.to_sql(tmp_Table,schema='data',if_exists='append',con=conn,index=False)

    trans.commit()


def insert_db2(utc_time,type_table,data):

    tmp_Table = f'{type_table}__tmp'

    conn = conn_bd().connect()
    trans = conn.begin()

    if type_table =='departments':
        campo ='department'
    elif type_table =='jobs':
        campo ='job'

    conn.execute(f'''
                UPDATE "data".{type_table} AS f
                SET
                    updated_at  = now() ,
                    deleted_at  = now()
                FROM
                    "data".{type_table} AS f_temp
                INNER JOIN "data".{tmp_Table} AS stg
                    ON f_temp.id = stg.id
                    AND f_temp.deleted_at is null
                WHERE
                    f_temp.id = f.id
                    AND f.deleted_at is null
                    AND
                    (
                        COALESCE(f.{campo}, '') != COALESCE(stg.{campo}) 
                    );
                ''')
    # NEWS
    conn.execute(f'''
                INSERT INTO "data".{type_table}
                (id, {campo}, create_at, updated_at, deleted_at)
                select tmp.id, tmp.{campo},now(),now(),null
                FROM "data".{tmp_Table} AS tmp
                left JOIN "data".{type_table} AS old
                    ON (tmp.id = old.id and old.deleted_at is null)
                WHERE old.id is null;
                ''')
    trans.commit()

def delete_tmp(type_table,data):
    tmp_Table = f'{type_table}__tmp'
    conn = conn_bd().connect()
    trans = conn.begin()

    conn.execute(f'''
                drop TABLE "data".{tmp_Table};
                ''')

    trans.commit()
