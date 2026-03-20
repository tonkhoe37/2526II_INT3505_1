# openapi_client.BooksApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_books_get**](BooksApi.md#api_books_get) | **GET** /api/books | Get all books
[**api_books_id_delete**](BooksApi.md#api_books_id_delete) | **DELETE** /api/books/{id} | Delete a book
[**api_books_id_get**](BooksApi.md#api_books_id_get) | **GET** /api/books/{id} | Get book by ID
[**api_books_id_put**](BooksApi.md#api_books_id_put) | **PUT** /api/books/{id} | Update a book
[**api_books_post**](BooksApi.md#api_books_post) | **POST** /api/books | Create a new book


# **api_books_get**
> List[Book] api_books_get()

Get all books

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)

    try:
        # Get all books
        api_response = api_instance.api_books_get()
        print("The response of BooksApi->api_books_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->api_books_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Book]**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of books |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_books_id_delete**
> api_books_id_delete(id)

Delete a book

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = 'id_example' # str | 

    try:
        # Delete a book
        api_instance.api_books_id_delete(id)
    except Exception as e:
        print("Exception when calling BooksApi->api_books_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Book deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_books_id_get**
> Book api_books_id_get(id)

Get book by ID

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = 'id_example' # str | 

    try:
        # Get book by ID
        api_response = api_instance.api_books_id_get(id)
        print("The response of BooksApi->api_books_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BooksApi->api_books_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

[**Book**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Book found |  -  |
**404** | Book not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_books_id_put**
> api_books_id_put(id, body)

Update a book

### Example


```python
import openapi_client
from openapi_client.models.book_update import BookUpdate
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    id = 'id_example' # str | 
    body = openapi_client.BookUpdate() # BookUpdate | 

    try:
        # Update a book
        api_instance.api_books_id_put(id, body)
    except Exception as e:
        print("Exception when calling BooksApi->api_books_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **body** | [**BookUpdate**](BookUpdate.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Book updated |  -  |
**404** | Book not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_books_post**
> api_books_post(body)

Create a new book

### Example


```python
import openapi_client
from openapi_client.models.book import Book
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.BooksApi(api_client)
    body = openapi_client.Book() # Book | 

    try:
        # Create a new book
        api_instance.api_books_post(body)
    except Exception as e:
        print("Exception when calling BooksApi->api_books_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Book**](Book.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Book created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

