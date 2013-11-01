"""Map text schemas to database schemas automatically.

Automatically maps text schemas for sheets (https://github.com/gulopine/sheets)
into database schemas for Pony ORM (http://ponyorm.com).
"""
# Copyright 2013 Imran S. Haque
# ihaque@cs.stanford.edu

# This file is licensed under the GNU Affero General Public License v3
# http://www.gnu.org/licenses/agpl-3.0.html

from datetime import date, datetime
from decimal import Decimal

from pony.orm import Required
import sheets


def _sheets_type_columns(sheets_type):
    is_column_type = lambda name: isinstance(getattr(sheets_type, name),
                                             sheets.Column)
    return filter(is_column_type, dir(sheets_type))


def _pony_schema_from_sheets_schema(schema):
    sheets2pony = {
        sheets.StringColumn: str,
        sheets.UnicodeColumn: unicode,
        sheets.IntegerColumn: int,
        sheets.FloatColumn: float,
        sheets.FloatWithCommaSeparatorsColumn: float,
        sheets.BooleanColumn: bool,
        sheets.DecimalColumn: Decimal,
        sheets.DateTimeColumn: datetime,
        sheets.DateColumn: date
    }
    col_info = {}
    for col_name in _sheets_type_columns(schema):
        sheets_col = getattr(schema, col_name)
        col_info[col_name] = {
            'pony_type': sheets2pony[type(sheets_col)],
            'indexed': getattr(sheets_col, 'indexed', False)
        }
    return {col_name: Required(metadata['pony_type'],
                               index=metadata['indexed'])
            for col_name, metadata in col_info.iteritems()}


def _create_db_schemata(database_file, *schemata):
    from pony.orm import Database
    db = Database('sqlite', database_file)
    models = {}
    for schema in schemata:
        # Build db.Entity objects for the side effect of registering them
        # with the ORM
        models[schema] = type(schema.__name__, (db.Entity,),
                              _pony_schema_from_sheets_schema(schema))
    db.generate_mapping(create_tables=True)
    return db, models


def csv_to_db(file2schema, database_file=':memory:'):
    """Load delimited text files into a database with given schemas.

    Automatically generates schemas for Pony ORM from sheets schemas;
    uses sheets schemas to convert text records into objects, and the
    corresponding Pony schemas to load them into the database.

    `file2schema`: a dict mapping filename to a `sheets` schema class
                   (a subclass of `sheets.Row`) defining the schema
                   with which the file should be parsed

    `database_file`: the filename in which to store the parsed data.
                     Defaults to ':memory:' to keep data in an
                     in-memory DB.

    Returns a tuple (db, models); `db` is the `pony.orm.Database` object
    for the database connection. `models` is a dict mapping `sheets` schema
    classes to `pony.orm` schema classes.

    Extension to sheets language: a sheets Column may have the `indexed`
    attribute set on it to indicate to pony_blanket that the corresponding
    database column should be indexed:

        class SheetsSchema(sheets.Row):
            my_column = StringColumn()
            ...
            # Index `my_column` in the database
            my_column.indexed = True
    """
    from pony.orm import db_session
    # Multiple files may share the same schema, so uniquify them
    db, models = _create_db_schemata(database_file,
                                     *list(set(file2schema.values())))
    with db_session:
        for filename, sheets_type in file2schema.iteritems():
            pony_type = models[sheets_type]
            with open(filename, 'r') as csvdata:
                for row in sheets_type.reader(csvdata):
                    data = {col_name: getattr(row, col_name)
                            for col_name in _sheets_type_columns(sheets_type)}
                    pony_type(**data)
    return db, models
