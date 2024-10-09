import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.accounts_management_masters.model import MasterAccountCategories, MasterClaims, \
    MasterMicroServices, MasterPolicies

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/{{accountsManagementUrl}}/accountcategories', status_code=status.HTTP_200_OK,
             name="To get master list of account categories", response_model=List[MasterAccountCategories])
async def get_master_account_categories(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM accounts.master_account_categories"""
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/microservices', status_code=status.HTTP_200_OK,
             name="To get master list of microservices", response_model=List[MasterMicroServices])
async def get_master_microservices(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT *
                FROM accounts.master_microservices"""
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/policies', status_code=status.HTTP_200_OK,
             name="To get list of polices", response_model=List[MasterPolicies])
async def get_master_policies(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT mps.id, mms.display_name AS microservice_display_name, 
                       mps.display_name, mps.claims, mps.menu, 
                       mps.permissions_required
                FROM accounts.master_policies mps 
                JOIN accounts.master_microservices mms 
                ON mps.microservice_id = mms.id 
            """
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/claims', status_code=status.HTTP_200_OK,
             name="To get list of claims", response_model=List[MasterClaims])
async def get_master_claims(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT mcs.id, mcs.feature_name, mcs.display_name, mcs.name, 
                       mcs.type, mcs.is_default_claim,
                       mms.display_name AS microservice_display_name
                FROM accounts.master_claims mcs 
                JOIN accounts.master_microservices mms 
                ON mcs.microservice_id = mms.id 
            """
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/microservices/{{microserviceid}}/claims', status_code=status.HTTP_200_OK,
             name="To get list of claims for selected micro service", response_model=List[MasterClaims])
async def get_claims_by_microservice_id(microserviceid, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT mcs.id, mcs.feature_name, mcs.display_name, mcs.name, 
                       mcs.type, mcs.is_default_claim,
                       mms.display_name AS microservice_display_name
                FROM accounts.master_claims mcs 
                JOIN accounts.master_microservices mms 
                ON mcs.microservice_id = mms.id 
                WHERE mcs.microservice_id = %s
            """, (microserviceid,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/policies/{{policyid}}/claims', status_code=status.HTTP_200_OK,
             name="To get list of claims for selected policy", response_model=List[MasterPolicies])
async def get_policies_by_policyid(policyid, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT mps.id, mms.display_name AS microservice_display_name, 
                       mps.display_name, mps.claims, mps.menu, 
                       mps.permissions_required
                FROM accounts.master_policies mps 
                JOIN accounts.master_microservices mms 
                ON mps.microservice_id = mms.id 
                WHERE mps.id = %s 
            """, (policyid,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/microservices/{{microserviceid}}/policies/{{policyid}}/claims', status_code=status.HTTP_200_OK,
             name="To get list of claims for selected micro service & selected policy", response_model=List[MasterPolicies])
async def get_policies_by_policyid(policyid, microserviceid, request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT mps.id, mms.display_name AS microservice_display_name, 
                       mps.display_name, mps.claims, mps.menu, 
                       mps.permissions_required
                FROM accounts.master_policies mps 
                JOIN accounts.master_microservices mms 
                ON mps.microservice_id = mms.id 
                WHERE mps.id = %s AND mps.microservice_id = %s 
            """, (policyid, microserviceid,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
