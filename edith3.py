"""
This is modified version of edith.py which does not use any external library.
The code in this file attempts to solve the problem faster than the previous version.

AUTHOR: Martin Alejandro Castro Alvarez
EMAIL: martincastro.10.5@gmail.com
HOME: https://www.martincastroalvarez.com
DATE: 2019, Feb 21th.

You can execute this script by running this:
>>> cat sample-01.in | python3 edith3.py
"""

import sys
import timeit

import itertools
import logging

UNFIT = 0
FIT = 1
PARTIAL = 2

start = timeit.timeit()

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def fit(sequence: list, a: list, b: list, new_genes: list) -> list:
    a = a + new_genes[0]
    b = b + new_genes[1]
    # logger.debug(a)
    if len(sequence) > 50:
        return UNFIT, [], [], []
    if len(a) == len(b) and a == b:
        return FIT, sequence + a, [], []
    if len(a) > len(b) and a[:len(b)] == b:
        return PARTIAL, sequence + b, a[len(b):], []
    if len(b) > len(a) and b[:len(a)] == a:
        return PARTIAL, sequence + a, [], b[len(a):]
    return UNFIT, [], [], []

# Amount of runs.
ages = 12

# The following piece of code reads from stdin
# and truncates the input by case length..
for case_number, line in enumerate(sys.stdin):

    # Reading block of characters from stdin.
    case_length = int(line)  # WARNING: May raise ValueError.
    genes = (
        next(sys.stdin).replace("\n", "").split()
        for _ in range(case_length)
    )
    genes = [
        (
            list(gene[0]),
            list(gene[1]),
        )
        for gene in genes
    ]

    # Generating initial population.
    chromosomes = (
        fit([], [], [], gene)
        for gene in genes
    )
    chromosomes = [
        chromosome
        for chromosome in chromosomes
        if chromosome[0] != UNFIT
    ]

    # Catching survivors in the origins.
    survivors = [
        chromosome[1]
        for chromosome in chromosomes
        if chromosome[0] == FIT
    ]
    min_survivor = min(len(s) for s in survivors) if survivors else 10000

    # For each age, mutations will be performed
    # on the chromosomes and only the survivors will be kept.
    for age in range(ages):

        # Generating mutations.
        mutations = (
            (c, g)
            for c in chromosomes
            for g in genes
            if c[0] != UNFIT
            and c[0] != FIT
            and len(c[1]) < min_survivor
            and c[2] == g[1][:len(c[2])]
            and c[3] == g[0][:len(c[3])]
        )

        # Evaluting mutation fitness.
        chromosomes = [
            fit(mutation[0][1],
                mutation[0][2],
                mutation[0][3],
                mutation[1])
            for mutation in mutations
        ]

        # Detecting when to stop.
        if not chromosomes:
            break

        # Detecting fittest chrosomes.
        survivors.extend(
            chromosome[1]
            for chromosome in chromosomes
            if chromosome[0] == FIT
        )
        min_survivor = min(
            len(s)
            for s in survivors
        ) if survivors else 10000

    # Detecting the final survivor.
    survivors = sorted(survivors, key=lambda s: (len(s), s))
    survivor = "".join(survivors[0]) if survivors else "IMPOSSIBLE"

    # Printing results to STDOUT.
    title = "Case {}:".format(case_number + 1)
    print(title, survivor)

logger.debug("Took: %s", timeit.timeit() - start)
