"""
This is modified version of edith.py which does not use any external library.
The code wil look ugly and the script will not scale so easily.

AUTHOR: Martin Alejandro Castro Alvarez
EMAIL: martincastro.10.5@gmail.com
HOME: https://www.martincastroalvarez.com
DATE: 2019, Feb 21th.

You can execute this script by running this:
>>> cat sample-01.in | python3 edith2.py
"""

import os
import sys
import json

import logging

logger = logging.getLogger(__name__)


class Genes(object):
    """
    Genes in this Genetic Algorithm represent the
    set of (a, b) pairs in the search space.

    @constant A: Represents the set of all 'a' elements in the genetic pairs.
    @constant B: Represents the set of all 'b' elements in the genetic pairs.
    """

    def __init__(self, genes: str=None):
        """
        Constructing the genetic code.

        @param genes: A string containing 2 columns is required.
                      The first column will be 'a' and the second
                      column will be 'b'.
        """
        logger.debug("Constructing genetic code.")
        if not genes:
            raise ValueError("Genetic code must not be empty.")
        if not isinstance(genes, str):
            raise ValueError("Expecting a string, not:", type(genes))
        self.A = []
        self.B = []
        for gene in genes.split("\n"):
            a, b = gene.split(" ")
            self.A.append(a)
            self.B.append(b)

    def get_genes(self, **kwargs) -> list:
        """
        Genes getter.

        This function returns the [dict instead of pd.DataFrame] 
        containing the genetic pairs.

        The purpose of this method is to provide
        custom mutations in the future. For example,
        by getting only genes that start with "s".
        """
        for i, _ in enumerate(self.A):
            yield [self.A[i], self.B[i]]

    @property
    def size(self) -> int:
        """
        Size getter.

        This function returns the size of the genetic code.
        """
        return len(self.A)

    def __str__(self):
        """ To String method. """
        return "<Genes: {}>".format(self.size)


class Population(object):
    """
    This class represents the active survivors playing the game.

    In each run, the population mutates and fitness is evaluated.
    Survivors and unfit chromosomes are removed from the population.

    You can keep mutating the population endlessly until
    there are no more possible combinations.

    @constant A_DOMINANCE: It represents gene A being stronger than gene B.
    @constant B_DOMINANCE: It represents gene B being stronger than gene A.

    @constant UNFIT: It is used to mark chromosomes as unfit.
    @constant FIT: It is used to detect winner chromosomes.

    @constant TMP_SUFFIX: It is a temporal constant used to merge datasets.
    @constant TMP_INDEX: It is a temporal constant used to merge datasets.
    """

    A_DOMINANCE = "A Dominance"
    B_DOMINANCE = "B Dominance"

    UNFIT = "_unfit"
    FIT = "_fit"

    TMP_SUFFIX = "_new"
    TMP_INDEX = "_tmp_idx"

    def __init__(self, genes: Genes=None):
        """
        Population constructor.

        @param genes: A Genes instance is required.
                      Mutations will take genes from this
                      instance and generate variations.

        NOTE: The initial set of chromosomes will only contain
              pairs of genes whose first character match in order
              to reduce the algorithm complexity.
        """
        logger.debug("Constructing new population.")
        if not isinstance(genes, Genes):
            raise ValueError("Invalid genes:", genes)
        if not genes.size:
            raise RuntimeError("Empty genetic code.")
        self.genes = genes
        self.survivors = []
        self.chromosomes = []
        for gene in self.genes.get_genes():
            if gene[0].startswith(gene[1]) or gene[1].startswith(gene[0]):
                self.chromosomes.append(gene)
        self.fit()

    def __str__(self):
        """ To String method. """
        return "<Population: {}>".format(self.size)

    @property
    def size(self) -> int:
        """
        Size getter.

        This function returns the amount of
        active chromosomes in this population.
        """
        return len(self.chromosomes)

    def get_survivor(self, default: str=None) -> str:
        """
        Survivor getter.

        This function returns the survivor name.

        If multiple surivors exist, only the first will be returned.
        The list of survivors will be arranged by string length
        and then in alphabetical order

        @param default: String value that will be
                        returned if there are no survivors.
        """
        if not self.survivors:
            return default
        survivors = [
            survivor[0]
            for survivor in self.survivors
        ]
        survivors = sorted(survivors, key=lambda s: (len(s), s))
        return survivors[0]

    def fit(self):
        """
        This method is used to detect the fitness of the population.

        The dominance of genes 'A' and 'B' will be calculated.
        logger.debug("Fitting population.")
        """
        self.__calculate_dominance()
        self.__remove_unfit()
        self.__remove_fit()
        logger.debug(json.dumps(self.chromosomes, indent=4))

    def __calculate_dominance(self):
        """
        This private method will calculate the dominance of
        gene 'A' over 'B' as well as the dominance of 'B' over 'A'.

        For example, if 'A' is 'asdf' and 'B' is 'as', then 'A' is dominant.
        The dominance will be 'df' because 'asdf' - 'as' = 'df'

        This can be later used to remove unfit chromosomes.
        """
        for i, chromosome in enumerate(self.chromosomes):
            a_dominance = self.get_fitness(chromosome[0], chromosome[1])
            b_dominance = self.get_fitness(chromosome[1], chromosome[0])
            self.chromosomes[i].append(a_dominance)
            self.chromosomes[i].append(b_dominance)

    @classmethod
    def get_fitness(cls, a: str=None, b: str=None):
        """
        This function must be used to calculate
        the string distance of 2 strings in a DataFrame.

        @param row: A DataFrame containing 2 elements.

        It will return FIT if the 2 strings match.
        It will return UNFIT if strings don't match.

        For example:
        >>> fitness("AJYFAJYF", "AJY")
        'FAJYF'
        >>> fitness("AASD", "FD")
        '_unfit'
        >>> fitness("AA", "AA")
        '_fit'
        """
        if a == b:
            return cls.FIT
        if a.startswith(b):
            return a[len(b):]
        return cls.UNFIT

    def __remove_unfit(self):
        """
        This private method will remove unfit chromosomes
        from the population.

        For example, only one gene can be dominant.
        If 'A' and 'B' are both dominant, it means the
        genes can not fuse and the chromosome will adapt.
        """
        self.chromosomes = [
            chromosome
            for chromosome in self.chromosomes
            if (chromosome[2] == self.UNFIT and chromosome[3] != self.UNFIT)
            or (chromosome[2] != self.UNFIT and chromosome[3] == self.UNFIT)
            or (chromosome[2] != self.UNFIT and chromosome[3] != self.UNFIT)
        ]

    def __remove_fit(self):
        """
        This private method detects winners in the population.

        Chromosomes that match the expected result will be
        removed from the chromosomes dataset and put into
        a different dataset.

        As a consequence, they won't be used for further mutations
        because there is at least 1 survivor that has higher
        alphabetical priority in the final result.
        """
        new_generation = []
        for chromosome in self.chromosomes:
            if chromosome[2] == self.FIT:
                self.survivors.append(chromosome)
            else:
                new_generation.append(chromosome)
        self.chromosomes = new_generation

    def mutate(self):
        """
        Genetic Mutation method.

        A new set of genes will be generated from the genetic code.

        Then, it will be combined with the current chromosomes
        in order to create more chromosomes from both.
        """
        logger.debug("Mutating population.")
        new_generation = []
        for gene in self.genes.get_genes():
            for chromosome in self.chromosomes:
                new_generation.append([
                    chromosome[0] + gene[0],
                    chromosome[1] + gene[1],
                ])
        self.chromosomes = new_generation
        logger.debug(json.dumps(self.chromosomes, indent=4))


class Sequence(object):
    """
    A Sequence represents a population mutating their
    genes over multiple configurable ages. Unfit chromosomes
    are removed from the population and only the fittest survive.

    @constant IMPOSSIBLE: Used to mark sequences as unresolvable.
    """

    IMPOSSIBLE = "IMPOSSIBLE"

    def __init__(self, genes: Genes=None, ages: int=10):
        """
        Sequence Constructor.

        @param genes: A Genes instance containing the genetic code.
        @param ages: The amount of iterations in which the
                     population will mutate.
        """
        if not isinstance(genes, Genes):
            raise ValueError("Invalid genes:", genes)
        if not isinstance(ages, int) or ages < 1:
            raise ValueError("Invalid amount of ages:", ages)
        self.ages = ages
        self.population = Population(genes=genes)

    def __str__(self):
        """ To String method. """
        return "<Sequence: {}>".format(self.ages)

    def run(self):
        """
        Main method.

        This method will run multiple times, mutation the
        population and attempting to get a survivor chromosome.

        At the end of the iterations, the winner can be
        retrieved by executing: self.population.get_survivor().
        """
        logger.debug("Analyzing sequence.")
        if self.population.chromosomes:
            for age in range(self.ages):
                logger.debug("Running on age: %s/%s.", age + 1, self.ages)
                self.population.mutate()
                self.population.fit()
                if not self.population.chromosomes:
                    logger.debug("Breaking iteration.")
                    break
        logger.debug("Finished analyzing sequence.")


if __name__ == "__main__":

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

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
        g = Genes(case_data)
        s = Sequence(genes=g, ages=ages)
        s.run()

        # Printing results to STDOUT.
        title = "Case {}:".format(case_number + 1)
        print(title, s.population.get_survivor(Sequence.IMPOSSIBLE))
