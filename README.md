Yorkie
======

A Yorkie will help your task

## Elapsed time

Measure elapsed time in seconds

```python
>>> import yorkie
>>> meter = yorkie.Meter()
>>> with meter.measure("test01"):
...   result = sum( [ i for i in range(10**7) ] )
...   print("test01 result:", result)
...
test01 result: 49999995000000
>>> meter.get("test01").to_dict()
{'elapsed': 0.6926}
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

