import os
from fastapi import FastAPI
from app.config.routers import urls
from app.config.settings import VERSION

app = FastAPI(
    title='Data File Uploader POC',
    description="""This project is a POC
                    - API to upload files
                    - Save data to S3
                    - Connection to DB (Postgresql)
                    - Docker""",
    version=VERSION,
    root_path=os.getenv(
        'ROOT_PATH',
        ''
    ),
)

app.include_router(
    urls
)