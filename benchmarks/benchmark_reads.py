import sys
import json
import sqlite3
import tables
from time import time
from os.path import getsize


def read_text(filename):
    with open(filename, 'r') as txtf:
        data = map(float, txtf.read().strip().split(' '))
    return data


def read_hdf5(filename):
    with tables.openFile(filename, 'r') as h5:
        data = h5.root.data[:]
    return data


def read_sqlite(filename):
    db = sqlite3.connect(filename)
    return db.execute('SELECT * FROM data;').fetchall()


def read_json(filename):
    with open(filename, 'r') as jf:
        return json.load(jf)


def benchmark(func, filename, iters):
    times = []
    for i in xrange(iters):
        start = time()
        func(filename)
        end = time()
        times.append(end - start)

    return min(times)

FORMAT_TO_SUFFIX_HANDLER = {
    'HDF5': ('h5', read_hdf5),
    'Text': ('txt', read_text),
    'JSON': ('json', read_json),
    'SQLite3': ('db', read_sqlite)
}

ITERS = 10


def benchmark_size_overhead(base_name, data_units):
    # 8b per double
    minimum_size = 8 * data_units

    def overhead(filename):
        return 100 * float(getsize(filename) - minimum_size) / minimum_size

    print 'Size Overhead (%d elements)' % data_units
    for fmt, (suffix, handler) in FORMAT_TO_SUFFIX_HANDLER.iteritems():
        print fmt, ': %f %%' % overhead('%s.%s' % (base_name, suffix))

if __name__ == '__main__':
    base_name = sys.argv[1]
    data_units = read_hdf5('%s.h5' % base_name).shape[0]

    benchmark_size_overhead(base_name, data_units)
    0/0
    print
    print 'Best time to read %d doubles by format over %d tries' % (
        data_units, ITERS)
    for fmt, (suffix, handler) in FORMAT_TO_SUFFIX_HANDLER.iteritems():
        readtime = benchmark(handler, '%s.%s' % (base_name, suffix), ITERS)
        print fmt, ': %f ms' % (readtime * 1000)
