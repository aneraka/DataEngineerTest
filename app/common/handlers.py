import json
import os
from abc import abstractmethod
from app.config.connections import get_aws_session, get_s3_resource


class UploadHandler:
    S3_FOLDER: str = ''
    

    SOURCE_METHOD: str = 'source'
    TRANSFORM_METHOD: str = 'transform'

    @staticmethod
    def file_contents(file):
        filename, file_extension = os.path.splitext(file.filename)


        return {
            'file_name': file.filename,
            'name': filename,
            'extension': file_extension,
            'contents': file.file.read()
        }

    @classmethod
    def s3_path(cls, *args):
        return os.path.join(
            cls.S3_FOLDER,
            *args
        )

    @classmethod
    def write_to_s3(cls, utc_time: str, file,type_table:str,proceso:str, *args):

        print(*args)
        s3 = get_s3_resource(
            get_aws_session()
        )
        print(s3)
        s3_path = cls.s3_path(
            type_table,
            utc_time,
            proceso,file['name']
        ) + file['extension']
        print(s3_path)
        return {
            'bucket': os.getenv('S3_BUCKET'),
            'path': s3_path,
            'response': s3.Object(
                os.getenv('S3_BUCKET'),
                s3_path
            ).put(Body=file['contents'])
        }
    
    @classmethod
    def write_to_s3_avro(cls, utc_time: str, file,type_table:str,proceso:str, *args):


        s3 = get_s3_resource(
            get_aws_session()
        )
        s3_path = cls.s3_path(
            'backup',
            type_table,
            utc_time
        ) + '.avro'
        # Body=bytes(json.dumps(file, default=str).encode())
        s3.Object(
                os.getenv('S3_BUCKET'),
                s3_path
            ).put(Body=file)
        
        return s3_path
    
    @classmethod
    def get_list_s3(cls,type_table:str, *args):
        
        s3 = get_s3_resource(
            get_aws_session()
        )
        bucket = s3.Bucket(os.getenv('S3_BUCKET'))
        objects = list(bucket.objects.filter(Prefix=f'backup/{type_table}'))
        objects = [o.key for o in objects]
        return objects

    @classmethod
    @abstractmethod
    def write_transformed(
            cls,
            utc_time: str,
            file: dict,
            *args,
            **kwargs
    ):
        pass

    @classmethod
    def clean_redshift(cls, cursor, *args, **kwargs):
        cursor.execute(
            cls.REDSHIFT_CLEAN_QUERY.format(
                *args,
                **kwargs
            )
        )

    @classmethod
    def copy_to_redshift(cls, cursor, *args, **kwargs):
        cursor.execute(
            cls.REDSHIFT_COPY_QUERY.format(
                *args,
                **kwargs
            )
        )

    @classmethod
    def update_db(cls, cursor, *args, **kwargs):
        cursor.execute(
            cls.REDSHIFT_UPDATE_QUERY.format(
                *args,
                **kwargs
            )
        )

    @classmethod
    def insert_db(cls, cursor, *args, **kwargs):

        
        cursor.execute(
            cls.REDSHIFT_INSERT_QUERY.format(
                *args,
                **kwargs
            )
        )

    @classmethod
    @abstractmethod
    def upload_file(
            cls,
            username: str,
            file,
            *args,
            **kwargs
    ):
        pass

    @classmethod
    def upload_files(
            cls,
            username: str,
            files: list,
            *args,
            **kwargs
    ) -> list:
        return [
            dict(
                filename=file.filename,
                **cls.upload_file(
                    username=username,
                    file=file,
                    *args,
                    **kwargs
                )
            )
            for file in files
        ]
