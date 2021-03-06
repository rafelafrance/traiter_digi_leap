"""Find collector notations on herbarium specimen labels."""

from itertools import zip_longest

import regex
from traiter.old.vocabulary import LOWEST, Vocabulary
from traiter.util import squash

from digi_leap.parsers import name_parts
from digi_leap.parsers.base import Base
from digi_leap.parsers.us_states import STATE_NAMES
from digi_leap.pylib.trait import Trait

VOCAB = Vocabulary(name_parts.VOCAB)

MIN_LEN = 5  # Minimum collector name length


def convert(token):
    """Build a collector trait"""
    names = regex.split(
        r'\s*(?:and|with|[,&])\s*',
        token.group.get('col_name'))

    traits = []

    for name, suffix in zip_longest(names, names[1:], fillvalue=''):
        name = regex.sub(r'\.{3,}.*', '', name)
        if len(name) < MIN_LEN:
            continue

        trait = Trait(start=token.start, end=token.end)
        trait.col_name = name

        if suffix.lower() in name_parts.SUFFIXES:
            trait.col_name = f'{name} {suffix}'

        if name.lower() not in name_parts.SUFFIXES:
            traits.append(trait)

    if not traits:
        return None

    if token.group.get('collector_no'):
        col_no = token.group['collector_no']
        # Temp hack
        if col_no[-1] in ('m', 'M'):
            return None
        traits[0].col_no = col_no

    return squash(traits)


COLLECTOR = Base(
    name='collector',
    rules=[
        VOCAB['eol'],
        VOCAB['month_name'],
        STATE_NAMES,

        VOCAB.part('col_label', r"""
            \b ( collect(or|ed) | coll | col ) ( \s* by )? 
            """, capture=False),

        VOCAB.term(
            'no_label', r""" number no num """.split(), capture=False),

        VOCAB.term(
            'part', r""" [[:alpha:]]+ """, priority=LOWEST, capture=False),

        VOCAB.term('other_label', r"""
            art artist ass assist assistant auth authors?
            cartographer conservator contributor corator curator curatorial
            det determiner dir director
            ecologist editor entomologist expedition explorer extractor
            gardener geographer geologist georeferencer grower
            herbarium horticulturalist
            illustrator
            manager
            naturalist
            preparator
            researcher
            volunteers?
            writer
            """.split(), capture=False),

        VOCAB.part('noise', r" [_`‘|\[\]/-]+ "),
        VOCAB.term('header_key', r' herbarium '.split()),

        VOCAB.term('junk', r' date '.split()),

        VOCAB.term('skip', """ of on dry """.split()),
        VOCAB.part('semi', r' [;] '),

        VOCAB.term('col_no', r"""
            [[:alpha:][:digit:]\-]+ (?! [.] )""", priority=LOWEST),

        VOCAB.grouper('collector', """
            ( (name_part | initial) )+ 
            ( name_part | part | initial )* """, capture=False),

        VOCAB.grouper('joiner', ' ( conj | comma | with ){1,2} '),

        # With a label
        VOCAB.producer(convert, """
            (?<= ^ | eol )
            (?<! other_label comma? name_part? ) (?<! part | col_no )
                noise? col_label comma? noise?
                (?P<col_name> collector
                    ( joiner collector )* ( comma name_part )? )
                noise?
            ( eol* ( (no_label? comma? (?P<collector_no> col_no )
                | no_label comma?
                    (?P<collector_no> ( part | col_no ){1,2} ) ) ) )?
                """),

        # Without a label
        VOCAB.producer(convert, """
            (?<= ^ | eol )
            (?<! other_label noise? name_part? )  (?<! part | col_no )
            noise? col_label? comma? noise?
            (?P<col_name> initial? name_part+ ( joiner collector )* )
            ( eol* ( (no_label? comma? (?P<collector_no> col_no )
                | no_label comma?
                    (?P<collector_no> ( part | col_no ){1,2} ) ) ) )?
            (?! header_key )
            (?= month_name | col_no | eol | $ ) """),

        VOCAB.producer(convert, """
            (?P<col_name> collector ) (?P<collector_no> col_no)
            """),
    ])
