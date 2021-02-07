import time
import json

import yorkie

print("Default meter")
@yorkie.measure
def foo1(n:int):
    time.sleep(n)

foo1(0.1)

# Define name
@yorkie.measure('foo2-1')
def foo2(n:int):
    time.sleep(n)
foo2(0.2)

print(json.dumps(yorkie.get_dict(), indent=4))

print("Create new meter")
meter = yorkie.Meter()

# Define name
@meter.measure
def bar1(n:int):
    time.sleep(n)

bar1(0.1)

@meter.measure
def bar2(n:int):
    time.sleep(n)
bar2(0.2)

# No invocation
@meter.measure
def bar3(n:int):
    time.sleep(n)

bar2(0.6)
bar1(0.2)

print(json.dumps(meter.to_dict(), indent=4))


