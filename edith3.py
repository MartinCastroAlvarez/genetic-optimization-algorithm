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

FIT = 1
UNFIT = 0

start = timeit.timeit()

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def fit(sequence: list, a: list, b: list, new_genes: list) -> list:
    a.extend(new_genes[0])
    b.extend(new_genes[1])
    if len(a) == len(b) and a == b:
        return FIT, [], []
    if len(a) > len(b) and a[:len(b)] == b:
        sequence.extend(b)
        return sequence, a[len(b):], []
    if len(b) > len(a) and b[:len(a)] == a:
        sequence.extend(a)
        return sequence, [], b[len(a):]
    return UNFIT, [], []

# Amount of runs.
ages = 20

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
        chromosome[0]
        for chromosome in chromosomes
        if chromosome[0] == FIT
    ]
    min_survivor = min(len(s) for s in survivors) if survivors else 10000

    # For each age, mutations will be performed
    # on the chromosomes and only the survivors will be kept.
    for age in range(ages):
        logger.debug("Age=%s | Chromosomes=%s | Survivors=%s", age, len(chromosomes), len(survivors))
        mutations = (
            (c, g)
            for c in chromosomes
            for g in genes
            if len(c[0]) < min_survivor
            and c[0] != FIT
        )
        raise Exception(list(mutations))
        chromosomes = (
            fit(mutation[0][0], mutation[0][1], mutation[0][2], mutation[1])
            for mutation in mutations
        )
        chromosomes = [
            chromosome
            for chromosome in chromosomes
            if chromosome[0] != UNFIT
        ]
        if not chromosomes:
            break
        survivors.extend([
            chromosome[0]
            for chromosome in chromosomes
            if chromosome[0] == FIT
        ])
        min_survivor = min(len(s) for s in survivors) if survivors else 10000
    raise Exception(survivors)

    # Detecting the final survivor.
    survivors = sorted(survivors, key=lambda s: (len(s), s))
    survivor = survivors[0] if survivors else "IMPOSSIBLE"

    # Printing results to STDOUT.
    title = "Case {}:".format(case_number + 1)
    print(title, survivor)

logger.debug("Took: %s", timeit.timeit() - start)
