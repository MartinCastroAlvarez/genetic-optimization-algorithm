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

import itertools
import logging

UNFIT = "_unfit"

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_fitness(sequence: str, dominance: list, new_genes: list) -> list:
    a = dominance[0] + new_genes[0]
    b = dominance[1] + new_genes[1]
    if sequence and len(a) > 5 * len(sequence):  # Probably diverging.
        return UNFIT, ['', '']
    if a.startswith(b):
        return sequence + b, [a[len(b):], '']
    if b.startswith(a):
        return sequence + a, ['', b[len(a):]]
    return UNFIT, ['', '']


if __name__ == "__main__":

    # Amount of runs.
    ages = 8

    # The following piece of code reads from stdin
    # and truncates the input by case length..
    for case_number, line in enumerate(sys.stdin):
        case_length = int(line)  # WARNING: May raise ValueError.
        case_data = "\n".join([
            next(sys.stdin).replace("\n", "")
            for _ in range(case_length)
        ])

        # This is where the Genetic Algorithm is executed.
        # It will run once per case in the input file.
        genes = [
            line.split()
            for line in case_data.split("\n")
        ]
        chromosomes = [
            get_fitness('', ['', ''], gene)
            for gene in genes
        ]

        # Catching survivors in the origins.
        survivors = [
            chromosome[0]
            for chromosome in chromosomes
            if chromosome[0] != UNFIT
            and not chromosome[1][0]
            and not chromosome[1][1]
        ]
        min_survivor = min(len(s) for s in survivors) if survivors else 10000

        # For each age, mutations will be performed
        # on the chromosomes and only the survivors will be kept.
        for age in range(ages):
            logger.debug("Age=%s | Chromosomes=%s | Survivors=%s", age, len(chromosomes), len(survivors))
            chromosomes = (
                get_fitness(mutation[0][0], mutation[0][1], mutation[1])
                for mutation in (
                    (c, g)
                    for c in chromosomes
                    for g in genes
                    if len(c[0]) < min_survivor
                )
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
                if chromosome[0] != UNFIT
                and not chromosome[1][0]
                and not chromosome[1][1]
            ])
            min_survivor = min(len(s) for s in survivors) if survivors else 10000

        # Detecting the final survivor.
        survivors = sorted(survivors, key=lambda s: (len(s), s))
        survivor = survivors[0] if survivors else "IMPOSSIBLE"

        # Printing results to STDOUT.
        title = "Case {}:".format(case_number + 1)
        print(title, survivor)
