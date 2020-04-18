import json

with open('test_data_SanskritLexicalAnalyzer/bg_failing.txt') as f:
  error = json.load(f)


error = error["errors"]

for err in error:
	x = ' '.join(err['split'])
	y = err['orig_split']
	if(x not in y):
		print(x in y)
