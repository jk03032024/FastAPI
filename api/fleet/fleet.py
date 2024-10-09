import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.fleet.model import Fleets, FleetSettings


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


# @router.get('/fleets', status_code=status.HTTP_200_OK,
#              name="Get all Fleets", response_model=List[Fleets])
# async def get_all_fleets(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM fleets.fleets"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/fleets', status_code=status.HTTP_200_OK,
            name="Get fleets by app_short_code", response_model=List[Fleets])
async def get_fleets_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT * 
            #     FROM fleets.fleets WHERE app_short_code = %s""", (app_short_code,)
            # )
            await cur.execute("""
                SELECT fls.id, fls.app_short_code, fls.display_name, 
                              acs.display_name AS customer_display_name, 
                              fls.fleet_location, fls.google_cordinates
                FROM fleets.fleets fls 
                JOIN accounts.accounts acs 
                ON fls.customer_id = acs.id 
                WHERE fls.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/fleets_settings', status_code=status.HTTP_200_OK,
#              name="Get all Fleets Settings", response_model=List[FleetSettings])
# async def get_all_fleets_settings(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM fleets.fleet_settings"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/fleet_settings', status_code=status.HTTP_200_OK,
            name="Get fleet settings by app_short_code", response_model=List[FleetSettings])
async def get_fleet_setting_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM fleets.fleet_settings WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
