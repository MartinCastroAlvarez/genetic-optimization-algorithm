"""
This is modified version of edith.py which does not use any external library.
The code in this file attempts to solve the problem faster than the previous version.

AUTHOR: Martin Alejandro Castro Alvarez
EMAIL: martincastro.10.5@gmail.com
HOME: https://www.martincastroalvarez.com
DATE: 2019, Feb 21th.

You can execute this script by running this:
>>> cat sample-01.in | python3 -m cProfile -s cumtime edith3.py
"""

import sys

# import timeit
# import logging

# logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)
# start = timeit.timeit()

UNFIT = 0
FITTEST = 1
FIT = 2

MAX_GENERATIONS = 12  # NOTE: 1 <= k <= 11
DEFAULT_SHORTEST_SURVIVOR = 100000
IMPOSSIBLE = "IMPOSSIBLE"


def get_fitness(a: str, b: str) -> str:
    """
    This function returns the fitness of 2 variables
    in this genetic algorithm.
    Fitness will increase as 'a' and 'b' are more similar.
    """
    if a[:len(b)] != b[:len(a)]:
        return UNFIT
    if a == b:
        return FITTEST
    return FIT


def mutate(phenotype: tuple, genotype: tuple, shortest_survivor: int) -> tuple:
    """
    This function will combine a phenotype and a genotype
    into a new phenotype, as if the phenotype mutated
    with the new genetic code.
    """
    a = phenotype[2] + genotype[0]
    b = phenotype[3] + genotype[1]
    path = phenotype[4][:]  # The fastest way to clone is slicing.
    path[genotype[4]] = False
    f = get_fitness(a, b)
    if f == FITTEST:
        shortest_survivor = min(shortest_survivor, len(phenotype[1] + a[:len(b)]))
    return (
        f,
        phenotype[1] + a[:len(b)],
        a[len(b):],
        b[len(a):],
        path,
    )

# The following piece of code reads from stdin
# and truncates the input by case length..
winners = []
for line in sys.stdin:

    # Reading block of characters from stdin.
    genotypes = (
        next(sys.stdin).rstrip().split()
        for _ in range(int(line))  # WARNING: May raise ValueError.
    )
    genotypes = {
        (
            tuple(ord(g) for g in genotype[0]),
            tuple(ord(g) for g in genotype[1]),
            len(genotype[0]),
            len(genotype[1]),
            genotype_id,
        )
        for genotype_id, genotype in enumerate(genotypes)
    }

    # Cleaning genes by removing the
    # ones with wierd characters not
    # in the other pair.
    a_all = {
        char
        for genotype in genotypes
        for char in genotype[0]
    }
    b_all = {
        char
        for genotype in genotypes
        for char in genotype[0]
    }
    genotypes = {
        genotype
        for genotype in genotypes
        if not set(genotype[0]) - b_all
        and not set(genotype[1]) - a_all
    }

    # Detecting systems that might diverge.
    # If all elements on the left or the right
    # are longer than the other genotype, it means
    # the system will inevitable diverge.
    a_diverges = all(
        genotype[2] > genotype[3]
        for genotype in genotypes
    )
    b_diverges = all(
        genotype[2] < genotype[3]
        for genotype in genotypes
    )
    if a_diverges or b_diverges:
        winners.append(IMPOSSIBLE)
        continue

    # Detecting the amount of generations.
    generations = max(len(genotypes), MAX_GENERATIONS)

    # Generating initial population.
    phenotypes = (
        (FIT, (), (), (), [True] * generations),
    )

    # Initializing survivors.
    survivors = []
    shortest_survivor = DEFAULT_SHORTEST_SURVIVOR

    # For each generation, mutations will be performed
    # on the phenotypes and only the survivors will be kept.
    for generation in range(generations):  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # Generating mutations.
        phenotypes = (
            mutate(phenotype=phenotype,
                   genotype=genotype,
                   shortest_survivor=shortest_survivor)
            for phenotype in phenotypes
            for genotype in genotypes
            if phenotype[0] == FIT  # Discard unfit phenotypes.
            and phenotype[4][genotype[4]]  # Avoid repeating an element.
            and len(phenotype[1]) < shortest_survivor  # Discarding long solutions.
            and (  # Only retrieve potentially useful genotypes.
                genotype[0][:len(phenotype[3])] == phenotype[3][:genotype[2]]
                or genotype[1][:len(phenotype[2])] == phenotype[2][:genotype[3]]
            )
        )

        # Removing unfit and duplicated phenotypes.
        phenotypes = {
            phenotype[:3]: phenotype
            for phenotype in phenotypes 
            if phenotype[0] != UNFIT
        }.values()

        # Stopping if there are no more mutations.
        if not phenotypes:
            break

        # Detecting fittest chrosomes.
        survivors.extend(list(filter(lambda phenotype: phenotype[0] == FITTEST,
                         phenotypes)))

    # Detecting the final survivor.
    survivors = sorted(survivors, key=lambda s: (len(s[1]), s[1]))
    winner = "".join(
        chr(s)
        for s in survivors[0][1]
    ) if survivors else IMPOSSIBLE
    winners.append(winner)

# Printing results to STDOUT.
sys.stdout.write("\n".join(
    "".join([
        "Case ",
        str(case_number + 1),
        ": ",
        winner,
    ])
    for case_number, winner in enumerate(winners)
))
sys.stdout.write("\n")

# logger.debug("Took: %s", timeit.timeit() - start)
