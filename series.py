# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

import itertools


def to_int(B: list):
    """
    Given a list of bits such as [1, 0, 1],
    returns the integer that it represents
    based on some series formula.
    """
    return sum(
        B[i] * (-2) ** i
        for i in range(len(B))
    )


GENOTYPE = (0, 1)

def get_mutations(size: int):
    """
    Given a phenotype size, generates a list
    of phenotypes using from the genotype.
    """
    return itertools.product(GENOTYPE, repeat=size)


def solution(A: list):
    """
    Given a sequence of bits such as [1, 0, 1]
    representing some integer X, returns the
    shortest sequence of bits representing X + 1.
    """
    assert A
    assert isinstance(A, list)
    assert all([x in GENOTYPE for x in A])
    fittest = to_int(A) + 1
    generation = 1
    while True:
        for phenotype in get_mutations(size=generation):
            # print(phenotype, to_int(phenotype), fittest)
            if to_int(phenotype) == fittest:
                return list(phenotype)
        generation += 1
    # This should probably stop after X iterations?


if __name__ == "__main__":
    
    assert to_int([1, 0, 1]) == 5
    assert to_int([1, 1, 1]) == 3
    assert to_int([0, 0, 1]) == 4
    assert to_int([0, 1, 0, 1, 1]) == 6
    
    assert solution([1, 0, 1]) == [0, 1, 0, 1, 1]
    assert solution([1, 1, 1]) == [0, 0, 1]
