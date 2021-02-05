import time
import inspect
import linecache
import tracemalloc
from contextlib import ContextDecorator
from collections import defaultdict


class Meter:

    def __init__(self):
        self._elapsed = {}

    def __repr__(self):
        return ', '.join([ "{}: {}".format(k, v.elapsed()) for k,v in self._elapsed.items()])

    def measure(self, name, **kwargs):
        if name in self._elapsed:
            length = len(filter(lambda x:x.startswith(name), self._elpased.keys()))
        self._elapsed[name] = Measure(**kwargs)
        return self._elapsed[name]

    def to_dict(self, n_round=4):
        return { k:v.to_dict(n_round) for k,v in self._elapsed.items() }

    def get(self, name):
        return self._elapsed.get(name)

_time = Meter()

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

        frm = inspect.stack()[2]
        self._called_fname = frm[1]

    def __enter__(self):
        self._begin = time.time()
        if self._measure_memory:
            tracemalloc.start(10)
        return self

    def __exit__(self, *exc): 
        self._end = time.time()
        if self._measure_memory:
            self._snapshot = snapshot = tracemalloc.take_snapshot()
            tracemalloc.stop()
            size = sum( [stat.size for stat in snapshot.statistics('lineno')] )
            self._size = _format_size(size)

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
        

    def elapsed(self, n_round=4):
        return round(self._end - self._begin, n_round)

    def to_dict(self, n_round=4):
        result = {'elapsed': self.elapsed(n_round)}
        if self._size:
            result['size'] = self._size
        return result

def measure(name=None, **kwargs):
    return _time.measure(name, **kwargs)

def get_dict(n_round=4):
    return _time.to_dict(n_round)
