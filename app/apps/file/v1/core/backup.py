from app.config.connections import conn_bd
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import pandas as pd
from io import BytesIO
from datetime import datetime
from app.config.connections import conn_bd

from app.common import constants, handlers


class backup():

    def __init__(self,type_action,type_table):
        self.type_table = type_table
        self.type_action = type_action

        self.con = conn_bd().connect()

        if self.type_action == 'create':
            self.create_backup()

        if self.type_action =='list_files':
            self.list_backups()

    def create_backup(self):
        import os
        print(os.getcwd())      
        data = pd.read_sql(f'select * from data.{self.type_table}',con=self.con)
        schema = avro.schema.parse(open(f"./{self.type_table}.avsc", "rb").read())

        now2 = datetime.utcnow()
        now = now2.strftime(constants.DATETIME_FORMAT)

        string = BytesIO()
        writer = DataFileWriter(string, DatumWriter(), schema)
        data['create_at'] = data['create_at'].astype(str)
        if self.type_table in ['jobs','departments']:
            data['updated_at'] = data['updated_at'].astype(str)
            data['deleted_at'] = data['deleted_at'].astype(str)

        for index,row in data.iterrows():
            writer.append(dict(row))
        writer.flush()
        bytes_value = string.getvalue()
        writer.close()
        self.result =  handlers.UploadHandler.write_to_s3_avro(
            now,
            bytes_value,
            self.type_table,
            'avro'
        )

    def list_backups(self):
        self.result =  handlers.UploadHandler.get_list_s3(type_table=self.type_table)
        # reader = DataFileReader(open("departments.avro", "rb"), DatumReader())
        # for user in reader:
        #     print(user)
        # reader.close()

    # def generate_avro_bytes(schema,avro_dicts, codec='snappy'):
    #     bytes_writer = io.BytesIO()
    #     writer = DataFileWriter(bytes_writer, DatumWriter(), schema, codec=codec)
    #     for d in avro_dicts:
    #         writer.append(d)
    #     writer.flush()
    #     bytes_value = bytes_writer.getvalue()
    #     writer.close()
    #     return bytes_value