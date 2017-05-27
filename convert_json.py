import json
f = open('news.json','r')
data = json.load(f)
f.close()

result = {}
for i in xrange(len(data)):
    key = data[i][u'code.i.']
    del data[i][u'code.i.']
    if key not in result:
        result[key] = [data[i]]
    else:
        result[key] += [data[i]]

output = open('news_v2.json','w')
output.write(json.dumps(result).encode('utf8'))
output.close()
