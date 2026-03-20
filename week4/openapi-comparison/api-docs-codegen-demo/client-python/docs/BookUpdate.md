# BookUpdate


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**author** | **str** |  | [optional] 
**price** | **float** |  | [optional] 

## Example

```python
from openapi_client.models.book_update import BookUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of BookUpdate from a JSON string
book_update_instance = BookUpdate.from_json(json)
# print the JSON string representation of the object
print(BookUpdate.to_json())

# convert the object into a dict
book_update_dict = book_update_instance.to_dict()
# create an instance of BookUpdate from a dict
book_update_from_dict = BookUpdate.from_dict(book_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


