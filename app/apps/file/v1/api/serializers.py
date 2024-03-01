from pydantic import BaseModel
from pydantic.typing import Literal
from typing import List


class UploadSerializer(BaseModel):
    type_table: Literal[
        'departments',
        'hired_employees',
        'jobs'
    ]

class Backup(BaseModel):
    type_action: Literal[
        'create',
        'list_files',
        'restore'
    ]
    
    type_table: Literal[
        'departments',
        'hired_employees',
        'jobs'
    ]

    file: str = ''

class ReporteBase(BaseModel):
    dimension: str
    metric: str

class Reporte(BaseModel):
    data: List[ReporteBase]


