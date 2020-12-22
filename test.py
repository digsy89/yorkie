import yorkie
import time
import json
import sys

t = yorkie.Time()

with t.measure('test1', measure_memory=True):
    with open("../kowiki-ner-corpus/a.json",'r') as f:
        data = [ json.loads(line) for line in f.readlines() ]
    print(sys.getsizeof(data))

print(t.get('test1').trace_memory())
for trace, size in t.get('test1').trace_memory():
    print(trace, '-', size)

print(t.get('test1').to_dict())

with yorkie.measure('test2', measure_memory=True):
    
    print('test2: ', sum( [ i for i in range(10**7) ] ))

with yorkie.measure('test3'):
    tmp = 0
    for i in range(10**7):
        tmp+=i
    print('test3: ', tmp)

print(yorkie.get_dict())

@yorkie.measure('test4')
def test3():
    time.sleep(0.5)

print(">_<")
test3()

print(yorkie.get_dict())
