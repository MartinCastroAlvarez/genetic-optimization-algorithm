"""
AUTHOR: Martin Alejandro Castro Alvarez
EMAIL: martincastro.10.5@gmail.com
HOME: https://www.martincastroalvarez.com
DATE: 2019, Feb 21th.

This is the unit test file for edith.py

You can run unit tests by executing the following command:
>>> python -m unittest test_edith.py
"""

import unittest
from parameterized import parameterized

from edith2 import Genes, Sequence
from edith import Genes, Sequence

fixtures = [(
    Sequence.IMPOSSIBLE,
    [
        "a ab",
        "b bb",
        "c cc",
    ]
), (
    "abcd",
    [
        "efgh efgh",
        "d cd",
        "abc ab"
    ]
), (
    "i",
    [
        "efgh efgh",
        "d cd",
        "abc ab",
        "i i",
    ]
), (
    "a",
    [
        "efgh efgh",
        "d cd",
        "a a",
        "i i",
    ]
), (
    "ienjoycorresponding",
    [
        'i ie',
        'ing ding',
        'resp orres',
        'ond pon',
        'oyc y',
        'hello hi',
        'enj njo',
        'or c'
    ]
), (
    "dearalanhowareyou",
    [
        "are yo",
        "you u",
        "how nhoware",
        "alan arala",
        "dear de"
    ]
), (
    Sequence.IMPOSSIBLE,
    [
        "aa aaa",
        "xa as"
    ]
), (
    Sequence.IMPOSSIBLE,
    [
        "i ii",
        "ii e"
    ]
), (
    "zbc",
    [
        "i iii",
        "zb z",
        "iii i",
        "c bc"
    ]
)]



class FunctionalTests(unittest.TestCase):
    """
    Functional Tests.

    Call this script with the following command:
    >>> python -m unittest edith.py
    """

    @parameterized.expand(fixtures)
    def test_sequence(self, output, input_):
        """
        Running functional tests for
        multiple parameters/fixtures.
        """
        input_ = "\n".join(input_)
        g = Genes(input_)
        s = Sequence(genes=g)
        s.run()
        self.assertEquals(s.population.get_survivor(Sequence.IMPOSSIBLE),
                          output)
