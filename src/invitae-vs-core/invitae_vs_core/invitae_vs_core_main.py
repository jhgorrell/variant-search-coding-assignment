#
# invitae-vs-core/invitae_vs_core/invitae_vs_core_main.py ---
#
#

from __future__ import (
    absolute_import,
    division,
    print_function,
)

import argparse
import os
import pdb
import sys

from .util import *
from .vs_core import *

#####


def main(raw_args):
    """
    The main for ``invitae-vs-core``.
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.description = """
DESCRIPTION:

FIXME

"""
    parser.epilog = """
EXAMPLES:

FIXME

"""

    g = parser.add_argument_group('GENERAL')

    g.add_argument("--debug", "-d",
                   nargs="?",
                   default=0,
                   type=int,
                   help=argparse.SUPPRESS)
    g.add_argument("--pdb",
                   action="store_true",
                   help=argparse.SUPPRESS)
    g.add_argument("--verbose", "-v",
                   action="store_true",
                   help="Be more verbose.")

    g = parser.add_argument_group(
        "Invitae Variant Search DB",
        description="DB stuff")

    g.add_argument("--db-uri",
                   help="The URI of database connection")

    g.add_argument("--db-echo",
                   action="store_true",
                   help="Echo DB commands.")

    g.add_argument("--db-create-tables",
                   action="store_true",
                   help="Creates the tables in the DB.")

    g.add_argument("--db-data-load",
                   action="append",
                   help="Load the data from the TSV file.")

    g = parser.add_argument_group(
        "Invitae Variant Search Queries",
        description="Query the DB for stuff.")

    g.add_argument("--gene-autocomplete",
                   help="Print autocompletions for the gene. (next characters.)")

    g.add_argument("--q-limit",
                   type=int,
                   help="Limit the output rows.")

    g.add_argument("--q-gene-like",
                   help="Query gene names with 'like'.")

    g.add_argument("--q-genomic-start",
                   help="A range of values like 'START:STOP'")

    g.add_argument("--q-genomic-stop",
                   help="A range of values like 'START:STOP'")

    args = parser.parse_args(raw_args)

    if args.pdb:
        pdb.set_trace()

    vs_core = VS_Core(
        db_uri=args.db_uri,
        db_echo=args.db_echo)
    print(f"{vs_core=}")

    # DB
    if args.db_create_tables:
        vs_core.db_create_tables()

    if args.db_data_load:
        for path in args.db_data_load:
            vs_core.db_data_load(path=path)
            return True

    # suggest

    if args.gene_autocomplete is not None:
        print("Suggestions for gene prefix:")
        print(vs_core.gene_autocomplete(
            prefix=args.gene_autocomplete))
        return True

    # Query
    rows = vs_core.query_variant(
        q_limit=args.q_limit,
        q_gene_like=args.q_gene_like,
        q_genomic_start_range=args.q_genomic_start,
        q_genomic_stop_range=args.q_genomic_stop)

    vs_core.rows_print(
        rows,
        col_names=[
            "id",
            "gene",
            "genomic_start",
            "genomic_stop",
        ])

    return True


def main_entry():
    """
    The entry point for main.
    Used to cast the return value to a numeric value.
    """
    sys.exit(cast_rv(main(sys.argv[1:])))


if __name__ == "__main__":
    main_entry()
