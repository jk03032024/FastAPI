import logging
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.asset.model import Assets, AssetWiseIothubdevices, \
    AssetsContextualMetadata, SiteAssets


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


# @router.get('/assets', status_code=status.HTTP_200_OK,
#              name="Get all Assets", response_model=List[Assets])
# async def get_all_asset_models(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM assets.assets"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/assets', status_code=status.HTTP_200_OK,
            name="Get Assets by app_short_code", response_model=List[Assets])
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

@router.get('/asset_wise_iothubdevices/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Asset Wise Iothubdevices by app_short_code & asset_id",
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

def remove_from_dict(results: list):
    keys_to_remove = ['_rid', '_self', '_etag', '_attachments', '_ts']
    for result in results:
        for key in keys_to_remove:
            result.pop(key, None)
    return results

@router.get('/live_data/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Live Data of asset by app_short_code and asset_id")
async def get_live_data_by_app_short_code_and_asset_id(asset_id,
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
    results = request.app.cosmos_tool.data_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/live_event/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Live Event of asset by app_short_code and asset_id")
async def get_live_event_by_app_short_code_and_asset_id(asset_id,
                                                        request: Request,
                                                        app_short_code: str = Header(..., alias="app_short_code")):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id AND c.date = @today_date 
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id},
        {"name": "@today_date", "value": today_date}
    ]
    results = request.app.cosmos_tool.event_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/global_security_events', status_code=status.HTTP_200_OK,
            name="Get Global Security Events of asset by app_short_code")
async def get_security_event_by_app_short_code_and_asset_id(request: Request,
                                                            app_short_code: str = Header(..., alias="app_short_code")):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.date = @today_date 
        ORDER BY c.ts DESC 
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@today_date", "value": today_date}
    ]
    results = request.app.cosmos_tool.security_query_items(query, parameters)
    results = remove_from_dict(results)

    dashboard = {}
    total_events = 0
    for item in results:
        if "data" in item:
            for event in item["data"].values():
                total_events += 1
                ecode = event["ecode"]
                if ecode in dashboard:
                    dashboard[ecode] += 1
                else:
                    dashboard[ecode] = 1

    dashboard_list = [{"name": ecode, "count": count} for ecode, count in dashboard.items()]
    updated_results = {}
    updated_results["security_events"] = results
    updated_results["total_events"] = total_events
    updated_results["dashboard"] = dashboard_list
    logger.info(updated_results)
    return updated_results

@router.get('/security_event/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Security Event of asset by app_short_code and asset_id")
async def get_security_event_by_app_short_code_and_asset_id(asset_id,
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
    results = request.app.cosmos_tool.security_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/heartbeats/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Heartbeats Events of asset by app_short_code and asset_id")
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

@router.get('/lifecycle/{asset_id}', status_code=status.HTTP_200_OK,
            name="Get Lifecycle Events of asset by app_short_code and asset_id")
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

@router.get('/assets/{asset_id}/latesttelemetry', status_code=status.HTTP_200_OK,
            name="Get Latest Telemetry Data of asset by app_short_code and asset_id")
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

@router.get('/assets/{asset_id}/recenttelemetry', status_code=status.HTTP_200_OK,
            name="Get Recent Telemetry Data of asset by app_short_code and asset_id")
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

@router.get('/assets/{asset_id}/recent_live_event', status_code=status.HTTP_200_OK,
            name="Get Recent Live Event of asset by app_short_code and asset_id")
async def get_recent_live_event_by_app_short_code_and_asset_id(asset_id,
                                                        request: Request,
                                                        app_short_code: str = Header(..., alias="app_short_code")):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_id = @asset_id AND c.date = @today_date 
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@asset_id", "value": asset_id},
        {"name": "@today_date", "value": today_date}
    ]
    results = request.app.cosmos_tool.event_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/assets/{asset_id}/contextualmetadata', status_code=status.HTTP_200_OK,
            name="Get Asset contextualmetadata by app_short_code & asset_id",
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

@router.get('/assets/{asset_id}/event_summary', status_code=status.HTTP_200_OK,
            name="Get Event Summary of asset by app_short_code and asset_id")
async def get_event_summary_by_app_short_code_and_asset_id(asset_id,
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
    results = request.app.cosmos_tool.event_query_items(query, parameters)
    results = remove_from_dict(results)
    event_summary = {
        'total_number_of_events': 0,
        'events_acknowledged': 0,
        'events_not_yet_acknowledged': 0,
        'active_events': 0,
        'events_cleared': 0,
        'info_events': 0,
        'critical_events': 0,
        'warning_events': 0,
        'error_events': 0
    }
    for result in results:
        if "data" in result:
            for event_key, event_data in result["data"].items():
                event_summary['total_number_of_events'] += 1
                eseverity = event_data.get("eseverity")
                if eseverity == "Critical":
                    event_summary['critical_events'] += 1
                elif eseverity == "Error":
                    event_summary['error_events'] += 1
                elif eseverity == "Warning":
                    event_summary['warning_events'] += 1
                elif eseverity == "Information":
                    event_summary['info_events'] += 1

                ack_status = event_data.get("ack_status")
                if ack_status == "yes":
                    event_summary['events_acknowledged'] += 1
                elif ack_status == "no":
                    event_summary['events_not_yet_acknowledged'] += 1

                clr_status = event_data.get("clr_status")
                if clr_status == "no":
                    event_summary['active_events'] += 1
                elif clr_status == "yes":
                    event_summary['events_cleared'] += 1
    logger.info(event_summary)
    return event_summary

@router.get('/site/{site_id}/recentevents', status_code=status.HTTP_200_OK,
            name="Get Site Wise Recent Events by app_short_code and site_id")
async def get_site_recent_by_app_short_code_and_site_id(site_id,
                                                        request: Request,
                                                        app_short_code: str = Header(..., alias="app_short_code")):
    today_date = datetime.utcnow().strftime('%Y-%m-%d')
    query = """
        SELECT * 
        FROM c 
        WHERE c.app_short_code = @app_short_code AND c.asset_site_id = @site_id AND c.date = @today_date 
    """
    parameters = [
        {"name": "@app_short_code", "value": app_short_code},
        {"name": "@site_id", "value": site_id},
        {"name": "@today_date", "value": today_date}
    ]
    results = request.app.cosmos_tool.sitewise_query_items(query, parameters)
    results = remove_from_dict(results)
    logger.info(results)
    return results

@router.get('/site/{site_id}/assets', status_code=status.HTTP_200_OK,
            name="Get Site Assets by app_short_code and site_id",
            response_model=List[SiteAssets])
async def get_site_assets_by_app_short_code_and_site_id(site_id,
                                                        request: Request,
                                                        app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM assets.assets WHERE app_short_code = %s AND site_id = %s""",
                (app_short_code, site_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
