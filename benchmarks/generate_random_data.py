import numpy as np
import tables
import json
import sqlite3
import sys

OUTPUT_BASE = sys.argv[1]
POINTS = int(sys.argv[2])

# type = np.float64
np_data = np.random.random(POINTS)
# type = float
py_data = map(float, np_data)

# Output text
with open('%s.txt' % OUTPUT_BASE, 'w') as tf:
    tf.write(' '.join(map(str, py_data)))

# Output JSON
with open('%s.json' % OUTPUT_BASE, 'w') as jf:
    json.dump(py_data, jf)

# Output HDF5
with tables.openFile('%s.h5' % OUTPUT_BASE, 'w') as h5:
    h5.createArray(h5.root, 'data', np_data)

# Output SQLite
db = sqlite3.connect('%s.db' % OUTPUT_BASE)
db.execute('CREATE TABLE data (x REAL);')
db.executemany('INSERT INTO data (x) VALUES (?);',
               ((x,) for x in py_data))
db.commit()
