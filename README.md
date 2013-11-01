pydata_nyc_2013
===============

Slides and code from my PyData NYC 2013 talk on Python tools for data wrangling.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
    <img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-sa/3.0/88x31.png" />
</a>
<br />
<span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">
    Slides and code (with the exception of `pony_blanket.py`) for Beyond the dict: Python Tools for Data Wrangling
</span> by
<a xmlns:cc="http://creativecommons.org/ns#" href="https://cs.stanford.edu/people/ihaque" property="cc:attributionName" rel="cc:attributionURL">
    Imran S Haque
</a>
are licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/deed.en_US">
    Creative Commons Attribution-ShareAlike 3.0 Unported License
</a>.

The `pony_blanket` module is licensed for open-source use under the
[GNU Affero General Public License v3](http://www.gnu.org/licenses/agpl-3.0.html) to comply
with the open-source license terms of [Pony ORM](http://ponyorm.com).

# Code included

## `pony_blanket`: Automatic text <-> database adapter

The `pony_blanket` module is an adapter between the schemas defined by Marty Alchin's
[`sheets` module](https://github.com/gulopine/sheets), providing
schematized parsing for delimited text data, and [Pony ORM](http://ponyorm.com), an ORM
for Python with Pythonic syntax and little boilerplate. `pony_blanket` allows you to create
a schema once, for `sheets`, and have that automatically turned into a schema for `pony.orm`:


```python
from sheets import Row, Dialect
from sheets import StringColumn, FloatColumn

class HapMapAllele(Row):
    Dialect = Dialect(has_header_row=True,
                      delimiter=' ')
    rsid = StringColumn()
    ref_freq = FloatColumn()
    alt_freq = FloatColumn()

    # pony_blanket extension to sheets
    # set the `indexed` attribute on any sheets column to index the
    # corresponding column in the database model
    alt_freq.indexed = True

from pony_blanket import csv_to_db
from pony.orm import db_session, select

db, models = csv_to_db({'hapmap.txt': HapMapAllele})

# Query the database to find loci with high frequency of the alternate allele
with db_session:
    print len(select(x for x in models[HapMapAllele]
                     if x.alt_freq > 0.01))
```

By default, `csv_to_db` will load the given files into an in-memory SQLite3 database
(`sqlite3.connect(':memory:')`).

## Numeric benchmarks

The code in `benchmarks/` generates the stats listed in my slide on numeric-storage performance.
Please don't complain about the different ways that I'm Doing It Wrong -- there are definitely
more efficient ways to do numeric storage (particularly in SQL). The point of these benchmarks is
to get order-of-magnitude estimates on the efficiency of storing numeric data in different formats
using the most obvious means in the respective libraries.

To regenerate the benchmarks, you will need the [`tables`](http://pytables.org) module installed. Just
run the Makefile inside the `benchmarks/` directory.

## Code snippets

The example code snippets on my slides are included in the `snippets/` directory in case it's easier
for someone to copy-paste from there. I offer no guarantees on whether they do the right thing for you.
