import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.app_management.model import Application


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


@router.get('/{{appManagementUrl}}/apps', status_code=status.HTTP_200_OK,
             name="To get list of all apps ", response_model=List[Application])
async def get_all_applications(
        request: Request                 
    ):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM applications.applications"""
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{appManagementUrl}}/apps/{id}', status_code=status.HTTP_200_OK,
             name="To get details of specific app (backend to check whether I am having app access or not) ", response_model=List[Application])
async def get_app_by_id(id, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM applications.applications 
                WHERE id = %s """, (id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
