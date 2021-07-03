#
# src/invitae-vs-core/invitae_vs_core/models.py ---
#

from __future__ import (
    absolute_import,
)

import sqlalchemy as sa
import sqlalchemy.orm

#####

ModelBase = sqlalchemy.orm.declarative_base()


class Variant(ModelBase):

    __tablename__ = "variant"

    #
    id = sa.Column(
        sa.Integer(),
        primary_key=True)
    #
    gene = sa.Column(
        sa.String())
    nucleotide_change = sa.Column(
        sa.String())
    protein_change = sa.Column(
        sa.String())
    other_mappings = sa.Column(
        sa.String())
    alias = sa.Column(
        sa.String())
    transcripts = sa.Column(
        sa.String())
    region = sa.Column(
        sa.String())
    reported_classification = sa.Column(
        sa.String())
    inferred_classification = sa.Column(
        sa.String())
    source = sa.Column(
        sa.String())
    last_evaluated = sa.Column(
        sa.String())
    last_updated = sa.Column(
        sa.String())
    url = sa.Column(
        sa.String())
    submitter_comment = sa.Column(
        sa.String())
    assembly = sa.Column(
        sa.String())
    chr = sa.Column(
        sa.String())
    genomic_start = sa.Column(
        sa.Integer())
    genomic_stop = sa.Column(
        sa.Integer())
    ref = sa.Column(
        sa.String())
    alt = sa.Column(
        sa.String())
    accession = sa.Column(
        sa.String())
    reported_ref = sa.Column(
        sa.String())
    reported_alt = sa.Column(
        sa.String())
