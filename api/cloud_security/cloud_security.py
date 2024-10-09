import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.cloud_security.model import CloudSecurityEvents

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/cloud_security_events', status_code=status.HTTP_200_OK,
            name="Get Cloud Security Events", response_model=List[CloudSecurityEvents])
async def get_cloud_security_events(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM cloud_security.cloud_security_events """
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
