from openapi_client import ApiClient, Configuration
from openapi_client.api.default_api import DefaultApi

# cấu hình host (mock server)
config = Configuration(host="http://localhost:4010")

client = ApiClient(config)
api = DefaultApi(client)

# gọi API
books = api.api_books_get()

print("Books:", books)
