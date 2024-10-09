import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from utils.database_helper import DBConnectionPool, CosmoseConnectionToolNew, CosmoseConnectionTool
from api.account import account
from api.application import application
from api.fleet import fleet
from api.site import site
from api.asset_model import asset_model
from api.asset import asset
from api.ticket import ticket
from api.app import app as app_router
from api.token import token as token_router
from api.inventory import inventory
from api.cloud_security import cloud_security
from api.app_management import app_management
from api.accounts_management_masters import accounts_management_masters
from api.accounts_management import accounts_management
from api.asset_models import asset_models
from api.asset_management import asset_management
from core import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    # PostgreSQL connection pool
    app.async_pool = DBConnectionPool()
    await app.async_pool.psyco_async_pool.open()
    # Cosmos DB connection
    app.cosmos_tool = CosmoseConnectionTool()
    app.cosmos_tool.connect()
    # app.cosmos_tool_new = CosmoseConnectionToolNew()
    # app.cosmos_tool_new.connect()
    yield
    await app.async_pool.close()

def get_application() -> FastAPI:
    Application = FastAPI(
        title=config.APP_NAME,
        debug=config.DEBUG,
        version=config.VERSION,
        lifespan=lifespan
    )

    Application.include_router(account.router, prefix=config.API_PREFIX, tags=["Account"])
    Application.include_router(application.router, prefix=config.API_PREFIX, tags=["Application"])
    Application.include_router(fleet.router, prefix=config.API_PREFIX, tags=["Fleet"])
    Application.include_router(site.router, prefix=config.API_PREFIX, tags=["Site"])
    Application.include_router(asset_model.router, prefix=config.API_PREFIX, tags=["Asset Model"])
    Application.include_router(asset.router, prefix=config.API_PREFIX, tags=["Asset"])
    Application.include_router(ticket.router, prefix=config.API_PREFIX, tags=["Ticket"])
    Application.include_router(app_router.router, prefix=config.API_PREFIX, tags=["App"])
    Application.include_router(token_router.router, prefix=config.API_PREFIX, tags=["Token"])
    Application.include_router(inventory.router, prefix=config.API_PREFIX, tags=["Inventory"])
    Application.include_router(cloud_security.router, prefix=config.API_PREFIX, tags=["CloudSecurity"])

    Application.include_router(app_management.router, prefix=config.API_PREFIX, tags=["App Management"])
    Application.include_router(accounts_management_masters.router, prefix=config.API_PREFIX, tags=["Accounts Management - Masters"])
    Application.include_router(accounts_management.router, prefix=config.API_PREFIX, tags=["Accounts Management"])
    Application.include_router(asset_management.router, prefix=config.API_PREFIX, tags=["Asset Management"])
    Application.include_router(asset_models.router, prefix=config.API_PREFIX, tags=["Asset Models"])
    return Application

app = get_application()
origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
