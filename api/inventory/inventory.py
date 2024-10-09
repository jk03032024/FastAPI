import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.inventory.model import Inventory

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/inventory', status_code=status.HTTP_200_OK,
            name="Get Inventory by app_short_code", response_model=List[Inventory])
async def get_inventory_by_app_short_code_and_asset_model_short_code(request: Request,
                                                                     app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT i.*, a.provisioned_on 
                FROM inventory.inventory i 
                LEFT JOIN assets.iothub_devices a 
                ON i.unique_id = a.unique_id 
                WHERE i.app_short_code = %s""",
                (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
