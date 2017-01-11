from random import randint

colors2 = ["red darken-4", "purple darken-4", "pink darken-4", "deep-purple darken-4", "indigo darken-4",
           "blue darken-4", "light-blue darken-4", "cyan darken-4", "teal darken-4", "green darken-4",
           "light-green darken-4", "lime darken-4", "orange darken-4", "deep-orange darken-4", "brown darken-4",
           "blue-grey darken-4", "grey darken-4", "yellow darken-4"]


def pick_color():
    num = randint(0, len(colors2))
    return colors2[num]
