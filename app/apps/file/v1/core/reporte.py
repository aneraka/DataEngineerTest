from app.config.connections import conn_bd
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import pandas as pd
import json
from io import BytesIO
from datetime import datetime
from app.config.connections import conn_bd
from app.apps.file.v1.core.utils import read_file

from app.common import constants, handlers


class reporte():

    def __init__(self,tipo='',data=''):
        self.con = conn_bd().connect()
        sql =read_file('sources/sql/kpi_general.sql')
        self.data_db = pd.read_sql(sql,con=self.con)
        self.data_db['datetime'] = pd.to_datetime(self.data_db['datetime'])

        self.data_db['year'] = self.data_db['datetime'].dt.year
        self.data_db['month'] = self.data_db['datetime'].dt.month
        self.data_db['quarter'] = self.data_db['datetime'].dt.quarter

        if tipo == 'general':
            try:
                self.data = data.dict()
                self.dimensions = self.data['data'][0]['dimension'].split(',')
                self.metrics = self.data['data'][0]['metric'].split(',')

                result = self.data_db.groupby(self.dimensions)['id'].count().reset_index()
                result.rename(columns={'id':self.metrics[0]},inplace=True)

                self.result =  {'status_code':200,
                    'msg':'ok',
                    'data' : result.to_dict(orient='records')}
            except Exception as e:
                result = pd.DataFrame()  
                
                self.result =  {'status_code':202,
                                'msg':'You sent wrong requests',
                                'data' : result.to_dict(orient='records')}
                
    def kpi1(self):
        data = self.data_db.copy()
        # transposed_df = data.pivot(index=['job','department'], columns='quarter', values='count')
        
        data = data[data['year']==2021]

        data = data.groupby(['department','job','quarter'])['id'].count().reset_index().sort_values(['department','job'],ascending=False)

        return {'status_code':200,
                    'msg':'ok',
                    'data' : data.to_dict(orient='records')}
    
    
    def kpi2(self):
        sql =read_file('sources/sql/kpi2.sql').format(year=2021)
        print(sql)
        data = pd.read_sql(sql,con=self.con)

        return {'status_code':200,
                    'msg':'ok',
                    'data' : data.to_dict(orient='records')}
        