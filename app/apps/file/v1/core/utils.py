import pandas as pd
from io import BytesIO
from datetime import datetime

def to_date(text: str) -> datetime:
        list_format = [
            '%Y-%m-%d %H:%M:%S.%f'
        ]

        for form in list_format:
            try:
                return datetime.strptime(str(text), form)
            except ValueError as error:
                pass

        return None

def get_df(
        data: bytes
    ):
        import io

        data_buffer = io.BytesIO(data)
        print(data_buffer)
        try:
            data = pd.read_csv(
                data_buffer,
                header=None,
                sep=','
            ).dropna(
                axis=1,
                how='all'
            ).dropna(
                axis=0,
                how='all'
            )
            return data
        except UnicodeDecodeError as e:
            data = pd.read_excel(data_buffer)

        
def transform(data, type_table: str):

    if type_table == 'departments':
        data_ok, data_bad = tabla_1(data, type_table)
    else:
        return None

    return data_ok,data_bad


def tabla_1(data, type_table:str): 

    column_trans = {}
    columns_numeric = []
    if type_table == 'departments':

        column_trans = {0:'id',1:'department'}
        columns_numeric = [
            'id'
        ]

    data.rename(columns=column_trans,inplace=True)

    index_bad = set([])
    for column in data.columns:
        index_bad = index_bad.union(set(data[data[column].isnull()].index))

    good_index = set(data.index).difference(index_bad)
    data_ok = data.filter(items=good_index, axis=0)
    data_no = data.filter(items=index_bad, axis=0)
    return data_ok,data_no