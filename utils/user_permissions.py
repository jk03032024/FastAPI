import logging

from fastapi import Body, FastAPI, Request, HTTPException, status

from utils.model import UserID

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

class CheckUserPermissions:

    def __init__(self, required_permissions: str) -> None:
        self.required_permissions = required_permissions

    async def __call__(self, user: UserID, request: Request) -> bool:
        async with request.app.async_pool.psyco_async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT user_access 
                    FROM users.user_permissions WHERE user_id = %s""", (user.user_id,)
        
                                )
                results = [entry[0] for entry in await cur.fetchall()]

        if self.required_permissions not in results:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'User {user.user_id} is not autothorize to {self.required_permissions}'
            )
        return True