import time
import inspect
import linecache
import tracemalloc
from copy import deepcopy

from contextlib import ContextDecorator
from collections import defaultdict
from functools import wraps

from typing import Callable, Text, Union

Context = Union[Callable, Text]

class Meter:

    def __init__(self):
        self._measurements = {}

    def __repr__(self):
        measurements = ','.join(self._measurements.keys())
        return "<{} measurements=[{}]>".format(self.__class__.__name__, measurements)

    def measure(self, context:Context, *args, **kwargs):
        if callable(context):
            @wraps(context)
            def wrapper(*args, **kwargs):
                with self.measure(context.__name__):
                    result = context(*args, **kwargs)
                return result
            return wrapper

        if context in self._measurements:
            #length = len(filter(lambda x:x.startswith(name), self._measurements.keys()))
            return self._measurements[context]
        self._measurements[context] = Measure(*args, **kwargs)
        return self._measurements[context]

    def to_dict(self, n_round=4):
        return { k:v.to_dict(n_round) for k,v in self._measurements.items() }

    def get(self, name):
        return self._measurements.get(name)

_meter = Meter()

def _format(trace):
    """Formatting trace"""
    filename, lineno = trace.split(':')
    return "  File \"{}\", line {}\n    {}".format(
            filename, lineno, linecache.getline(filename, int(lineno)).strip())

def _format_size(size):
    unit = ['B', 'KiB', 'MiB', 'GiB', 'TiB']
    for u in unit:
        if size < 1024//10:
            break
        size /= 1024
    return str(round(size,2))+' '+u
        

class Measure(ContextDecorator):

    def __init__(self, measure_memory=False):
        self._begin = None
        self._size = None
        self._measure_memory = measure_memory

        self._logs = []

        frm = inspect.stack()[2]
        self._called_fname = frm[1]

    def __enter__(self):
        self._begin = time.time()
        if self._measure_memory:
            tracemalloc.start(10)
        return self

    def __exit__(self, *exc): 
        end = time.time()

        frm = inspect.stack()[-1]
        context = "{}:{} - \"{}\"".format(frm.filename, frm.lineno, frm.code_context[0])

        self._logs.append({'context': context, 'elapsed': end-self._begin})
 
        if self._measure_memory:
            self._snapshot = snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            size = sum( [stat.size for stat in snapshot.statistics('lineno')] )
            self._size = _format_size(size)
            self._logs[-1]['memory'] = size
            self._logs[-1]['memory_h'] = _format_size(size)

    def trace_memory(self):
        if not self._measure_memory:
            raise Exception("Must set 'measure_memory'=True in order to use '{}'".format(__name__))
        tm = defaultdict(lambda:0)
        for stat in self._snapshot.statistics('traceback'):
            prev = None
            for fname, lineno in stat.traceback._frames: 
                if fname != self._called_fname: continue;
                trace = fname+':'+str(lineno)
                if trace!=prev:
                    tm[trace] += stat.size
                prev = trace
        tm = sorted(tm.items(), key=lambda x:x[1], reverse=True)[:2]
        result = [ (_format(trace), _format_size(memory))for trace, memory in tm ] 
        return result
        
    def to_dict(self, n_round=4):
        if len(self._logs) > 0:
            result = deepcopy(self._logs)
            for i in range(len(result)):
                result[i]['elapsed'] = round(result[i]['elapsed'], n_round)
        else:
            result = None
        return result


def measure(context:Context=None, *args, **kwargs):
    return _meter.measure(context, *args, **kwargs)

def get_dict(n_round=4):
    return _meter.to_dict(n_round)
