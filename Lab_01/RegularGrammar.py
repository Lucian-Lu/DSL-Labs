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


    def classify_grammar(self) -> str:
        left_side = re.compile(r'(.+)(?=\-\>)')
        right_side = re.compile(r'->(.+)$')
        left_side_chars = []
        right_side_chars = []
        for tran in self.P:
            left_side_chars.append(left_side.search(tran).group(1))
            right_side_chars.append(right_side.search(tran).group(1))

        # Checking if the grammar has left-side elements that have terminals or have a length greater than 1
        if not(any(char in chars for char in self.VT for chars in left_side_chars) or any(len(ch) > 1 for ch in left_side_chars)):
            right = False
            left = False

            for chars in right_side_chars:
                # Checking right side for >1 VN or VT
                if sum(ch in self.VN for ch in chars) > 1 or sum(ch in self.VT for ch in chars) > 1:
                    break
                # Checking if the first character is in VN or VT and determining the subtype of the grammar
                if chars[0] in self.VN and len(chars) > 1:
                    right = True
                if chars[0] in self.VT and len(chars) > 1:
                    left = True
            # XOR to determine if we have left or right grammar
            if left ^ right:
                return("Type 3")
        # If not, then it's a combination of the two, meaning it's type two grammar
            else:
                return("Type 2")
        # Type 1 grammar cannot have terminal symbols on the left and can't have an empty string on the right
        elif " " not in right_side_chars and not(any(char in chars for char in self.VT for chars in left_side_chars)):
            return("Type 1")
        # Otherwise, it's just type 0
        else:
            return("Type 0")

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
result = grammar.classify_grammar()
print(result)
# string = []
# transitions = []
# while len(string) < 5:
#     temp = grammar.generate_string()
#     temp_str, temp_trans = temp
#     if temp_str not in string:
#         string.append(temp_str)
#         transitions.append(temp_trans)
#
# for i in range(len(string)):
#     print("Generated string[" + str(i + 1) + "] = " + str(string[i]))
#     print("Transitions to generate the string: " + str(transitions[i]))
#
# strings_to_check = ["abababaabababaaa", "aaa", "c", "abbaaa"]
# finite_automaton = grammar.finite_automaton_conversion()
# for i in range(len(strings_to_check)):
#     truth, transitions = finite_automaton.string_belong_to_language(strings_to_check[i])
#     print("\nIs the string = [" + strings_to_check[i] + "] valid for the language? ")
#     print(truth)
#     if truth:
#         print("Transitions for obtaining the word: " + str(transitions))
