#
# invitae-hw-variant-search/src/invitae-vs-core/invitae_vs_core/vs_core.py ---
#

"""
FIXME
"""

from __future__ import (
    absolute_import,
    division,
    print_function,
)

import math
import os
import pdb
import pprint
import re
import sys

import pandas
import sqlalchemy as sa

from .models import *
from .util import (
    safe_int,
)

#####

#:
INVITAE_VS_CLIENT = os.environ.get("INVITAE_VS_CLIENT")
#:
INVITAE_VS_DEPLOY = os.environ.get("INVITAE_VS_DEPLOY")
#:
INVITAE_VS_DB_URI = os.environ.get("INVITAE_VS_DB_URI")
#:
INVITAE_VS_DEBUG = int(os.environ.get("INVITAE_VS_DEBUG", 0))

#####


class VS_Core(object):

    def __init__(
            self,
            *args,
            db_uri=None,
            db_echo=None,
            debug=None,
            **kwargs):
        #
        self._debug = INVITAE_VS_DEBUG
        if debug is not None:
            self._debug = debug
        #
        self._db_uri = db_uri or INVITAE_VS_DB_URI
        self._db_echo = db_echo or False
        #
        self._db_engine = None
        self._db_Session = None
        self._db_session = None

    def __repr__(self):
        return "#<{} {:#x} {!r}>".format(
            self.__class__.__name__,
            id(self),
            self._db_uri)

    ###

    def db_engine(self):
        """Gets our db engine."""
        if self._db_engine:
            return self._db_engine
        #
        self._db_engine = sa.create_engine(
            self._db_uri,
            encoding='latin1',
            echo=self._db_echo,
            poolclass=sqlalchemy.pool.NullPool)
        #
        self._db_Session = sqlalchemy.orm.sessionmaker(
            bind=self._db_engine)
        #
        return self._db_engine

    def db_session(self):
        self.db_engine()
        return self._db_Session()

    def db_create_tables(self):
        """Create our tables."""
        return ModelBase.metadata.create_all(
            self.db_engine())

    ###

    def col_rename_func(self, col_name):
        """Turn a column name like 'Protein Change' into 'protein_change'."""

        new_name = col_name.lower()
        new_name = new_name.replace(" ", "_")
        if self._debug:
            print("column_rename_func: {!r}->{!r}", col_name, new_name)
        return new_name

    def db_data_load(
            self,
            path: str) -> bool:
        #
        df = pandas.read_csv(
            path,
            index_col=False,
            dtype='str',
            delimiter="\t")

        # map column names.
        df.rename(
            self.col_rename_func,
            axis='columns',
            inplace=True)

        #
        if self._debug:
            print("df=")
            print(df[0:5])

        df.to_sql(
            name=Variant.__tablename__,
            con=self.db_engine(),
            #
            index=False,
            # we made the table already.
            if_exists='append')

    ###

    def parse_range(self, value):
        """Parse a range value.

        START:END -> [start, end]
        START:    -> [start, inf]
        :END      -> [0 , end]

        VALUE     -> value
        """

        if value is None:
            return None

        if isinstance(value, list):
            return value

        m = re.match("(?P<start>\\d+)?(?P<colon>:)?(?P<stop>\\d+)?", value)
        if not m:
            return None

        start = m.group("start")
        colon = m.group("colon")
        stop = m.group("stop")

        if start:
            start = int(start)
        if stop:
            stop = int(stop)

        return [start, colon, stop]

    def query_variant(
            self,
            q_gene_name=None,
            q_gene_like=None,
            q_genomic_start_range=None,
            q_genomic_stop_range=None,
            q_limit=None):

        #
        q = self.db_session().query(Variant)

        print(f"{q_gene_name=}")
        print(f"{q_gene_like=}")
        print(f"{q_genomic_start_range=}")
        print(f"{q_genomic_stop_range=}")
        print(f"{q_limit=}")


        if q_gene_name:
            if "%" in q_gene_name:
                q = q.filter(Variant.gene.like(q_gene_name))
            else:
                q = q.filter(Variant.gene == q_gene_name)

        if q_gene_like:
            q = q.filter(Variant.gene.like(q_gene_like))

        #
        for (col_name, col_range) in [
                ["genomic_start",
                 self.parse_range(q_genomic_start_range)],
                ["genomic_stop",
                 self.parse_range(q_genomic_stop_range)],
        ]:
            if col_range:
                (start, colon, stop) = col_range
                if colon is None and start:
                    q = q.filter(getattr(Variant, col_name) == start)
                else:
                    if start:
                        q = q.filter(getattr(Variant, col_name) >= start)
                    if stop:
                        q = q.filter(getattr(Variant, col_name) <= stop)

        # apply a default order
        q.order_by(Variant.id)

        # apply limit
        q_limit = safe_int(q_limit)
        if q_limit:
            q = q.limit(q_limit)

        #
        data = q.all()
        return data

    def rows_print(
            self,
            rows,
            col_names):
        """Print a table of rows.
        """
        #
        print("{:<15}".format("IDX"), end="")
        for col_name in col_names:
            print(f"{col_name:<15}", end="")
        print()

        #
        for row_idx, row in enumerate(rows):
            print(f"{row_idx:<15}", end="")
            for col_name in col_names:
                col_value = str(getattr(row, col_name))
                print(f"{col_value:<15}", end="")
            print()

        return True

    def gene_autocomplete(self,prefix):
        """Suggest the next char after the prefix.

        While are test data is small enough to send the entire list,
        presumably we have lots of genes and we dont want to send the
        entire list to the client.

        So the client gives us the prefix and we build the suggestion list
        which just has the next character.
        """

        # clean up prefix
        if not prefix:
            prefix=""
        prefix=prefix.upper()

        print(f"gene_autocomplete: {prefix=}")

        q = self.db_session().query(
            sqlalchemy.sql.func.substr(Variant.gene,1,len(prefix)+1).distinct().label("next_chars"))
        q=q.filter(Variant.gene.like(prefix+"%"))

        print("Q=",q)

        rows=q.all()
        rows=[row[0] for row in rows]
        rows=sorted(rows)
        return rows
