from snownlp import SnowNLP
with open('/Users/johnhongokchao/Desktop/news.json') as data_file:    
    data = json.load(data_file)
emotion=[]
for i in range(250):
	s=SnowNLP(data[i]["text"])
	t=s.han
	t=SnowNLP(t)
	data[i]["sentiment"]=t.sentiments
	data[i]["keywords"]=t.keywords(3)

with open('/Users/johnhongokchao/Desktop/news.json', 'w') as outfile:
    json.dump(data, outfile,indent=4)
