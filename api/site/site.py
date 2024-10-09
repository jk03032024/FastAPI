import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.site.model import Sites, SiteSettings

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


# @router.get('/sites', status_code=status.HTTP_200_OK,
#              name="Get all Sites", response_model=List[Sites])
# async def get_all_sites(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM sites.sites"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/sites', status_code=status.HTTP_200_OK,
            name="Get sites by app_short_code", response_model=List[Sites])
async def get_sites_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT * 
            #     FROM sites.sites WHERE app_short_code = %s""", (app_short_code,)
            # )
            await cur.execute("""
                SELECT ss.id, ss.app_short_code, ss.display_name, 
                              acs.display_name AS customer_display_name, ss.site_location, 
                              ss.google_cordinates
                FROM sites.sites ss 
                JOIN accounts.accounts acs 
                ON ss.customer_id = acs.id 
                WHERE ss.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/sites_settings', status_code=status.HTTP_200_OK,
#              name="Get all Sites Settings", response_model=List[SiteSettings])
# async def get_all_sites_settings(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM sites.site_settings"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/site_settings', status_code=status.HTTP_200_OK,
            name="Get sites setting by app_short_code", response_model=List[SiteSettings])
async def get_sites_setting_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM sites.site_settings WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
