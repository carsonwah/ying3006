import json
import io


users = {
 'terence': {
   'id': 1,
   'username': 'terence'
 },
 'carson': {
   'id': 2,
   'username': 'carson'
 },
 'handason':{
   'id': 3,
   'username': 'handason'
 },
 'chris':{
   'id': 4,
   'username': 'chris'
 },
 'john':{
   'id': 5,
   'username': 'john'
 }
}

with io.open('news_v2.json','r',encoding='utf8') as data_file:
    news = json.load(data_file)
