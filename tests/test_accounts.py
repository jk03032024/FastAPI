from fastapi.testclient import TestClient
from main import app
from api.account import account
from api.account.model import Account

client = TestClient(app)

def get_account():
    with client():
        a = 0


