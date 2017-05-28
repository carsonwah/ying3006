import json
import io


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

with io.open('news_v2.json','r',encoding='utf8') as data_file:
    news = json.load(data_file)
