import requests
import json
import pandas as pd



api__Key = "nice-try-getting-api-key"
api__URI = "https://api.monday.com/v2"

headers = {"Authorization" : api__Key}

search__Query_board_items = 'query {boards (ids: 00000000) {groups {id title}}}' #Queries all groups in a board. Includes groupID which you can use to query next variable.
search__Query_StartEndTime = '{boards(ids: 00000000) {groups (ids:"group_name") {title id items_page(limit: 100) {cursor items {id name column_values {... on TimelineValue {text}}}}}}}' #Outputs timeline values (both start and end + all item names)


data_board_item = {'query': search__Query_board_items}
data_startEndTime = {'query': search__Query_StartEndTime}

Query_boardItems = requests.post(url=api__URI, json=data_board_item, headers=headers)
Query_StartEndTime = requests.post(url=api__URI, json=data_startEndTime, headers=headers)

json_data_boarditems = json.loads(Query_boardItems.text)
json_data_StartEndTime = json.loads(Query_StartEndTime.text)



parsed_JSON__boardItem = pd.json_normalize(json_data_boarditems['data']['boards'][0]['groups'])
parsed_JSON__StartEndTime = pd.json_normalize(json_data_StartEndTime['data']['boards'][0]['groups'][0]['items_page']['items'],record_path='column_values', meta=['name'])
print(parsed_JSON__boardItem)
print(parsed_JSON__StartEndTime.head(5))



