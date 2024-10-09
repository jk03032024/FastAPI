import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.application.model import Application


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


@router.get('/applications', status_code=status.HTTP_200_OK,
             name="Get all applications", response_model=List[Application])
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

# @router.get('/applications', status_code=status.HTTP_200_OK,
#             name="Get applications by short_code", response_model=List[Application])
# async def get_applications_by_short_code(request: Request, short_code: str = Header(..., alias="app_short_code")):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT * 
#                 FROM applications.applications WHERE short_code = %s""", (short_code,)
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results
