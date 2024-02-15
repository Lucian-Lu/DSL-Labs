# Variant 18
import random
import re

class FiniteAutomaton:
    Q = []
    Sigma = []
    Delta = []
    q0 = ''
    F = []

    def __init__(self):
        pass

    def string_belong_to_language(self, input_string) -> tuple:
        # # Checking if some characters aren't in Q or Sigma so that we can return false immediately
        backup_string = input_string
        while input_string != "":
            if "aaa" in input_string:
                input_string = input_string.replace("aaa", "")
            elif "aab" in input_string:
                input_string = input_string.replace("aab", "")
            elif "ab" in input_string:
                input_string = input_string.replace("ab", "")
            else:
                return False, []
        creation_transitions = self.generate_transitions_to_create_word(backup_string)
        return True, creation_transitions

    def generate_transitions_to_create_word(self, input_string) -> []:
        created_transitions_test = []

        while input_string != '':
            test_char = input_string[:3]
            if test_char == "aaa":
                created_transitions_test.extend(['S->aB', 'B->aC', 'C->a'])
                input_string = input_string.replace("aaa", '', 1)
            elif test_char == 'aab':
                created_transitions_test.extend(['S->aB', 'B->aC', 'C->bS'])
                input_string = input_string.replace('aab', '', 1)
            elif test_char[:2] == 'ab':
                created_transitions_test.extend(['S->aA', 'A->bS'])
                input_string = input_string.replace('ab', '', 1)

        return created_transitions_test


class Grammar:
    VN = []
    VT = []
    P = []

    def __init__(self):
        self.VN = ["S", "A", "B", "C"]
        self.VT = ["a", "b"]
        self.P = ["S->aA", "A->bS", "S->aB", "B->aC", "C->a", "C->bS"]
        pass


    def generate_string(self) -> tuple:
        generated_string = "S"
        transition_prerequisite = [ch[0] for ch in self.P]
        pattern = re.compile(r'->(.+)$')
        creation_transitions = []

        # Checking if we still have non-terminal characters
        while any(ch in self.VN for ch in generated_string):
            # Choosing a non-terminal character at random
            random_non_terminal = random.choice([ch for ch in generated_string if ch in self.VN])
            # Choosing a random transition for the non-terminal character
            random_transition_pos = random.choice([i for i, tr in enumerate(transition_prerequisite) if tr in random_non_terminal])
            # Getting the characters which we'll be replacing the non-terminal with using the pattern
            replacing_string = pattern.search(self.P[random_transition_pos]).group(1)
            # Replacing the random non-terminal with the transition
            generated_string = generated_string.replace(random_non_terminal, replacing_string)
            creation_transitions.append(str(random_non_terminal + "->" + replacing_string))

        return generated_string, creation_transitions


    def finite_automaton_conversion(self) -> FiniteAutomaton:
        finite_automaton = FiniteAutomaton()
        # Start state
        finite_automaton.q0 = 'S'
        # Set of states
        finite_automaton.Q = self.VN
        # Alphabet
        finite_automaton.Sigma = self.VT
        # Accepting states
        finite_automaton.F = self.VT
        # Set of rules
        finite_automaton.Delta = self.P

        return finite_automaton


grammar = Grammar()
string = []
transitions = []
while len(string) < 5:
    temp = grammar.generate_string()
    temp_str, temp_trans = temp
    if temp_str not in string:
        string.append(temp_str)
        transitions.append(temp_trans)

for i in range(len(string)):
    print("Generated string[" + str(i + 1) + "] = " + str(string[i]))
    print("Transitions to generate the string: " + str(transitions[i]))

string_to_check = "abababaabababaaa"
finite_automaton = grammar.finite_automaton_conversion()
truth, transitions = finite_automaton.string_belong_to_language(string_to_check)
print("\nIs the string = [" + string_to_check + "] valid for the language? ")
print(truth)
print("Transitions for obtaining the word: " + str(transitions))

