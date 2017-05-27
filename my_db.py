import json

users = {
 'carson': {
   'id': 2,
   'username': 'carson'
 },
 'john':{
   'id': 3,
   'username': 'john'
 }
}

with open('news_v2.json') as data_file:
    news = json.load(data_file)
