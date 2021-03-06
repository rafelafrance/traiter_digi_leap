"""Parse date notations."""

from calendar import IllegalMonthError
from datetime import date

import regex
from dateutil import parser
from dateutil.relativedelta import relativedelta
from traiter.old.vocabulary import LOWEST, Vocabulary

from digi_leap.parsers.base import Base
from digi_leap.pylib import patterns
from digi_leap.pylib.trait import Trait

VOCAB = Vocabulary(patterns.VOCAB)

YEAR_LEN = 2


def convert(token):
    """Normalize a parsed date."""
    trait = Trait(start=token.start, end=token.end)

    value = regex.sub(
        r'[^a-z\d]+', '-', token.group['value'], flags=regex.I | regex.X)

    if len(value) < 4:
        return None

    try:
        trait.value = parser.parse(value).date()
    except (parser.ParserError, IllegalMonthError):
        return None

    if trait.value > date.today():
        trait.value -= relativedelta(years=100)
        trait.century_adjust = True

    trait.value = trait.value.isoformat()[:10]
    return trait


def short_date_name(token):
    """Normalize a month name & year notation."""
    if token.group.get('month') and len(token.group['digits']) < YEAR_LEN:
        return None

    trait = convert(token)
    if trait:
        trait.value = str(trait.value[:-2]) + '??'
    return trait


# Until dateutils IllegalMonthError is fixes do this
def short_date_digits(token):
    """Normalize a month year as all digits notation."""
    digits = token.group['digits']

    has_month = any(x for x in digits if 0 < int(x) <= 12)
    has_year = any(x for x in digits if len(x) >= YEAR_LEN)
    if not (has_month and has_year):
        return None

    trait = convert(token)
    if trait:
        trait.value = str(trait.value[:-2]) + '??'
    return trait


LABEL_DATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        VOCAB['eol'],
        VOCAB['uuid'],  # Get rid of these before they're a problem

        VOCAB.term('label', ' date '.split()),

        VOCAB.part(
            'digits', r'(?<! \d ) ( [12]\d{3} | \d{1,2} ) (?! \d )'),

        VOCAB.part('sep', r' [/_-]+ ', capture=False),

        VOCAB.part('noise', r""" \w+ """, priority=LOWEST, capture=False),

        VOCAB.producer(convert, """
            label? (?P<value> digits sep? month_name sep? digits ) """),

        VOCAB.producer(convert, """
            label? (?P<value> month_name sep? digits sep? digits ) """),

        VOCAB.producer(convert, """
            label? (?P<value> digits sep digits sep digits ) """),

        VOCAB.producer(short_date_digits, f"""
            label? (?P<value> digits sep digits ) """),

        VOCAB.producer(short_date_name, f"""
            label? (?P<value> month_name sep? digits ) """),

        VOCAB.producer(short_date_name, f"""
            label? (?P<value> digits sep? month_name ) """),
    ])
