from pydantic import BaseModel
from pydantic.typing import Literal


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
