import logging
from typing import List
from fastapi import APIRouter, Request, status, FastAPI, Header, HTTPException
from psycopg.rows import dict_row
from psycopg.types.json import Json
from api.ticket.model import Tickets, TicketCreateRequest

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()
app = FastAPI()

@router.get('/tickets', status_code=status.HTTP_200_OK,
            name="Get tickets by app_short_code", response_model=List[Tickets])
async def get_tickets_by_app_short_code(request: Request, app_short_code: str = Header(..., alias="app_short_code")):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT ts.id, ts.app_short_code, ts.category, ts.problem_statement, 
                              acs.display_name AS alloted_to, 
                              ts.original_email, 
                              ts.contact_details_mentioned_in_email, 
                              ts.ai_diagnostics, ts.ai_prescriptions, ts.job_summary, 
                              ts.media_uploads, ts.current_status, ts.created_by, 
                              ts.created_on, ts.updated_by, ts.updated_on, 
                              ts.ticket_created_by, ts.ticket_updated_by, 
                              ts.ticket_short_code, 
                              uas.user_fullname AS assigned_to, 
                              cua.display_name AS customer_fullname 
                FROM tickets.tickets ts 
                JOIN tickets.ticket_assignee tae 
                ON ts.ticket_short_code = tae.ticket_short_code 
                JOIN accounts.user_accounts uas 
                ON tae.servicetechnician_id = uas.account_id::UUID AND tae.serviceaccount_id = uas.id 
                JOIN accounts.accounts acs 
                ON tae.servicetechnician_id = acs.id 
                JOIN accounts.accounts cua 
                ON ts.customer_id = cua.id 
                WHERE ts.app_short_code = %s
            """, (app_short_code,)
            )
            results = await cur.fetchall()
            logger.info(results)
            return results

@router.post('/tickets', status_code=status.HTTP_201_CREATED, name="Create Ticket")
async def create_ticket(request: Request, ticket_request: TicketCreateRequest):
    async with request.app.async_pool.psyco_async_pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT * 
                FROM accounts.accounts 
                WHERE contactdetails->>'contactemail' = %s 
            """, (ticket_request.original_email.senderemail,))
            contact_details = await cur.fetchone()
            # logger.info(contact_details)

            if contact_details:
                contact_details_mentioned_in_email = contact_details['contactdetails']
                # contact_details_mentioned_in_email = {
                #     "contactname" : contact_details["user_login"],
                #     "contactemail" : contact_details["user_email"],
                #     "contactnumber": contact_details["user_mobile"]
                # }
                # customer_id = contact_details['id']
                customer_id = '04baa1af-5850-4f58-9529-957e5dcebc6e'
            else:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Contact Details not found for {ticket_request.original_email.senderemail}")

            await cur.execute("""
                INSERT INTO tickets.tickets(
                    app_short_code, category, problem_statement, customer_id, original_email, 
                    contact_details_mentioned_in_email, ai_diagnostics, ai_prescriptions, media_uploads, 
                    current_status)
                VALUES (%s, %s, %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb, %s) 
                RETURNING ticket_short_code, app_short_code 
            """, (
                ticket_request.app_short_code,
                ticket_request.category,
                ticket_request.problem_statement, 
                customer_id,
                Json(ticket_request.original_email.model_dump()),
                Json(contact_details_mentioned_in_email), 
                Json(ticket_request.ai_diagnostics),
                Json(ticket_request.ai_prescriptions), 
                Json([attachment.model_dump() for attachment in ticket_request.original_email.emailattachments]),
                "New"
            ))
            ticket = await cur.fetchone()
            ticket_short_code = ticket['ticket_short_code']
            # app_short_code = ticket['app_short_code']

            # await cur.execute("""
            #     SELECT id, account_id 
            #     FROM accounts.user_accounts WHERE app_short_code = %s AND user_fullname = %s """,
            #     (app_short_code, 'Field Service Two Technician',)
            # )
            # results = await cur.fetchone()
            await cur.execute("""
                INSERT INTO tickets.ticket_assignee(ticket_short_code, serviceaccount_id, servicetechnician_id) 
                VALUES (%s, %s, %s) 
            """, (ticket_short_code, '0998e1cb-1c76-4b6c-85de-58cd7d66b3f8', 'ee95f31d-31cf-429d-9e36-f46ea7ae5959',))
            # await cur.execute("""
            #     INSERT INTO tickets.ticket_assignee(ticket_short_code, serviceaccount_id, servicetechnician_id) 
            #     VALUES (%s, %s, %s) 
            # """, (ticket_short_code, results['id'], results['account_id'],))

            await conn.commit()

    logger.info({"status": "success", "message": "Ticket created successfully"})
    return {"status": "success", "message": "Ticket created successfully"}
