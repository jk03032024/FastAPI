import logging
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.asset_management.model import Assets, AssetWiseIothubdevices, \
    AssetsContextualMetadata


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

def remove_from_dict(results: list):
    keys_to_remove = ['_rid', '_self', '_etag', '_attachments', '_ts']
    for result in results:
        for key in keys_to_remove:
            result.pop(key, None)
    return results

@router.get('/{{assetManagement}}/assets', status_code=status.HTTP_200_OK,
            name="To get list of assets", response_model=List[Assets])
async def get_assets_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT ats.id, ats.app_short_code, ats.asset_model_short_code, 
                              ats.display_name,
                              ats.no_of_linked_iothubdevices,
                              acs.display_name AS customer_display_name, 
                              sts.site_location, 
                              fls.fleet_location, 
                              sas.display_name as superasset_display_name, 
                              ats.contextual_data_captured, ats.image_uri 
                FROM assets.assets ats 
                LEFT JOIN accounts.accounts acs ON ats.customer_id = acs.id 
                LEFT JOIN sites.sites sts ON ats.site_id = sts.id 
                LEFT JOIN fleets.fleets fls ON ats.fleet_id = fls.id 
                LEFT JOIN super_assets.super_assets sas ON ats.superasset_id = sas.id
                WHERE ats.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetManagement}}/assets/{id}/metadata', status_code=status.HTTP_200_OK,
            name="To get specific asset metadata", response_model=List[Assets])
async def get_specific_assets_by_app_short_code_and_id(id, request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT ats.id, ats.app_short_code, ats.asset_model_short_code, 
                              ats.display_name,
                              ats.no_of_linked_iothubdevices,
                              acs.display_name AS customer_display_name, 
                              sts.site_location, 
                              fls.fleet_location, 
                              sas.display_name as superasset_display_name, 
                              ats.contextual_data_captured, ats.image_uri 
                FROM assets.assets ats 
                LEFT JOIN accounts.accounts acs ON ats.customer_id = acs.id 
                LEFT JOIN sites.sites sts ON ats.site_id = sts.id 
                LEFT JOIN fleets.fleets fls ON ats.fleet_id = fls.id 
                LEFT JOIN super_assets.super_assets sas ON ats.superasset_id = sas.id
                WHERE ats.app_short_code = %s AND ats.id = %s 
            """, (app_short_code, id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetManagement}}/assets/{id}/latesttelemetry', status_code=status.HTTP_200_OK,
            name="To get specific asset latest telemetry")
async def get_latest_telemetry_by_app_short_code_and_asset_id(asset_id,
                                                              request: Request,
                                                              app_short_code: str = Header(..., alias="app_short_code")):
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id 
        ORDER BY c.ts DESC OFFSET 0 LIMIT 1
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id}
    ]
    results = request.app.cosmos_tool.data_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/{{assetManagement}}/assets/{id}/recenttelemetry', status_code=status.HTTP_200_OK,
            name="To get specific asset recent telemetry")
async def get_recent_telemetry_by_app_short_code_and_asset_id(asset_id,
                                                              request: Request,
                                                              app_short_code: str = Header(..., alias="app_short_code")):
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id 
        ORDER BY c.ts DESC OFFSET 0 LIMIT 15
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id}
    ]
    results = request.app.cosmos_tool.data_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/{{assetManagement}}/assets/{{id}}/contextualdata', status_code=status.HTTP_200_OK,
            name="To view asset wise contextual data",
            response_model=List[AssetsContextualMetadata])
async def get_asset_contextualmetadata_by_app_short_code_and_asset_id(asset_id,
                                                                      request: Request,
                                                                      app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT contextual_data_captured 
                FROM assets.assets WHERE app_short_code = %s AND id = %s""",
                (app_short_code, asset_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetManagement}}/assets/{{id}}/iothubdevices', status_code=status.HTTP_200_OK,
            name="To view asset wise iot hub devices",
            response_model=List[AssetWiseIothubdevices])
async def get_asset_wise_iothubdevices_by_app_short_code_and_asset_id(asset_id,
                                                                      request: Request,
                                                                      app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM assets.asset_wise_iothubdevices WHERE app_short_code = %s AND asset_id = %s""",
                (app_short_code, asset_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetManagement}}/assets/{id}/recentevents', status_code=status.HTTP_200_OK,
            name="To view asset wise recent events",
            response_model=List[AssetWiseIothubdevices])
async def get_asset_wise_iothubdevices_by_app_short_code_and_asset_id(asset_id,
                                                                      request: Request,
                                                                      app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM assets.asset_wise_iothubdevices 
                WHERE app_short_code = %s AND asset_id = %s 
                ORDER BY c.ts DESC OFFSET 0 LIMIT 1 """,
                (app_short_code, asset_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetManagement}}/assets/{id}/heartbeatevents', status_code=status.HTTP_200_OK,
            name="To view asset wise heartbeat events")
async def get_heartbeats_by_app_short_code_and_asset_id(asset_id,
                                                        request: Request,
                                                        app_short_code: str = Header(..., alias="app_short_code")):
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id}
    ]
    results = request.app.cosmos_tool.heartbeats_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/{{assetManagement}}/assets/{id}/lifecycleevents', status_code=status.HTTP_200_OK,
            name="To view asset wise lifecycle events")
async def get_lifecycle_by_app_short_code_and_asset_id(asset_id,
                                                       request: Request,
                                                       app_short_code: str = Header(..., alias="app_short_code")):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    last_week_date = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id 
            AND c.date >= @last_week_date AND c.date <= @today_date 
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id},
        {"name": "@last_week_date", "value": last_week_date},
        {"name": "@today_date", "value": today_date}
    ]
    results = request.app.cosmos_tool.lifecycle_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results
