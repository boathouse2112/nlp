import itertools


def read_tokens(path_string):
    with open(path_string) as f:
        lines = f.readlines()

    lines = list(
        itertools.chain(*[("<s> " + line + " </s>").split() for line in lines])
    )
    return lines
