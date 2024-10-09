import os
import json
import random
import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row
from psycopg.types.json import Json

from api.asset_model.model import AssetModels, ChildDevices, DataModel,\
    EdgeEventModel, EdgeGetsetModel, EdgeTelemetryModel, EdgeServices, Widgets, \
    EdgeContexetualModel, NetworkInterfaces
from api.asset_model.post_model import InsertDataModel


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()


# @router.get('/asset_models', status_code=status.HTTP_200_OK,
#              name="Get all Asset Models", response_model=List[AssetModels])
# async def get_all_asset_models(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM asset_models.asset_models"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

# @router.get('/asset_models', status_code=status.HTTP_200_OK,
#             name="Get Asset Models by app_short_code", response_model=List[AssetModels])
# async def get_asset_models_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT * 
#                 FROM asset_models.asset_models WHERE app_short_code = %s""", (app_short_code,)
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

# @router.get('/child_devices', status_code=status.HTTP_200_OK,
#              name="Get all Child Devices", response_model=List[ChildDevices])
# async def get_all_child_devices(
#         request: Request                 
#     ):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM asset_models.child_devices"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/asset_models', status_code=status.HTTP_200_OK,
            name="Get Asset Models by app_short_code", response_model=List[AssetModels])
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

@router.get('/child_devices/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Child Devices by app_short_code & asset_model_short_code", response_model=List[ChildDevices])
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

@router.get('/data_model/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Data Model by app_short_code & asset_model_short_code", response_model=DataModel)
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

@router.get('/edge_event_model/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Edge Event Model by app_short_code & asset_model_short_code",
            response_model=List[EdgeEventModel])
async def get_edge_event_model_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                            request: Request,
                                                                            app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.edge_event_model WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/edge_getset_model/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Edge Getset Model by app_short_code & asset_model_short_code",
            response_model=List[EdgeGetsetModel])
async def get_edge_getset_model_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                             request: Request,
                                                                             app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.edge_getset_model WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/edge_telemetry_model/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Edge Telemetry Model by app_short_code & asset_model_short_code",
            response_model=List[EdgeTelemetryModel])
async def get_edge_telemetry_model_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                                request: Request,
                                                                                app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.edge_telemetry_model WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/edge_services/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Edge Services by app_short_code & asset_model_short_code",
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

@router.get('/edge_contextual_model/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Edge Contextual Model by app_short_code & asset_model_short_code",
            response_model=List[EdgeContexetualModel])
async def get_edge_contextual_model_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                         request: Request,
                                                                         app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.edge_contextual_model WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/widgets/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Widgets by app_short_code & asset_model_short_code",
            response_model=List[Widgets])
async def get_widgets_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                   request: Request,
                                                                   app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.widgets WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/network_interfaces/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get Network Interfaces by app_short_code & asset_model_short_code",
            response_model=List[NetworkInterfaces])
async def get_network_interfaces_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                         request: Request,
                                                                         app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM asset_models.network_interfaces WHERE app_short_code = %s AND asset_model_short_code = %s""",
                (app_short_code, asset_model_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/file_create/{asset_model_short_code}', status_code=status.HTTP_200_OK,
            name="Get File Creation by app_short_code & asset_model_short_code")
async def get_file_create_by_app_short_code_and_asset_model_short_code(asset_model_short_code,
                                                                       request: Request,
                                                                       app_short_code: str = Header(..., alias="app_short_code")):
    final_result = {}
    query_map = {
        "child_devices": """
            SELECT * 
            FROM asset_models.child_devices 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",
        
        "assets": """
            SELECT * 
            FROM assets.assets 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",

        "inventory": """
            SELECT * 
            FROM inventory.inventory 
            WHERE app_short_code = %s AND asset_model_short_code = %s""",

        "edge_events": """
            SELECT * FROM asset_models.edge_event_model 
            WHERE app_short_code = %s AND asset_model_short_code = %s AND source_type = 'Edge_Service' 
            ORDER BY id ASC """,

        "site": """
            SELECT * FROM sites.sites 
            WHERE app_short_code = %s AND display_name != 'Austin Convention Center' 
            ORDER BY id ASC """
    }
    formatted_result = {}
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            for key, query in query_map.items():
                if key == "site":
                    await cur.execute(query, (app_short_code,))
                else:
                    await cur.execute(query, (app_short_code, asset_model_short_code))
                results = await cur.fetchall()
                formatted_result[key] = results
    for asset in formatted_result["assets"]:
        site_id = random.choice(formatted_result['site'])
        final_result["tags"] = {"app_short_code": app_short_code,
                                "asset_model_short_code": asset_model_short_code,
                                "asset_site_id": str(site_id["id"]),
                                "asset_name": asset["display_name"]}
        for child_device in formatted_result["child_devices"]:
            read_only = child_device.get("read_only")
            measurables = child_device.get("measurables")
            events = child_device.get("event_codes")
            inventory = random.choice(formatted_result['inventory'])
            final_result[f"{child_device['id']}"] = {
                "short_code": child_device.get("short_code"),
                "routed_via": child_device.get("routed_via"),
                "is_it_iothubdevice": child_device.get("is_it_iothubdevice"),
                "iothubdevice_unique_id": inventory["unique_id"],
                "measurables": measurables.get("measurables") if measurables is not None else [],
                "readonly": read_only.get("readonly") if read_only is not None else [],
                "events": events.get("events") if events is not None else [],
                # New Key
                "intervals": {"telemetry": 10, "event": 10, "heartbeat": 10, "securityincident": 10} if child_device.get("is_it_iothubdevice") else {}
            }

        final_result[str(formatted_result["edge_events"][0]["id"])] = {
            "short_code": formatted_result["edge_events"][0]["source_short_code"],
            "routed_via": formatted_result["edge_events"][0]["iothubdevice_short_code"],
            "is_it_iothubdevice": False,
            "iothubdevice_unique_id": "",
            "measurables": [],
            "readonly": [],
            "events": []
        }
        for data in formatted_result["edge_events"]:
            final_result[str(formatted_result["edge_events"][0]["id"])]["events"].append(
                {
                    "eventcode": data["event_code"],
                    "eventmessage": data["event_message"],
                    "eventseverity": data["event_severity"]
                }
            )

        logger.info(json.dumps(final_result, indent=2))
        json_name = os.path.join(f'{app_short_code}_{asset_model_short_code}_results', f"{asset['id']}.json")
        if not os.path.exists(f"{app_short_code}_{asset_model_short_code}_results"):
            os.makedirs(f"{app_short_code}_{asset_model_short_code}_results")
        if os.path.exists(json_name):
            os.remove(json_name)
        with open(json_name, 'w') as f:
            json.dump(final_result, f, ensure_ascii=False, indent=2)
    return final_result

def convert_sets_to_lists(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {key: convert_sets_to_lists(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    else:
        return obj

@router.post('/asset_model', status_code=status.HTTP_201_CREATED,
             name="Insert Data Model by app_short_code")
async def insert_data_model_by_app_short_code(data_model: InsertDataModel,
                                              request: Request,
                                              app_short_code: str = Header(..., alias="app_short_code")):
    insert_queries = {
        "asset_model": """
            INSERT INTO asset_models.asset_models 
            (app_short_code, display_name, short_code, reference_image_url, iot_architecture_url, domain, asset_general_category, product_code, oem, field_deployment_template, field_deployment_description, contextual_data_to_be_captured) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)""",

        "child_devices": """
            INSERT INTO asset_models.child_devices 
            (app_short_code, asset_model_short_code, display_name, short_code, part_type, part_code, oem, protocol, measurables, derivates, aggregates, read_only, read_write, event_codes, outputs, is_it_iothubdevice, routed_via, contextual_data_to_be_captured) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %b, %s, %s::jsonb)""",

        "contextual_model": """
            INSERT INTO asset_models.edge_contextual_model 
            (app_short_code, asset_model_short_code, source_short_code, source_type, parameter_json_key, parameter_display_name) 
            VALUES (%s, %s, %s, %s, %s, %s)""",

        "event_model": """
            INSERT INTO asset_models.edge_event_model 
            (app_short_code, asset_model_short_code, source_short_code, source_type, iothubdevice_short_code, event_code, event_message, event_severity, is_edge_ack_possible, is_cloud_ack_possible, is_edge_clr_possible, is_cloud_clr_possible, triggers) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %b, %b, %b, %b, %s::jsonb)""",

        "getset_model": """
            INSERT INTO asset_models.edge_getset_model 
            (app_short_code, asset_model_short_code, source_short_code, source_type, iothubdevice_short_code, property_type, property_json_key, property_display_name, property_data_type, property_default_value, property_min_value, property_max_value, property_enum, property_unit, property_accuracy) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",

        "service": """
            INSERT INTO asset_models.edge_services 
            (app_short_code, asset_model_short_code, child_device_short_code, display_name, short_code, service_type, service_version, publisher, measurables, derivatives, aggregates, read_only, read_write, event_codes, contextual_data_to_be_captured) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb)""",

        "telemetry_model": """
            INSERT INTO asset_models.edge_telemetry_model 
            (app_short_code, asset_model_short_code, source_short_code, source_type, iothubdevice_short_code, property_type, property_json_key, property_display_name, property_data_type, property_default_value, property_min_value, property_max_value, property_enum, property_unit, property_accuracy) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",

        "widget": """
            INSERT INTO asset_models.widgets 
            (app_short_code, asset_model_short_code, widget_code, widget_type, widget_size, widget_color_theme, widget_parameters, purpose) 
            VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s)"""
    }

    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Insert asset model data
            if data_model.asset_model.contextual_data_to_be_captured and data_model.asset_model.contextual_data_to_be_captured.contextualparameters:
                contextualparameters_asm = json.dumps(convert_sets_to_lists(data_model.asset_model.contextual_data_to_be_captured.dict()))
            else:
                contextualparameters_asm = None
            await cur.execute(insert_queries["asset_model"], (
                app_short_code,
                data_model.asset_model.display_name,
                data_model.asset_model.short_code,
                data_model.asset_model.reference_image_url,
                data_model.asset_model.iot_architecture_url,
                data_model.asset_model.domain,
                data_model.asset_model.asset_general_category,
                data_model.asset_model.product_code,
                data_model.asset_model.oem,
                data_model.asset_model.field_deployment_template,
                data_model.asset_model.field_deployment_description,
                contextualparameters_asm
            ))

            # Insert child devices data
            if data_model.child_devices.contextual_data_to_be_captured and data_model.child_devices.contextual_data_to_be_captured.contextualparameters:
                contextualparameters_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.contextual_data_to_be_captured.dict()))
            else:
                contextualparameters_cds = None

            if data_model.child_devices.measurables and data_model.child_devices.measurables.measurables:
                measurables_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.measurables.dict()))
            else:
                measurables_cds = None
            if data_model.child_devices.read_only and data_model.child_devices.read_only.readonly:
                read_only_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.read_only.dict()))
            else:
                read_only_cds = None
            if data_model.child_devices.read_write and data_model.child_devices.read_write.configurables:
                read_write_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.read_write.dict()))
            else:
                read_write_cds = None
            if data_model.child_devices.event_codes and data_model.child_devices.event_codes.events:
                event_codes_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.event_codes.dict()))
            else:
                event_codes_cds = None
            if data_model.child_devices.derivatives:
                derivatives_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.derivatives.dict()))
            else:
                derivatives_cds = None
            if data_model.child_devices.aggregates:
                aggregates_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.aggregates.dict()))
            else:
                aggregates_cds = None
            if data_model.child_devices.outputs:
                outputs_cds = json.dumps(convert_sets_to_lists(data_model.child_devices.outputs.dict()))
            else:
                outputs_cds = None
            await cur.execute(insert_queries["child_devices"], (
                app_short_code,
                data_model.child_devices.asset_model_short_code,
                data_model.child_devices.display_name,
                data_model.child_devices.short_code,
                data_model.child_devices.part_type,
                data_model.child_devices.part_code,
                data_model.child_devices.oem,
                data_model.child_devices.protocol,
                measurables_cds,
                derivatives_cds,
                aggregates_cds,
                read_only_cds,
                read_write_cds,
                event_codes_cds,
                outputs_cds,
                data_model.child_devices.is_it_iothubdevice,
                data_model.child_devices.routed_via,
                contextualparameters_cds
            ))

            # Insert contextual model data
            if data_model.child_devices.contextual_data_to_be_captured and \
            data_model.child_devices.contextual_data_to_be_captured.contextualparameters:
                for contextual in data_model.child_devices.contextual_data_to_be_captured.contextualparameters:
                    await cur.execute(insert_queries["contextual_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.child_devices.short_code,
                        "Child Device",
                        contextual.parameterjsonkey,
                        contextual.parameterdisplayname
                    ))
            if data_model.asset_model.contextual_data_to_be_captured and \
            data_model.asset_model.contextual_data_to_be_captured.contextualparameters:
                for contextual in data_model.asset_model.contextual_data_to_be_captured.contextualparameters:
                    await cur.execute(insert_queries["contextual_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.asset_model.short_code,
                        "Asset",
                        contextual.parameterjsonkey,
                        contextual.parameterdisplayname
                    ))
            if data_model.service_model.contextual_data_to_be_captured and \
            data_model.service_model.contextual_data_to_be_captured.contextualparameters:
                for contextual in data_model.service_model.contextual_data_to_be_captured.contextualparameters:
                    await cur.execute(insert_queries["contextual_model"], (
                        app_short_code,
                        data_model.service_model.asset_model_short_code,
                        data_model.service_model.short_code,
                        "Edge Service",
                        contextual.parameterjsonkey,
                        contextual.parameterdisplayname
                    ))

            # Insert event model data
            if data_model.child_devices.event_codes and \
            data_model.child_devices.event_codes.events:
                for event in data_model.child_devices.event_codes.events:
                    if data_model.event_model.triggers:
                        triggers_eml = json.dumps(convert_sets_to_lists(data_model.event_model.triggers.dict()))
                    else:
                        triggers_eml = None
                    await cur.execute(insert_queries["event_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.child_devices.short_code,
                        "Child_Device",
                        data_model.child_devices.routed_via,
                        event.eventcode,
                        event.eventmessage,
                        event.eventseverity,
                        data_model.event_model.is_edge_ack_possible,
                        data_model.event_model.is_cloud_ack_possible,
                        data_model.event_model.is_edge_clr_possible,
                        data_model.event_model.is_cloud_clr_possible,
                        triggers_eml
                    ))
            if data_model.service_model.event_codes and \
            data_model.service_model.event_codes.events:
                for event in data_model.service_model.event_codes.events:
                    if data_model.event_model.triggers:
                        triggers_eml = json.dumps(convert_sets_to_lists((data_model.event_model.triggers.dict())))
                    else:
                        triggers_eml = None
                    await cur.execute(insert_queries["event_model"], (
                        app_short_code,
                        data_model.service_model.asset_model_short_code,
                        data_model.service_model.short_code,
                        "Edge_Service",
                        data_model.child_devices.routed_via,
                        event.eventcode,
                        event.eventmessage,
                        event.eventseverity,
                        data_model.event_model.is_edge_ack_possible,
                        data_model.event_model.is_cloud_ack_possible,
                        data_model.event_model.is_edge_clr_possible,
                        data_model.event_model.is_cloud_clr_possible,
                        triggers_eml
                    ))

            # Insert getset model data
            if data_model.child_devices.read_only and \
            data_model.child_devices.read_only.readonly:
                for data in data_model.child_devices.read_only.readonly:
                    property_enum_array = '{' + ','.join(map(str, data.propertyenum)) + '}' if data.propertyenum else None
                    await cur.execute(insert_queries["getset_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.child_devices.short_code,
                        "Child_Device",
                        data_model.child_devices.routed_via,
                        "read_only",
                        data.propertyjsonkey,
                        data.propertyname,
                        data.propertydatatype,
                        data.propertydefaultvalue,
                        data.propertyminvalue,
                        data.propertymaxvalue,
                        property_enum_array,
                        data.propertyunits,
                        data.propertyaccuracy
                    ))
            if data_model.child_devices.read_write and \
            data_model.child_devices.read_write.configurables:
                for data in data_model.child_devices.read_write.configurables:
                    property_enum_array = '{' + ','.join(map(str, data.propertyenum)) + '}' if data.propertyenum else None
                    await cur.execute(insert_queries["getset_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.child_devices.short_code,
                        "Child_Device",
                        data_model.child_devices.routed_via,
                        "read_write",
                        data.propertyjsonkey,
                        data.propertyname,
                        data.propertydatatype,
                        data.propertydefaultvalue,
                        data.propertyminvalue,
                        data.propertymaxvalue,
                        property_enum_array,
                        data.propertyunits,
                        data.propertyaccuracy
                    ))
            if data_model.service_model.read_only and \
            data_model.service_model.read_only.readonly:
                for data in data_model.service_model.read_only.readonly:
                    property_enum_array = '{' + ','.join(map(str, data.propertyenum)) + '}' if data.propertyenum else None
                    await cur.execute(insert_queries["getset_model"], (
                        app_short_code,
                        data_model.service_model.asset_model_short_code,
                        data_model.service_model.short_code,
                        "Edge_Service",
                        data_model.child_devices.routed_via,
                        "read_only",
                        data.propertyjsonkey,
                        data.propertyname,
                        data.propertydatatype,
                        data.propertydefaultvalue,
                        data.propertyminvalue,
                        data.propertymaxvalue,
                        property_enum_array,
                        data.propertyunits,
                        data.propertyaccuracy
                    ))
            if data_model.service_model.read_write and \
            data_model.service_model.read_write.configurables:
                for data in data_model.service_model.read_write.configurables:
                    property_enum_array = '{' + ','.join(map(str, data.propertyenum)) + '}' if data.propertyenum else None
                    await cur.execute(insert_queries["getset_model"], (
                        app_short_code,
                        data_model.service_model.asset_model_short_code,
                        data_model.service_model.short_code,
                        "Edge_Service",
                        data_model.child_devices.routed_via,
                        "read_write",
                        data.propertyjsonkey,
                        data.propertyname,
                        data.propertydatatype,
                        data.propertydefaultvalue,
                        data.propertyminvalue,
                        data.propertymaxvalue,
                        property_enum_array,
                        data.propertyunits,
                        data.propertyaccuracy
                    ))

            if data_model.service_model.measurables and data_model.service_model.measurables.measurables:
                measurables_sr = json.dumps(convert_sets_to_lists(data_model.service_model.measurables.dict()))
            else:
                measurables_sr = None
            if data_model.service_model.read_only and data_model.service_model.read_only.readonly:
                read_only_sr = json.dumps(convert_sets_to_lists(data_model.service_model.read_only.dict()))
            else:
                read_only_sr = None
            if data_model.service_model.read_write and data_model.service_model.read_write.configurables:
                read_write_sr = json.dumps(convert_sets_to_lists(data_model.service_model.read_write.dict()))
            else:
                read_write_sr = None
            if data_model.service_model.event_codes and data_model.service_model.event_codes.events:
                event_codes_sr = json.dumps(convert_sets_to_lists(data_model.service_model.event_codes.dict()))
            else:
                event_codes_sr = None
            if data_model.service_model.contextual_data_to_be_captured and data_model.service_model.contextual_data_to_be_captured.contextualparameters:
                contextualparameters_sr = json.dumps(convert_sets_to_lists(data_model.service_model.contextual_data_to_be_captured.dict()))
            else:
                contextualparameters_sr = None
            if data_model.service_model.derivatives:
                derivatives_sr = json.dumps(convert_sets_to_lists(data_model.service_model.derivatives.dict()))
            else:
                derivatives_sr = None
            if data_model.service_model.aggregates:
                aggregates_sr = json.dumps(convert_sets_to_lists(data_model.service_model.aggregates.dict()))
            else:
                aggregates_sr = None
            await cur.execute(insert_queries["service"], (
                app_short_code,
                data_model.service_model.asset_model_short_code,
                data_model.child_devices.short_code,
                data_model.service_model.display_name,
                data_model.service_model.short_code,
                data_model.service_model.service_type,
                data_model.service_model.service_version,
                data_model.service_model.publisher,
                measurables_sr,
                derivatives_sr,
                aggregates_sr,
                read_only_sr, read_write_sr, event_codes_sr,
                contextualparameters_sr
            ))

            # Insert telemetry model data
            if data_model.child_devices.measurables and \
            data_model.child_devices.measurables.measurables:
                for measurable in data_model.child_devices.measurables.measurables:
                    property_enum_array = '{' + ','.join(map(str, measurable.propertyenum)) + '}' if measurable.propertyenum else None
                    await cur.execute(insert_queries["telemetry_model"], (
                        app_short_code,
                        data_model.child_devices.asset_model_short_code,
                        data_model.child_devices.short_code,
                        "Child_Device",
                        data_model.child_devices.routed_via,
                        measurable.propertytype,
                        measurable.propertyjsonkey,
                        measurable.propertyname,
                        measurable.propertydatatype,
                        measurable.propertydefaultvalue,
                        measurable.propertyminvalue,
                        measurable.propertymaxvalue,
                        property_enum_array,
                        measurable.propertyunits,
                        measurable.propertyaccuracy
                    ))

            if data_model.child_devices.measurables and \
            data_model.child_devices.measurables.measurables:
                await cur.execute("""
                    SELECT ws.widget_code 
                    FROM asset_models.widgets ws 
                    WHERE ws.widget_code ~ '^W[0-9]+$' 
                    ORDER BY CAST(SUBSTRING(ws.widget_code FROM 2) AS INTEGER) DESC 
                    LIMIT 1;
                """)
                widget_code = await cur.fetchone()
                widget_code = f'W{int(widget_code["widget_code"].split("W")[1]) + 1}'
                widget_value = {"Label Chart (Single Parameter)": "Latest Telemetry",
                                "Trend Chart (Single Parameter)": "Recent Telemetry"}
                for data in data_model.child_devices.measurables.measurables:
                    widget_parameters = json.dumps(convert_sets_to_lists({"propertyjsonkey": data.propertyjsonkey}))
                    for widget_type, purpose in widget_value.items():
                        await cur.execute(insert_queries["widget"], (
                            app_short_code,
                            data_model.child_devices.asset_model_short_code,
                            widget_code,
                            widget_type,
                            "1x1",
                            "Standard",
                            widget_parameters,
                            purpose
                        ))

        await conn.commit()
    logger.info({"Message": "Asset Model Data Inserted Successfully"})
    return {"Message": "Asset Model Data Inserted Successfully"}
