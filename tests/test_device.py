from fastapi.testclient import TestClient
import sys
sys.path.append("..")
from main import app
from api.device.model import Device
from tests.local_db import create_device, LocalDB, delete_device
import asyncio
import json
try:
    from asyncio import WindowsSelectorEventLoopPolicy
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
except:
    pass

client = TestClient(app)
db_connection = LocalDB().connection

def test_get_device():
    """
    GIVEN
    WHEN /api/device/device_id with GET method
    THEN response with status 200 and Device model
    """
    with TestClient(app) as client:
        device_id = 2
        
        delete_device(device_id, db_connection)
        create_device(device_id, db_connection)
        response = client.get(f"/api/device/{device_id}")
        assert response.status_code == 200
        assert Device.model_validate(response.json()[0])
        assert response.json() == [{"device_id":device_id,"device_name":"test", "optional": None}]

def test_get_devices_unauthorized():
    """
    GIVEN
    WHEN /api/devices with POST method and user_id who has no permission
    THEN response with status 401 Unauthorized
    """
    with TestClient(app) as client:
        device_id = 2
        delete_device(device_id, db_connection)
        create_device(device_id, db_connection)
        request_body = {'user_id': '2'}
        response = client.post(f"/api/devices", data = json.dumps(request_body))
        print(response.json())
        assert response.status_code == 401

def test_get_devices_authorized():
    """
    GIVEN
    WHEN /api/devices with POST method and user_id who has right permission
    THEN response with status 200 and list of Device
    """
    with TestClient(app) as client:
        device_id = 2
        delete_device(device_id, db_connection)
        create_device(device_id, db_connection)
        request_body = {'user_id': '1'}
        response = client.post(f"/api/devices", data = json.dumps(request_body))
        assert response.status_code == 200
        assert Device.model_validate(response.json()[0])
        assert response.json() == [{"device_id":device_id,"device_name":"test", "optional": None}]