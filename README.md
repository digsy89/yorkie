Yorkie
======

A Yorkie will help your experiment

## Elapsed time

Measure elapsed time in seconds

```python
import time                    
import yorkie                  

# with context manager
with yorkie.measure('test1'):  
    time.sleep(0.123)          

# with decorator
@yorkie.measure                
def foo(sec):                  
    time.sleep(sec)            
                               
foo(0.456)                     
foo(1.0)                       

print(yorkie.get_dict())
```
stdout >>
```python
{
    'test1': [
        {'context': '/home/ubuntu/yorkie/examples/example.py:4 - "with yorkie.measure(\'test1\'):\n"', 'elapsed': 0.1234}], 
    'foo': [
        {'context': '/home/ubuntu/yorkie/examples/example.py:14 - "foo(0.456)\n"', 'elapsed': 0.4568},
        {'context': '/home/ubuntu/yorkie/examples/example.py:15 - "foo(1.0)\n"', 'elapsed': 1.0015}
    ]
}
```

## Memory usage

Approximate memory usage. 
> :warning: Make script slow

```python
>>> import json
>>> with meter.measure("test02", measure_memory=True):
...   with open("sample.txt",'r') as f:
...     data = [ json.loads(line) for line in f.readlines() ]
... 
>>> meter.get("test02").to_dict()
{'elapsed': 0.5983, 'size': '11.29 MiB'}
```

