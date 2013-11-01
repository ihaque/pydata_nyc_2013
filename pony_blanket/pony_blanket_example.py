from sheets import Row, Dialect
from sheets import StringColumn, FloatColumn
from pony.orm import db_session, select
from pony_blanket import csv_to_db


class HapMapAllele(Row):
    Dialect = Dialect(has_header_row=True, delimiter=' ')
    rsid = StringColumn('rs#')
    ref_freq = FloatColumn('refallele_freq')
    alt_freq = FloatColumn('otherallele_freq')

    # Extension to pass info to the ORM
    rsid.indexed = True
    alt_freq.indexed = True


def main(csvfile):
    db, models = csv_to_db({csvfile: HapMapAllele})
    hmalleles = models[HapMapAllele]
    with db_session:
        print select(x for x in hmalleles if x.rsid ==
                     'rs6423165')[:][0].ref_freq
        print len(select(x.rsid for x in hmalleles
                         if x.alt_freq > 0.01))


if __name__ == '__main__':
    import sys
    main(csvfile=sys.argv[1])
