import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.account.model import Account_Types, Accounts, \
    MasterAccountCategories, MasterClaims, MasterMicroServices, \
        MasterPolicies, RoleWisePoliciesAndPermissions, Roles, UserAccounts

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

# @router.get('/account_types', status_code=status.HTTP_200_OK,
#              name="Get all accounts types", response_model=List[Account_Types])
# async def get_all_accounts_types(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.account_types"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/account_types', status_code=status.HTTP_200_OK,
            name="Get account types by app_short_code", response_model=List[Account_Types])
async def get_account_types_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT ats.id, ats.app_short_code, ats.display_name, ats.short_code, 
                       mac.display_name AS account_category_display_name, 
                       ats.account_subcategory, ats.account_classification, 
                       ats.self_registration_allowed, acs.display_name AS parent_account_display_name
                FROM accounts.account_types ats
				LEFT JOIN accounts.account_types acs 
                ON ats.parent_account_type_id = acs.id
                JOIN accounts.master_account_categories mac 
                ON ats.account_category_id = mac.id 
                WHERE ats.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/accounts', status_code=status.HTTP_200_OK,
#              name="Get all accounts", response_model=List[Accounts])
# async def get_all_accounts(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.accounts"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/accounts', status_code=status.HTTP_200_OK,
            name="Get accounts by app_short_code", response_model=List[Accounts])
async def get_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/service_provider_accounts', status_code=status.HTTP_200_OK,
            name="Get Service Provider Accounts by app_short_code", response_model=List[Accounts])
async def get_service_provider_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 1""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/support_accounts', status_code=status.HTTP_200_OK,
            name="Get Support Accounts by app_short_code", response_model=List[Accounts])
async def get_support_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 2""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/partner_accounts', status_code=status.HTTP_200_OK,
            name="Get Partner Accounts by app_short_code", response_model=List[Accounts])
async def get_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 3""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/customer_accounts', status_code=status.HTTP_200_OK,
            name="Get Customer Accounts by app_short_code", response_model=List[Accounts])
async def get_customer_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT acs.id, acs.app_short_code, acs.display_name, 
                              mac.display_name AS account_category_display_name, 
                              ats.display_name AS account_type_display_name, 
                              ats.account_subcategory, 
                              acs.address, acs.contactdetails, 
                              acs.logo_uri, acs.status, 
                              acs.parent_id, acs.grandparent_id 
                FROM accounts.accounts acs 
                JOIN accounts.master_account_categories mac 
                ON acs.account_category_id = mac.id 
                JOIN accounts.account_types ats 
                ON acs.account_type_id = ats.id 
                WHERE acs.app_short_code = %s AND acs.account_category_id = 4""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/master_account_categories', status_code=status.HTTP_200_OK,
             name="Get all master account categories", response_model=List[MasterAccountCategories])
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

@router.get('/master_claims', status_code=status.HTTP_200_OK,
             name="Get all master claims", response_model=List[MasterClaims])
async def get_master_claims(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT *
            #     FROM accounts.master_claims"""
            # )
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

@router.get('/master_microservices', status_code=status.HTTP_200_OK,
             name="Get all master microservices", response_model=List[MasterMicroServices])
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

@router.get('/master_policies', status_code=status.HTTP_200_OK,
             name="Get all master policies", response_model=List[MasterPolicies])
async def get_master_policies(request: Request):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT *
            #     FROM accounts.master_policies"""
            # )
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

# @router.get('/role_wise_policies_and_permissions', status_code=status.HTTP_200_OK,
#              name="Get all role wise policies and permissions",
#              response_model=List[RoleWisePoliciesAndPermissions])
# async def get_all_role_wise_policies_and_permissions(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.role_wise_policies_and_permissions"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/role_wise_policies_and_permissions',
            status_code=status.HTTP_200_OK,
            name="Get role wise policies and permissions by app_short_code",
            response_model=List[RoleWisePoliciesAndPermissions])
async def get_role_wise_policies_and_permissions_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM accounts.role_wise_policies_and_permissions WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/roles', status_code=status.HTTP_200_OK, name="Get all roles",
#              response_model=List[Roles])
# async def get_all_roles(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.roles"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/roles', status_code=status.HTTP_200_OK,
            name="Get roles by app_short_code", response_model=List[Roles])
async def get_roles_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # await cur.execute("""
            #     SELECT * 
            #     FROM accounts.roles WHERE app_short_code = %s""", (app_short_code,)
            # )
            await cur.execute("""
                SELECT rs.id, rs.app_short_code, ats.display_name AS account_type_name, 
                              rs.display_name, rs.is_it_admin_role
                FROM accounts.roles rs 
                JOIN accounts.account_types ats 
                ON rs.account_type_id::INTEGER = ats.id 
                WHERE rs.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/user_accounts', status_code=status.HTTP_200_OK,
#              name="Get all user accounts", response_model=List[UserAccounts])
# async def get_all_user_accounts(request: Request):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT *
#                 FROM accounts.user_accounts"""
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/user_accounts', status_code=status.HTTP_200_OK,
            name="Get user accounts by app_short_code", response_model=List[UserAccounts])
async def get_user_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM accounts.user_accounts WHERE app_short_code = %s""", (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
