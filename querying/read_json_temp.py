import time
import json
with open('../indexing/full_index.json', 'r') as f:
    x = json.load(f)
    start = time.time()
    if 'machin' in x:  
        print(len(x['machin']))

end = time.time()
print(end - start)
