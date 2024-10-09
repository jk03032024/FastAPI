from fastapi import APIRouter, HTTPException, Header, status
from fastapi.responses import StreamingResponse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from io import BytesIO
from core import config

router = APIRouter()

def get_blob_client(container_name: str, blob_name: str) -> BlobClient:
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(account_url=f"https://{config.STORAGE_ACCOUNT_NAME}.blob.core.windows.net",
                                            credential=credential)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    return blob_client

@router.get("/get_app_icon", status_code=status.HTTP_200_OK,
            name="Get App Icon by app_icon_uri",)
async def get_app_icon(app_icon_uri: str = Header(..., alias="app_icon_uri")):
    try:
        app_icon_uri = app_icon_uri.split("/")
        blob_client = get_blob_client(app_icon_uri[0], app_icon_uri[1])
        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()
        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_asset_model_icons", status_code=status.HTTP_200_OK,
            name="Get Asset Model Icons by asset_model_icon_uri",)
async def get_asset_model_icons(asset_model_icon_uri: str = Header(..., alias="asset_model_icon_uri")):
    try:
        asset_model_icon_uri = asset_model_icon_uri.split("/")
        blob_client = get_blob_client(asset_model_icon_uri[0], asset_model_icon_uri[1])
        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()
        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_asset_model_iot_architecture_image", status_code=status.HTTP_200_OK,
            name="Get Asset Model Iot Architecture Image by asset_model_icon_uri",)
async def get_asset_model_iot_architecture_image(asset_model_iot_architecture_image_uri: str = Header(..., alias="asset_model_iot_architecture_image_uri")):
    try:
        asset_model_iot_architecture_image_uri = asset_model_iot_architecture_image_uri.split("/")
        blob_client = get_blob_client(asset_model_iot_architecture_image_uri[0], asset_model_iot_architecture_image_uri[1])
        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()
        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_asset_images", status_code=status.HTTP_200_OK,
            name="Get Asset Images by asset_image_uri",)
async def get_asset_images(asset_image_uri: str = Header(..., alias="asset_image_uri")):
    try:
        asset_image_uri = asset_image_uri.split("/")
        blob_client = get_blob_client(asset_image_uri[0], asset_image_uri[1])
        download_stream = blob_client.download_blob()
        image_data = download_stream.readall()
        return StreamingResponse(BytesIO(image_data), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
