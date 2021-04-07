import time
import json

def get_file_index_and_prof_index(id):
    file_index = id//5000
    prof_index = id%5000
    return (file_index, prof_index)

s = time.time()
with open('../../full_index_new.json', 'r') as f:
    x = json.load(f)
    e = time.time()
    print(e - s)
    s = e
    if 'neeldhara' in x:  
        for y in x['neeldhara']:
            print(get_file_index_and_prof_index(y[0]), y[1])

end = time.time()
print(end - s)
