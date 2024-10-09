import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header
from psycopg.rows import dict_row

from api.account.model import Account_Types, Accounts, Roles, \
    UserAccounts, RoleWisePoliciesAndPermissions

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/{{accountsManagementUrl}}/accounttypes', status_code=status.HTTP_200_OK,
            name="To get list of account types configured for that app", response_model=List[Account_Types])
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

@router.get('/{{accountsManagementUrl}}/businessaccounttypes', status_code=status.HTTP_200_OK,
            name="To get list of only business type accounts configured for that app", response_model=List[Account_Types])
async def get_business_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE ats.app_short_code = %s AND ats.account_classification = 'Business' 
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

# @router.get('/{{accountsManagementUrl}}/businessaccounttypes', status_code=status.HTTP_200_OK,
#             name="To get list of only business type accounts configured for that app", response_model=List[Accounts])
# async def get_business_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
#     async with request.app.async_pool.psyco_async_pool.connection() as conn:
#         async with conn.cursor(row_factory=dict_row) as cur:
#             await cur.execute("""
#                 SELECT acs.id, acs.app_short_code, acs.display_name, 
#                               mac.display_name AS account_category_display_name, 
#                               ats.display_name AS account_type_display_name, 
#                               ats.account_subcategory, 
#                               acs.address, acs.contactdetails, 
#                               acs.logo_uri, acs.status, 
#                               acs.parent_id, acs.grandparent_id 
#                 FROM accounts.accounts acs 
#                 JOIN accounts.master_account_categories mac 
#                 ON acs.account_category_id = mac.id 
#                 JOIN accounts.account_types ats 
#                 ON acs.account_type_id = ats.id 
#                 WHERE acs.app_short_code = %s AND ats.account_classification = 'Business' 
#             """, (app_short_code,)
#             )
#             results = await cur.fetchall()
#             logger.info(results)
#             return results

@router.get('/{{accountsManagementUrl}}/partneraccounttypes', status_code=status.HTTP_200_OK,
            name="To get list of account types where category = partner", response_model=List[Account_Types])
async def get_partner_accounts_tpyes_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE ats.app_short_code = %s AND ats.account_subcategory LIKE %s 
            """, (app_short_code, '%Partner%')
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/customeraccounttypes', status_code=status.HTTP_200_OK,
            name="To get list of account types where category = customer", response_model=List[Account_Types])
async def get_customer_accounts_tpyes_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE ats.app_short_code = %s AND ats.account_subcategory LIKE %s 
            """, (app_short_code, '%Customer%',)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/roles', status_code=status.HTTP_200_OK,
            name="To get list of roles configured for that app", response_model=List[Roles])
async def get_roles_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
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

@router.get('/{{accountsManagementUrl}}/accounttype/{id}/roles', status_code=status.HTTP_200_OK,
            name="To get list of roles configured for specific account type", response_model=List[Roles])
async def get_roles_by_app_short_code_and_account_type_id(account_type_id, request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT rs.id, rs.app_short_code, ats.display_name AS account_type_name, 
                              rs.display_name, rs.is_it_admin_role
                FROM accounts.roles rs 
                JOIN accounts.account_types ats 
                ON rs.account_type_id::INTEGER = ats.id 
                WHERE rs.app_short_code = %s AND rs.account_type_id = %s 
            """, (app_short_code, account_type_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/roles/{id}/policies_permissions',
            status_code=status.HTTP_200_OK,
            name="To get list of policies & permissions of specific role",
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

@router.get('/{{accountsManagementUrl}}/serviceprovideraccounts', status_code=status.HTTP_200_OK,
            name="To get list of service provider accounts for that app (based on the scope)", response_model=List[Accounts])
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

@router.get('/{{accountsManagementUrl}}/supportaccounts', status_code=status.HTTP_200_OK,
            name="To get list of support accounts for that app (based on the scope)", response_model=List[Accounts])
async def get_support_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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

@router.get('{{accountsManagementUrl}}/partneraccounts', status_code=status.HTTP_200_OK,
            name="To get list of partners accounts for that app (based on the scope)", response_model=List[Accounts])
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

@router.get('/{{accountsManagementUrl}}/servicepartneraccounts', status_code=status.HTTP_200_OK,
            name="To get service partner accounts", response_model=List[Accounts])
async def get_service_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE acs.app_short_code = %s AND ats.account_subcategory = %s
            """, (app_short_code, 'Service Partner')
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/channelpartneraccounts', status_code=status.HTTP_200_OK,
            name="To get channel partner accounts", response_model=List[Accounts])
async def get_service_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE acs.app_short_code = %s AND ats.account_subcategory = %s
            """, (app_short_code, 'Channel Partner')
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/insurancepartneraccounts', status_code=status.HTTP_200_OK,
            name="To get insurance partner accounts", response_model=List[Accounts])
async def get_insurance_partner_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
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
                WHERE acs.app_short_code = %s AND ats.account_subcategory = %s
            """, (app_short_code, 'Insurance Partner')
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/customeraccounts', status_code=status.HTTP_200_OK,
            name="To get list of customer accounts for that app (based on the scope)", response_model=List[Accounts])
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
                WHERE acs.app_short_code = %s AND ats.account_subcategory = %s
            """, (app_short_code, 'Retail Customer')
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/serviceprovideraccounts/{id}/users', status_code=status.HTTP_200_OK,
            name="To get list of user accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_spa_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 1 
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/supportaccounts/{id}/users', status_code=status.HTTP_200_OK,
            name="To get list of user accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_sa_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 2 
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/partneraccounts/{id}/Users', status_code=status.HTTP_200_OK,
            name="To get list of user accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_pa_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 3 
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/PartnerAccounts/{roleid}/Roles/{id}/Users', status_code=status.HTTP_200_OK,
            name="To get list of specific user role accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_pa_roles_accounts_by_app_short_code(role_id,
                                                       request: Request,
                                                       app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                JOIN accounts.roles rs 
                ON uas.user_roleid = rs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 3 AND uas.user_roleid = %s 
            """, (app_short_code, role_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/CustomerAccounts/{id}/Users', status_code=status.HTTP_200_OK,
            name="To get list of user accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_pa_accounts_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 4 
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.get('/{{accountsManagementUrl}}/CustomerAccounts/{roleid}/Roles/{id}/Users', status_code=status.HTTP_200_OK,
            name="To get list of specific user role accounts for selected account for that app (based on the scope)", response_model=List[UserAccounts])
async def get_user_pa_roles_accounts_by_app_short_code(role_id,
                                                       request: Request,
                                                       app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT uas.* 
                FROM accounts.user_accounts uas 
                JOIN accounts.accounts acs 
                ON uas.account_id::UUID = acs.id 
                JOIN accounts.roles rs 
                ON uas.user_roleid = rs.id 
                WHERE uas.app_short_code = %s AND acs.account_category_id = 4 AND uas.user_roleid = %s 
            """, (app_short_code, role_id,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results
