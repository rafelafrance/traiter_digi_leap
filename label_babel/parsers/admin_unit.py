"""Parse administrative unit notations."""

from label_babel.pylib.trait import Trait
from label_babel.parsers import us_counties, us_states
from traiter.vocabulary import Vocabulary
from label_babel.parsers.base import Base

VOCAB = Vocabulary(us_counties.VOCAB)


def convert(token):
    """Normalize a parsed date"""
    trait = Trait(start=token.start, end=token.end)

    if token.group.get('us_county'):
        trait.us_county = token.group['us_county'].title()

    if token.group.get('us_state'):
        trait.us_state = us_states.normalize_state(token.group['us_state'])

    return trait


ADMIN_UNIT = Base(
    name='us_county',
    rules=[
        VOCAB['eol'],
        VOCAB['word'],
        VOCAB.term('co_label', r""" co | coun[tc]y """, capture=False),
        VOCAB.term('st_label', r"""
            ( plants | flora ) \s* of """, capture=False),

        VOCAB.producer(convert, ' us_state? eol? co_label comma? us_county '),
        VOCAB.producer(convert, ' us_county co_label comma? us_state? '),
        VOCAB.producer(convert, ' us_county comma? us_state '),
        VOCAB.producer(convert, """
            st_label us_state eol? co_label us_county """),
        VOCAB.producer(convert, ' st_label eol? us_state '),
        VOCAB.producer(convert, ' us_state '),
    ])
