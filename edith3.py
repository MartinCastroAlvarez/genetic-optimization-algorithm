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

import logging

UNFIT = 0
FIT = 1
ONGOING = 2

MAX_AGES = 12
DEFAULT_SHORTEST_SURVIVOR = 100000
IMPOSSIBLE = "IMPOSSIBLE"

start = timeit.timeit()

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)


def mutate(sequence: list, a: list, b:list, gene: list) -> list:

    logger.debug("------------------------------------------------")
    logger.debug("%s | %s %s | %s", sequence, a, b, gene)
    a = a + gene[1]
    b = b + gene[2]

    if a == b:
        logger.debug("FIT")
        return FIT, sequence + a, [], []

    if a[:len(b)] == b[:len(a)]:
        logger.debug("ONGOING")
        return ONGOING, sequence + a[:len(b)], a[len(b):], b[len(a):]

    logger.debug("UNFIT")
    return UNFIT, [], [], []


# The following piece of code reads from stdin
# and truncates the input by case length..
output = []
for line in sys.stdin:

    # Reading block of characters from stdin.
    genes = (
        next(sys.stdin).replace("\n", "").split()
        for _ in range(int(line))  # WARNING: May raise ValueError.
    )
    genes = [
        (
            i,
            list(gene[0]),
            list(gene[1]),
        )
        for i, gene in enumerate(genes)
    ]

    # Detecting systems that might diverge.
    # If all elements on the left or the right
    # are longer than the other gene, it means
    # the system will inevitable diverge.
    a_diverges = all(
        len(gene[1]) > len(gene[2])
        for gene in genes
    )
    b_diverges = all(
        len(gene[2]) > len(gene[1])
        for gene in genes
    )
    if a_diverges or b_diverges:
        output.append(IMPOSSIBLE)
        continue

    # Generating initial population.
    chromosomes = (
        mutate(sequence=[], a=[], b=[], gene=gene)
        for gene in genes
        if gene[1][:len(gene[2])] == gene[2][:len(gene[1])]
        and gene[2][:len(gene[1])] == gene[1][:len(gene[2])]
    )
    chromosomes = {
        hash(str(chromosome)): chromosome
        for chromosome in chromosomes
        if chromosome[0] != UNFIT
    }

    # Catching survivors in the origins.
    survivors = [
        chromosome[1]
        for chromosome in chromosomes.values()
        if chromosome[0] == FIT
    ]
    shortest_survivor = min(
        len(survivor)
        for survivor in survivors
    ) if survivors else DEFAULT_SHORTEST_SURVIVOR

    # For each age, mutations will be performed
    # on the chromosomes and only the survivors will be kept.
    age = 1
    while True:

        logger.debug("====================================")
        logger.debug("Age:%s", age)
        logger.debug("Chromosomes=%s", chromosomes)
        logger.debug("====================================")

        # Generating mutations.
        chromosomes = (
            mutate(sequence=chromosome[1],
                   a=chromosome[2],
                   b=chromosome[3],
                   gene=gene)
            for chromosome in chromosomes.values()
            for gene in genes
            if chromosome[0] == ONGOING
            and len(chromosome[1]) < shortest_survivor
            and (
                gene[1][:len(chromosome[3])] == chromosome[3][:len(gene[1])]
                or gene[2][:len(chromosome[2])] == chromosome[2][:len(gene[2])]
            )
        )
        chromosomes = {
            hash(str(chromosome)): chromosome
            for chromosome in chromosomes
            if chromosome[0] != UNFIT
        }

        # Detecting when to stop.
        if not chromosomes:
            break

        # Detecting fittest chrosomes.
        survivors.extend(
            chromosome[1]
            for chromosome in chromosomes.values()
            if chromosome[0] == FIT
        )
        shortest_survivor = min(
            len(survivor)
            for survivor in survivors
        ) if survivors else DEFAULT_SHORTEST_SURVIVOR

    # Detecting the final survivor.
    survivors = sorted(survivors, key=lambda s: (len(s), s))
    output.append("".join(survivors[0]) if survivors else IMPOSSIBLE)

# Printing results to STDOUT.
print("\n".join(
    "".join([
        "Case ",
        str(case_number + 1),
        ": ",
        survivor,
    ])
    for case_number, survivor in enumerate(output)
))
logger.debug("Took: %s", timeit.timeit() - start)
