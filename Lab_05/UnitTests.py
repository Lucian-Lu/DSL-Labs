import unittest
from ChomskyNormalForm import ChomskyNormalForm


class TestChomskyNormalForm(unittest.TestCase):
    def test_chomsky_for_variant18(self):
        chomsky_instance = ChomskyNormalForm(
            ["S", "A", "B", "C", "D"],
            ["a", "b"],
            {
                "S": ["aB", "bA", "A"],
                "A": ["B", "Sa", "bBA", "b"],
                "B": ["b", "bS", "aD", "ε"],
                "C": ["Ba"],
                "D": ["AA"]
            }
        )
        chomsky = chomsky_instance.to_chomsky_normal_form()
        dict_to_verify = {'S': ['a', 'b', 'ε', 'X1B', 'X2A', 'SX1', 'X3A', 'X2S', 'X1D'],
                          'A': ['b', 'ε', 'SX1', 'X3A', 'X2A', 'X2S', 'X1D'], 'B': ['b', 'X2S', 'X1D'],
                          'D': ['AA'], 'X1': 'a', 'X2': 'b', 'X3': 'X2B'}
        self.assertDictEqual(chomsky.P, dict_to_verify)

    def test_chomsky_for_variant19(self):
        chomsky_instance = ChomskyNormalForm(
            ["S", "A", "B", "C", "E"],
            ["a", "d"],
            {
                "S": ["dB", "B"],
                "A": ["d", "dS", "aAdCB"],
                "B": ["aC", "bA", "AC"],
                "C": ["ε"],
                "E": ["AS"]
            }
        )
        chomsky = chomsky_instance.to_chomsky_normal_form()
        dict_to_verify = {'S': ['bA', 'AC', 'a', 'd', 'X1B', 'X2C', 'X1S', 'X5B', 'X4B'], 'A': ['d', 'X1S', 'X5B', 'X4B'],
                          'B': ['bA', 'AC', 'a', 'd', 'X2C', 'X1S', 'X5B', 'X4B'],
                          'X1': 'd', 'X2': 'a', 'X3': 'X2A', 'X4': 'X3X1', 'X5': 'X4C'}

        self.assertDictEqual(chomsky.P, dict_to_verify)

    def test_chomsky_for_variant20(self):
        chomsky_instance = ChomskyNormalForm(
            ["S", "A", "B", "C", "D"],
            ["a", "b"],
            {
                "S": ["aB", "bA", "B"],
                "A": ["b", "aD", "AS", "bAB", "ε"],
                "B": ["a", "bS"],
                "C": ["AB"],
                "D": ["BB"]
            }
        )
        chomsky = chomsky_instance.to_chomsky_normal_form()
        dict_to_verify = {'S': ['b', 'a', 'X1B', 'X2A', 'X2S'], 'A': ['b', 'AS', 'a', 'X1D', 'X3B', 'X2B', 'X1B', 'X2A', 'X2S'],
                          'B': ['a', 'X2S'], 'D': ['BB'], 'X1': 'a', 'X2': 'b', 'X3': 'X2A'}

        self.assertDictEqual(chomsky.P, dict_to_verify)


if __name__ == "__main__":
    unittest.main()
