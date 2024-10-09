import psycopg
from core import config


class LocalDB():
    def __init__(self):
        self.connection = psycopg.connect(
            f'postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{
                config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}?application_name={config.APP_NAME}'
        )


def create_device(device_id: int, db_connection: psycopg.connection):
    with db_connection.cursor() as cur:
        cur.execute(
            """
            INSERT INTO device.devices VALUES (%s,%s)
            """, ('test', device_id)
        )


def delete_device(device_id: int, db_connection: psycopg.connection):
    with db_connection.cursor() as cur:
        cur.execute(
            """
            DELETE FROM device.devices WHERE device_id = %s
            """, (device_id,)
        )
