import sys
from baseconv import BaseConverter

from random import randint, SystemRandom

colors2 = ["red darken-4", "purple darken-4", "pink darken-4", "deep-purple darken-4", "indigo darken-4",
           "blue darken-4", "light-blue darken-4", "cyan darken-4", "teal darken-4", "green darken-4",
           "light-green darken-4", "lime darken-4", "orange darken-4", "deep-orange darken-4", "brown darken-4",
           "blue-grey darken-4", "grey darken-4", "yellow darken-4"]

characters = 'abcdefghkmnpqrstwxyz'
digits = '23456789'
base = characters + characters.upper() + digits
number_converter = BaseConverter(base)


def pick_color():
    num = randint(0, len(colors2))
    return colors2[num]


def id_generator():
    return SystemRandom().randint(1, sys.maxsize)


def gen_short_id(long_id):
    return number_converter.encode(long_id)


def get_long_id(short_id):
    return number_converter.decode(short_id)