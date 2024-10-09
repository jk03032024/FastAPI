import psycopg_pool
from core import config
from azure.cosmos import CosmosClient, ContainerProxy
from azure.identity import DefaultAzureCredential

#conn_string = f'postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}?application_name={config.APP_NAME}'
conn_string = f'host={config.POSTGRES_HOST} user={config.POSTGRES_USER} password={config.POSTGRES_PASSWORD} dbname={config.POSTGRES_DB} port={config.POSTGRES_PORT}'

class DBConnectionPool:
    def __init__(self):
        self.psyco_async_pool: psycopg_pool.AsyncConnectionPool = psycopg_pool.AsyncConnectionPool(
            conn_string,
            min_size=4,
            max_size=10,
            open=False
        )
        
    async def close(self):
        await self.psyco_async_pool.close()

class CosmoseConnectionTool:
    def __init__(self):
        self.client: CosmosClient = CosmosClient(config.COSMOS_DB_ENDPOINT, config.COSMOS_DB_KEY, connection_verify=False)
        self.database_name = config.COSMOS_DB_DATABASE_NAME
        self.data_container_name = config.COSMOS_DB_DATA_CONTAINER_NAME
        self.event_container_name = config.COSMOS_DB_EVENT_CONTAINER_NAME
        self.security_container_name = config.COSMOS_DB_SECURITY_CONTAINER_NAME
        self.heartbeats_container_name = config.COSMOS_DB_HEARTBEATS_CONTAINER_NAME
        self.lifecycle_container_name = config.COSMOS_DB_LIFECYCLE_CONTAINER_NAME
        self.sitewise_container_name = config.COSMOS_DB_SITEWISE_CONTAINER_NAME
        self.container: ContainerProxy = None

    def connect(self):
        database = self.client.get_database_client(self.database_name)
        self.data_container = database.get_container_client(self.data_container_name)
        self.event_container = database.get_container_client(self.event_container_name)
        self.security_container = database.get_container_client(self.security_container_name)
        self.heartbeats_container = database.get_container_client(self.heartbeats_container_name)
        self.lifecycle_container = database.get_container_client(self.lifecycle_container_name)
        self.sitewise_container = database.get_container_client(self.sitewise_container_name)

    def data_query_items(self, query: str, parameters: dict):
        return list(self.data_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def event_query_items(self, query: str, parameters: dict):
        return list(self.event_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def security_query_items(self, query: str, parameters: dict):
        return list(self.security_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def heartbeats_query_items(self, query: str, parameters: dict):
        return list(self.heartbeats_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def lifecycle_query_items(self, query: str, parameters: dict):
        return list(self.lifecycle_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def sitewise_query_items(self, query: str, parameters: dict):
        return list(self.sitewise_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

class CosmoseConnectionToolNew:
    def __init__(self):
        aad_credentials = DefaultAzureCredential()
        self.client: CosmosClient = CosmosClient(config.COSMOS_DB_ENDPOINT, aad_credentials)
        self.database_name = config.COSMOS_DB_DATABASE_NAME
        self.data_container_name = config.COSMOS_DB_DATA_CONTAINER_NAME
        self.event_container_name = config.COSMOS_DB_EVENT_CONTAINER_NAME
        self.security_container_name = config.COSMOS_DB_SECURITY_CONTAINER_NAME
        self.container: ContainerProxy = None

    def connect(self):
        database = self.client.get_database_client(self.database_name)
        self.data_container = database.get_container_client(self.data_container_name)
        self.event_container = database.get_container_client(self.event_container_name)
        self.security_container = database.get_container_client(self.security_container_name)

    def data_query_items(self, query: str, parameters: dict):
        print("INFO: New Cosmose Coonection")
        return list(self.data_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def event_query_items(self, query: str, parameters: dict):
        print("INFO: New Cosmose Coonection")
        return list(self.event_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))

    def security_query_items(self, query: str, parameters: dict):
        print("INFO: New Cosmose Coonection")
        return list(self.security_container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
