import os
import json
import random
import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.asset_models.model import AssetModels, ChildDevices, DataModel, EdgeServices


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/{{assetModelManagement}}/assetmodels', status_code=status.HTTP_200_OK,
            name="To view list of asset models", response_model=List[AssetModels])
async def get_asset_models_by_app_short_code(request: Request,
                                             app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.asset_models WHERE app_short_code = %s""",
                (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetModelManagement}}/assetmodels/{{assetmodelid}}/childdevices', status_code=status.HTTP_200_OK,
            name="To get existing asset model child devices", response_model=List[ChildDevices])
async def get_child_devices_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                         request: Request,
                                                                         app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.child_devices WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetModelManagement}}/assetmodels/{{assetmodelid}}/edgeservices', status_code=status.HTTP_200_OK,
            name="To get existing assetmodel edge services",
            response_model=List[EdgeServices])
async def get_edge_services_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                         request: Request,
                                                                         app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.edge_services WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{assetModelManagement}}/assetmodels/{{assetmodelid}}/datamodel', status_code=status.HTTP_200_OK,
            name="To get existing assetmodel data model", response_model=DataModel)
async def get_data_model_by_app_short_code_and_asset_model_short_code(asset_model_short_code: str,
                                                                      request: Request,
                                                                      app_short_code: str = Header(..., alias="app_short_code")):
    query_map = {
        "telemetry_model": """
            SELECT source_short_code, property_json_key, property_display_name, property_unit, property_data_type, property_accuracy 
            FROM asset_models.edge_telemetry_model 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",
        
        "getset_model": """
            SELECT * 
            FROM asset_models.edge_getset_model 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",
        
        "event_model": """
            SELECT source_short_code, event_code, event_message, event_severity 
            FROM asset_models.edge_event_model 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",
        
        "contextual_model": """
            SELECT source_short_code, parameter_json_key, parameter_display_name 
            FROM asset_models.edge_contextual_model 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",
        
        "child_devices": """
            SELECT outputs 
            FROM asset_models.child_devices 
            WHERE app_short_code = %s AND asset_model_short_code = %s"""
        
    }

    formatted_result = {}

    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            for key, query in query_map.items():
                await cur.execute(query, (app_short_code, asset_model_short_code))
                results = await cur.fetchall()
                formatted_result[key] = results

    logger.info(formatted_result)
    return formatted_result
