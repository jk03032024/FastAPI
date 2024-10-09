import logging
import requests
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential
from fastapi import APIRouter, status, HTTPException, Request, Header
from core import config

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/get_token", status_code=status.HTTP_200_OK, name="Get Token")
async def get_token(temp_header_name: str = Header(..., alias="temp_header_name")):
    if temp_header_name == "xlr8-apim":
        url = f"https://login.microsoftonline.com/{config.ID}/oauth2/v2.0/token"
        payload = (
            f'grant_type=client_credentials&client_id={config.CLIENT_ID}&'
            f'client_secret={config.CLIENT_SECRET}&scope=api://{config.CLIENT_ID}/.default'
        )
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            logger.info("Access token retrieved successfully.")
            token = {"access_token": access_token}
            logger.info(token)
            return token
        else:
            logger.error(f"Failed to retrieve token: {response.status_code} - {response.text}")
            return {"error": "Failed to retrieve token"}, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        raise HTTPException(status_code=500, detail=f"Not able to process: {temp_header_name}")

@router.get("/get_code", status_code=status.HTTP_200_OK, name="Get Code")
async def get_code(temp_header_name: str = Header(..., alias="temp_header_name"),
                   Origin: str = Header(None, alias="Origin")):
    url = f"https://login.microsoftonline.com/{config.ID}/oauth2/v2.0/token"

    temp_url = Origin
    if Origin:
        temp_url = f"{Origin}/loginMFA"
    else:
        temp_url = 'https://moschip-genaiot.com/loginMFA'

    payload = {
        'grant_type': 'authorization_code',
        'client_id': config.CODE_CLIENT_ID,
        'code': temp_header_name,
        'redirect_uri': temp_url,
        'client_secret': config.CODE_CLIENT_SECRET,
        'scope': 'https://graph.microsoft.com/.default'
    }
    files=[]
    headers = {}
    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    resp=response.json()
    logger.info(resp)
    access_token=resp["access_token"]


    url = "https://graph.microsoft.com/v1.0/me"

    payload = {}
    headers = {
    'Authorization': access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    code = {
        "userDetails":response.json(),
        "access_token":access_token
        }
    logger.info(code)
    return code

@router.post('/notifications_service/put_email', status_code=status.HTTP_201_CREATED,
             name="Send message to Azure Service Bus")
async def send_service_bus_message(request: Request):
    try:
        credential = DefaultAzureCredential()
        servicebus_client = ServiceBusClient(
            fully_qualified_namespace=config.SERVICE_BUS_NAMESPACE,
            credential=credential
        )
        with servicebus_client:
            sender = servicebus_client.get_queue_sender(config.QUEUE_NAME)
            with sender:
                message_content = "Hello, Service Bus using Managed Identity!"
                message = ServiceBusMessage(message_content)
                sender.send_messages(message)
                logger.info(f"Message sent successfully: {message_content}")
                return {"message": "Message sent successfully.",
                        "content": message_content}
    except Exception as e:
        logger.error(f"Error sending message to Service Bus: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to send message")
